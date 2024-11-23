import { CommandType } from "../types/types.js";
export class Parser {
    constructor(code) {
        this.instructions = this.preprocess(code);
        this.currentInstruction = "";
        this.current = 0;
    }
    preprocess(code) {
        return code
            .split("\n")
            .map((line) => line.trim())
            .filter((line) => line && !line.startsWith("//"));
    }
    hasMoreLines() {
        return this.current < this.instructions.length;
    }
    advance() {
        this.currentInstruction = this.instructions[this.current];
        this.current++;
    }
    instructionType() {
        if (this.currentInstruction.startsWith("@")) {
            return CommandType.A;
        }
        else if (this.currentInstruction.includes("=") ||
            this.currentInstruction.includes(";")) {
            return CommandType.C;
        }
        else {
            return CommandType.L;
        }
    }
    symbol() {
        if (this.instructionType() === CommandType.A) {
            return this.currentInstruction.slice(1);
        }
        else if (this.instructionType() === CommandType.L) {
            return this.currentInstruction.slice(1, -1);
        }
        else {
            throw new Error("Invalid instruction type");
        }
    }
    dest() {
        if (this.currentInstruction.includes("=")) {
            return this.currentInstruction.split("=")[0];
        }
        return "";
    }
    comp() {
        if (this.currentInstruction.includes("=")) {
            return this.currentInstruction.split("=")[1];
        }
        else if (this.currentInstruction.includes(";")) {
            return this.currentInstruction.split(";")[0];
        }
        return "";
    }
    jump() {
        if (this.currentInstruction.includes(";")) {
            return this.currentInstruction.split(";")[1];
        }
        return "";
    }
    reset() {
        this.current = 0;
        this.currentInstruction = "";
    }
}
