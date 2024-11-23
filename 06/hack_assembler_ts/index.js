import { Parser } from "./parser/Parser.js";
import { translate } from "./code/Code.js";
import symbolTable from "./SymbolTable/SymbolTable.js";
import { readFileSync, writeFileSync } from "fs";
import path from "path";
import { CommandType } from "./types/types.js";
const isNumeric = (str) => {
    return !isNaN(parseInt(str, 10)) && !isNaN(parseFloat(str));
};
const filePath = path.resolve(process.argv[2]);
const outputPath = path.resolve(path.dirname(filePath), path.basename(filePath).replace(".asm", ".hack"));
const code = readFileSync(filePath, "utf-8");
const parser = new Parser(code);
const binary = [];
const firstPass = () => {
    let currentAddress = 0;
    while (parser.hasMoreLines()) {
        parser.advance();
        if (parser.instructionType() === CommandType.L) {
            symbolTable.addEntry(parser.symbol(), currentAddress);
        }
        else {
            currentAddress++;
        }
    }
};
const secondPass = () => {
    while (parser.hasMoreLines()) {
        parser.advance();
        if (parser.instructionType() === CommandType.A) {
            const s = parser.symbol();
            if (!isNumeric(s) && !symbolTable.contains(s)) {
                symbolTable.addEntry(s, symbolTable.getNextAddress());
            }
        }
    }
};
firstPass();
parser.reset();
secondPass();
parser.reset();
while (parser.hasMoreLines()) {
    parser.advance();
    const instruction = translate(parser);
    if (instruction) {
        binary.push(instruction);
    }
}
writeFileSync(outputPath, binary.join("\n"));
