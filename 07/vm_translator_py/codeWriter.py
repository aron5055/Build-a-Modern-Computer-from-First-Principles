from type import CommandType
from Code import *
from pathlib import Path


class CodeWriter:
    def __init__(self, output_path: str) -> None:
        self.file = open(output_path, "w")
        self.file_name = Path(output_path).stem

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
                self.comparison_count = getattr(
                    self, 'comparison_count', 0) + 1
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
