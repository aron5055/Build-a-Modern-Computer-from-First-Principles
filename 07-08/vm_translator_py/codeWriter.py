from type import CommandType
from Code import *
from pathlib import Path


class CodeWriter:
    def __init__(self, output_path: str) -> None:
        self.file = open(output_path, "w")
        self.file_name = Path(output_path).stem
        self.function_call_count = 0
        self.comparison_count = 0
        self.current_function = ""

    def write_init(self) -> None:
        comments = "// init\n"
        code = "@256\nD=A\n@SP\nM=D\n"
        self.file.write(comments + code)
        self.write_call("Sys.init", 0)

    def set_file_name(self, file_name: str) -> None:
        self.file_name = Path(file_name).stem

    def write_arithmetic(self, command: str) -> None:
        comments = f"// {command}\n"
        match command:
            case "add" | "sub" | "and" | "or":
                code = pop_d()
                code += "@R13\nM=D\n"
                code += "@SP\nA=M-1\nD=M\n"
                code += f"@R13\nD=D{binary_operators[command]}M\n"
                code += "@SP\nA=M-1\nM=D\n"
            case "neg" | "not":
                code = f"@SP\nA=M-1\nM={unary_operators[command]}M\n"
            case "eq" | "gt" | "lt":
                self.comparison_count += 1
                label = f"{self.file_name}${command}${self.comparison_count}"
                code = pop_d()
                code += "A=A-1\n"     # 指向第二个操作数
                code += "D=M-D\n"     # 计算差值
                code += f"@{label}_TRUE\n"
                code += f"D;{comparison_jumps[command]}\n"  # 根据条件跳转
                code += "@SP\n"
                code += "A=M-1\n"
                code += "M=0\n"       # false case
                code += f"@{label}_END\n"
                code += "0;JMP\n"
                code += f"({label}_TRUE)\n"
                code += "@SP\n"
                code += "A=M-1\n"
                code += "M=-1\n"      # true case (-1 表示 true)
                code += f"({label}_END)\n"
            case _:
                raise ValueError(f"Invalid command: {command}")
        self.file.write(comments + code)

    def write_push_pop(self, command: CommandType, segment: str, index: int) -> None:
        comments = f"// {command.name} {segment} {index}\n"
        match command:
            case CommandType.C_PUSH:
                code = self._get_push_code(segment, index)
            case CommandType.C_POP:
                code = self._get_pop_code(segment, index)
            case _:
                raise ValueError(f"Invalid command: {command}")
        self.file.write(comments + code)

    def write_label(self, label: str) -> None:
        comments = f"// label {label}\n"
        code = f"({self.current_function}${label})\n"
        self.file.write(comments + code)

    def write_goto(self, label: str) -> None:
        comments = f"// goto {label}\n"
        code = f"@{self.current_function}${label}\n0;JMP\n"
        self.file.write(comments + code)

    def write_if(self, label: str) -> None:
        comments = f"// if-goto {label}\n"
        code = pop_d()
        code += f"@{self.current_function}${label}\nD;JNE\n"
        self.file.write(comments + code)

    def write_function(self, name: str, n_locals: int) -> None:
        self.current_function = name
        comments = f"// function {name} {n_locals}\n"
        code = f"({name})\n"
        # every local variable is initialized to 0
        for _ in range(n_locals):
            code += "@0\nD=A\n" + push_d()
        self.file.write(comments + code)

    def write_call(self, name: str, n_args: int) -> None:
        comments = f"// call {name} {n_args}\n"
        return_address = f"{self.file_name}.{name}$ret.{self.function_call_count}"
        self.function_call_count += 1

        code = (
            # push returnAddress
            f"@{return_address}\n"
            "D=A\n"
            + push_d()

            # push LCL
            + "@LCL\n"
            "D=M\n"
            + push_d()

            # push ARG
            + "@ARG\n"
            "D=M\n"
            + push_d()

            # push THIS
            + "@THIS\n"
            "D=M\n"
            + push_d()

            # push THAT
            + "@THAT\n"
            "D=M\n"
            + push_d()

            # ARG = SP-5-nArgs
            + "@SP\n"
            "D=M\n"
            "@5\n"
            "D=D-A\n"
            f"@{n_args}\n"
            "D=D-A\n"
            "@ARG\n"
            "M=D\n"

            # LCL = SP
            + "@SP\n"
            "D=M\n"
            "@LCL\n"
            "M=D\n"

            # goto f
            + f"@{name}\n"
            "0;JMP\n"

            # (returnAddress)
            + f"({return_address})\n"
        )

        self.file.write(comments + code)

    def write_return(self) -> None:
        comments = "// return\n"
        code = (
            # frame = LCL
            "@LCL\n"
            "D=M\n"
            "@R13\n"  # R13 = frame
            "M=D\n"

            # retAddr = *(frame-5)
            "@5\n"
            "A=D-A\n"  # A = frame-5
            "D=M\n"    # D = *(frame-5)
            "@R14\n"   # R14 = retAddr
            "M=D\n"

            # *ARG = pop()
            + pop_d()
            + "@ARG\n"
            "A=M\n"
            "M=D\n"

            # SP = ARG+1
            "@ARG\n"
            "D=M+1\n"
            "@SP\n"
            "M=D\n"

            # THAT = *(frame-1)
            "@R13\n"
            "A=M-1\n"
            "D=M\n"
            "@THAT\n"
            "M=D\n"

            # THIS = *(frame-2)
            "@R13\n"
            "D=M\n"
            "@2\n"
            "A=D-A\n"
            "D=M\n"
            "@THIS\n"
            "M=D\n"

            # ARG = *(frame-3)
            "@R13\n"
            "D=M\n"
            "@3\n"
            "A=D-A\n"
            "D=M\n"
            "@ARG\n"
            "M=D\n"

            # LCL = *(frame-4)
            "@R13\n"
            "D=M\n"
            "@4\n"
            "A=D-A\n"
            "D=M\n"
            "@LCL\n"
            "M=D\n"

            # goto retAddr
            "@R14\n"
            "A=M\n"
            "0;JMP\n"
        )
        self.file.write(comments + code)

    def _get_push_code(self, segment: str, index: int) -> str:
        if segment == "constant":
            code = f"@{index}\nD=A\n"
        else:
            code = resolve_address(segment, index, self.file_name)
            code += "D=M\n"
        return code + push_d()

    def _get_pop_code(self, segment: str, index: int) -> str:
        code = resolve_address(segment, index, self.file_name)
        code += "D=A\n@R13\nM=D\n"
        code += pop_d()
        code += "@R13\nA=M\nM=D\n"
        return code

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.file.close()
