segment_symbols = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
}

binary_operators = {
    "add": "+",
    "sub": "-",
    "neg": "-",
    "not": "!",
    "and": "&",
    "or": "|",
}

unary_operators = {
    "neg": "-",
    "not": "!",
}

comparison_jumps = {
    "eq": "JEQ",
    "gt": "JGT",
    "lt": "JLT",
}


def resolve_address(segment: str, index: int, file_name: str) -> str:
    if segment in segment_symbols:
        return segment_address(segment, index)
    elif segment == "temp":
        return f"@{5 + index}\n"
    elif segment == "pointer":
        return f"@{3 + index}\n"
    elif segment == "static":
        return f"@{file_name}.{index}\n"
    else:
        raise ValueError(f"Invalid segment: {segment}")


def segment_address(segment: str, index: int) -> str:
    """计算段地址，将地址存储在 A 寄存器"""
    return f"@{index}\n"\
           "D=A\n"\
           f"@{segment_symbols[segment]}\n"\
           "A=D+M\n"


def push_d() -> str:
    """将 D 寄存器的值压入栈"""
    return "@SP\n"\
           "A=M\n"\
           "M=D\n"\
           "@SP\n"\
           "M=M+1\n"


def pop_d() -> str:
    """将栈顶值弹出到 D 寄存器"""
    return "@SP\n"\
           "M=M-1\n"\
           "A=M\n"\
           "D=M\n"
