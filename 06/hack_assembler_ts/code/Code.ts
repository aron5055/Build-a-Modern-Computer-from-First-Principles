import { Parser } from "../parser/Parser.js";
import { CommandType } from "../types/types.js";
import symbolTable from "../SymbolTable/SymbolTable.js";

const destMap: Record<string, string> = {
  "": "000",
  M: "001",
  D: "010",
  MD: "011",
  A: "100",
  AM: "101",
  AD: "110",
  AMD: "111",
};

const compMap: Record<string, string> = {
  "0": "0101010",
  "1": "0111111",
  "-1": "0111010",
  D: "0001100",
  A: "0110000",
  "!D": "0001101",
  "!A": "0110001",
  "-D": "0001111",
  "-A": "0110011",
  "D+1": "0011111",
  "A+1": "0110111",
  "D-1": "0001110",
  "A-1": "0110010",
  "D+A": "0000010",
  "D-A": "0010011",
  "A-D": "0000111",
  "D&A": "0000000",
  "D|A": "0010101",
  M: "1110000",
  "!M": "1110001",
  "-M": "1110011",
  "M+1": "1110111",
  "M-1": "1110010",
  "D+M": "1000010",
  "D-M": "1010011",
  "M-D": "1000111",
  "D&M": "1000000",
  "D|M": "1010101",
};

const jumpMap: Record<string, string> = {
  "": "000",
  JGT: "001",
  JEQ: "010",
  JGE: "011",
  JLT: "100",
  JNE: "101",
  JLE: "110",
  JMP: "111",
};

const dest = (mnemonic: string): string => {
  return destMap[mnemonic] ?? "000";
};

const comp = (mnemonic: string): string => {
  return compMap[mnemonic] ?? "0000000";
};

const jump = (mnemonic: string): string => {
  return jumpMap[mnemonic] ?? "000";
};

const translateA = (symbol: string): string => {
  try {
    const address = symbolTable.getAddress(symbol);
    return `0${address.toString(2).padStart(15, "0")}`;
  } catch (e) {
    return `0${parseInt(symbol).toString(2).padStart(15, "0")}`;
  }
};

const translateC = (d: string, c: string, j: string): string => {
  return `111${comp(c)}${dest(d)}${jump(j)}`;
};

export const translate = (parser: Parser): string => {
  switch (parser.instructionType()) {
    case CommandType.A:
      return translateA(parser.symbol());
    case CommandType.C:
      return translateC(parser.dest(), parser.comp(), parser.jump());
    default:
      return "";
  }
};
