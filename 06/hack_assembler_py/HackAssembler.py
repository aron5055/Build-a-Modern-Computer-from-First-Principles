from SymbolTable import symbol_table
from Code import translate
from Parser import *
import argparse
import os
from pathlib import Path


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Assemble Hack assembly code into binary.')
    parser.add_argument(
        'file', type=str, help='The path to the assembly file to assemble.')
    parser.add_argument('-o', '--output', type=str,
                        help='The path to the output file.')

    return parser


def validate_args(args):
    if not os.path.exists(args.file):
        raise FileNotFoundError(f'File not found: {args.file}')

    if not args.file.endswith('.asm'):
        raise ValueError('File must have a .asm extension.')

    if not args.output:
        args.output = str(Path(args.file).with_suffix('.hack'))

    return True


def main():
    parser = create_parser()
    args = parser.parse_args()
    validate_args(args)

    lines = get_content(args.file)
    # first pass, add labels to symbol table
    for address, line in address_lines(args.file):
        if instruction_type(line) == InstructionType.L:
            symbol_table.add_entry(symbol(line), address)
    # second pass, add variables to symbol table
    for line in lines:
        if instruction_type(line) == InstructionType.A:
            s = symbol(line)
            if not s.isdigit() and not symbol_table.contains(s):
                symbol_table.add_entry(s, symbol_table.get_next_address())

    translated = list(filter(lambda x: x != '', map(translate, lines)))
    with open(args.output, 'w') as f:
        f.write(''.join(translated))


if __name__ == '__main__':
    main()
