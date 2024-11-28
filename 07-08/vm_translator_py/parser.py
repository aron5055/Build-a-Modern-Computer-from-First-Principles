from type import CommandType


class Parser:
    def __init__(self, file_path) -> None:
        self.contents = self._read_file(file_path)
        self.code = self._remove_comments_and_whitespace()
        self.index = 0
        self.current_command = ""

    def has_more_lines(self) -> bool:
        return self.index < len(self.code)

    def advance(self) -> None:
        self.current_command = self.code[self.index]
        self.index += 1

    def command_type(self) -> CommandType:
        if self.current_command.startswith("push"):
            return CommandType.C_PUSH
        elif self.current_command.startswith("pop"):
            return CommandType.C_POP
        elif self.current_command.startswith("label"):
            return CommandType.C_LABEL
        elif self.current_command.startswith("goto"):
            return CommandType.C_GOTO
        elif self.current_command.startswith("if-goto"):
            return CommandType.C_IF
        elif self.current_command.startswith("function"):
            return CommandType.C_FUNCTION
        elif self.current_command.startswith("return"):
            return CommandType.C_RETURN
        elif self.current_command.startswith("call"):
            return CommandType.C_CALL
        else:
            return CommandType.C_ARITHMETIC

    def arg1(self) -> str:
        if self.command_type() == CommandType.C_ARITHMETIC:
            return self.current_command
        else:
            return self.current_command.split()[1]

    def arg2(self) -> int:
        return int(self.current_command.split()[2])

    def _read_file(self, file_path) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def _remove_comments_and_whitespace(self) -> list[str]:
        code = []
        for line in self.contents.split("\n"):
            if '//' in line:
                line = line.split('//')[0]
            if line.strip():
                code.append(line.strip())
        return code


if __name__ == "__main__":
    parser = Parser("test.vm")
    print(parser.code)
