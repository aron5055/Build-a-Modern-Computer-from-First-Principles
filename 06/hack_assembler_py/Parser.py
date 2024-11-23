from enum import Enum, auto
from typing import Iterator


class InstructionType(Enum):
    A = auto()
    C = auto()
    L = auto()


def remove_whitespace_and_comments(lines: list[str]) -> list[str]:
    cleaned = []
    for line in lines:
        if '//' in line:
            line = line[:line.index('//')]
        if line.strip():
            cleaned.append(line.strip())
    return cleaned


def get_content(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as file:
        return remove_whitespace_and_comments(file.read().split('\n'))


def address_lines(path: str) -> Iterator[tuple[int, str]]:
    address = 0
    for line in get_content(path):
        if instruction_type(line) == InstructionType.L:
            yield address, line
        else:
            yield address, line
            address += 1


def instruction_type(line: str) -> InstructionType:
    if line.startswith('@'):
        return InstructionType.A
    elif '=' in line or ';' in line:
        return InstructionType.C
    elif '(' in line and ')' in line:
        return InstructionType.L
    raise ValueError(f'Invalid instruction type: {line}')


def symbol(line: str) -> str:
    match instruction_type(line):
        case InstructionType.A:
            return line[1:]
        case InstructionType.L:
            return line[1:-1]
        case _:
            raise ValueError(f'Invalid symbol: {line}')


def dest(line: str) -> str:
    if '=' in line:
        return line.split('=')[0]
    return ''


def comp(line: str) -> str:
    if '=' in line:
        return line.split('=')[1]
    if ';' in line:
        return line.split(';')[0]
    return line


def jump(line: str) -> str:
    if ';' in line:
        return line.split(';')[1]
    return ''
