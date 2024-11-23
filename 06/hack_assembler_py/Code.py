from Parser import *
from SymbolTable import symbol_table


def translate_a(line: str) -> str:
    try:
        value = int(line[1:])
    except ValueError:
        value = symbol_table.get_address(line[1:])
    return f'{value:016b}\n'


def translate_dest(d: str) -> str:
    dest_table = {
        '': '000', 'M': '001', 'D': '010', 'MD': '011',
        'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'
    }
    return dest_table.get(d, '000')


def translate_comp(c: str) -> str:
    comp_table = {
        '0': '0101010',   '1': '0111111',   '-1': '0111010',
        'D': '0001100',   'A': '0110000',   'M': '1110000',
        '!D': '0001101',  '!A': '0110001',  '!M': '1110001',
        '-D': '0001111',  '-A': '0110011',  '-M': '1110011',
        'D+1': '0011111', 'A+1': '0110111', 'M+1': '1110111',
        'D-1': '0001110', 'A-1': '0110010', 'M-1': '1110010',
        'D+A': '0000010', 'D+M': '1000010',
        'D-A': '0010011', 'D-M': '1010011',
        'A-D': '0000111', 'M-D': '1000111',
        'D&A': '0000000', 'D&M': '1000000',
        'D|A': '0010101', 'D|M': '1010101'
    }
    return comp_table.get(c, '0000000')


def translate_jump(j: str) -> str:
    jump_table = {
        '': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
        'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'
    }
    return jump_table.get(j, '000')


def translate(line: str) -> str:
    match instruction_type(line):
        case InstructionType.A:
            return translate_a(line)
        case InstructionType.C:
            comp_part = translate_comp(comp(line))
            dest_part = translate_dest(dest(line))
            jump_part = translate_jump(jump(line))
            # print(
            #     f"debug: {comp(line)}: {comp_part}, {dest(line)}: {dest_part}, {jump(line)}: {jump_part}")
            return f'111{comp_part}{dest_part}{jump_part}\n'
        case _:
            return ''
