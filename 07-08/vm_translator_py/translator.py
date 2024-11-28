import argparse
import os
from pathlib import Path
from parser import Parser
from codeWriter import CodeWriter
from type import CommandType


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="VM translator")
    parser.add_argument("path", help="Path to the input VM file or directory")
    parser.add_argument(
        "-o", "--output", help="Path to the output assembly file")
    return parser


def validate_path(args: argparse.Namespace) -> None:
    if not os.path.exists(args.path):
        raise FileNotFoundError(f"Path not found: {args.path}")

    path = Path(args.path)
    if path.is_file() and not args.path.endswith(".vm"):
        raise ValueError("The input file must be a VM file.")

    if not args.output:
        if path.is_file():
            args.output = str(path.with_suffix(".asm"))
        else:
            args.output = str(path / (path.name + ".asm"))


def translate_file(parser: Parser, code_writer: CodeWriter) -> None:
    while parser.has_more_lines():
        parser.advance()
        match parser.command_type():
            case CommandType.C_ARITHMETIC:
                code_writer.write_arithmetic(parser.arg1())
            case CommandType.C_PUSH | CommandType.C_POP:
                code_writer.write_push_pop(
                    parser.command_type(), parser.arg1(), parser.arg2())
            case CommandType.C_LABEL:
                code_writer.write_label(parser.arg1())
            case CommandType.C_GOTO:
                code_writer.write_goto(parser.arg1())
            case CommandType.C_IF:
                code_writer.write_if(parser.arg1())
            case CommandType.C_FUNCTION:
                code_writer.write_function(parser.arg1(), parser.arg2())
            case CommandType.C_RETURN:
                code_writer.write_return()
            case CommandType.C_CALL:
                code_writer.write_call(parser.arg1(), parser.arg2())


def main():
    args = create_parser().parse_args()
    validate_path(args)

    path = Path(args.path)
    with CodeWriter(args.output) as code_writer:
        if path.is_file():
            parser = Parser(str(path))
            code_writer.set_file_name(path.name)
            translate_file(parser, code_writer)
        else:
            code_writer.write_init()
            # 处理目录下的所有 .vm 文件
            vm_files = list(path.glob("*.vm"))
            if not vm_files:
                raise ValueError(f"No .vm files found in directory: {path}")

            sys_vm = path / "Sys.vm"
            if sys_vm in vm_files:
                vm_files.remove(sys_vm)
                parser = Parser(str(sys_vm))
                code_writer.set_file_name(sys_vm.name)
                translate_file(parser, code_writer)

            for vm_file in vm_files:
                parser = Parser(str(vm_file))
                code_writer.set_file_name(vm_file.name)
                translate_file(parser, code_writer)


if __name__ == "__main__":
    main()
