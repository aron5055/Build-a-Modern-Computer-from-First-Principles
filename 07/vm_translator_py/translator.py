import argparse
import os
from pathlib import Path
from parser import Parser
from codeWriter import CodeWriter
from type import CommandType


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="VM translator")
    parser.add_argument("file", help="Path to the input VM file")
    parser.add_argument(
        "-o", "--output", help="Path to the output assembly file")
    return parser


def validate_file(args: argparse.Namespace) -> None:
    if not os.path.exists(args.file):
        raise FileNotFoundError(f"File not found: {args.file}")

    if not args.file.endswith(".vm"):
        raise ValueError("The input file must be a VM file.")

    if not args.output:
        args.output = str(Path(args.file).with_suffix(".asm"))


def main():
    args = create_parser().parse_args()
    validate_file(args)

    parser = Parser(args.file)

    with CodeWriter(args.output) as code_writer:
        while parser.has_more_lines():
            parser.advance()
            match parser.command_type():
                case CommandType.C_ARITHMETIC:
                    code_writer.write_arithmetic(parser.arg1())
                case CommandType.C_PUSH | CommandType.C_POP:
                    code_writer.write_push_pop(
                        parser.command_type(), parser.arg1(), parser.arg2())
                case _:
                    raise ValueError(
                        f"Invalid command: {parser.current_command}")


if __name__ == "__main__":
    main()
