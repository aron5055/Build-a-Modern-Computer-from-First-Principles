import { CommandType } from "../types/types.js";

export class Parser {
  private instructions: string[];
  private currentInstruction: string;
  private current: number;

  constructor(code: string) {
    this.instructions = this.preprocess(code);
    this.currentInstruction = "";
    this.current = 0;
  }

  private preprocess(code: string): string[] {
    return code
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line && !line.startsWith("//"));
  }

  hasMoreLines(): boolean {
    return this.current < this.instructions.length;
  }

  advance(): void {
    this.currentInstruction = this.instructions[this.current];
    this.current++;
  }

  instructionType(): CommandType {
    if (this.currentInstruction.startsWith("@")) {
      return CommandType.A;
    } else if (
      this.currentInstruction.includes("=") ||
      this.currentInstruction.includes(";")
    ) {
      return CommandType.C;
    } else {
      return CommandType.L;
    }
  }

  symbol(): string {
    if (this.instructionType() === CommandType.A) {
      return this.currentInstruction.slice(1);
    } else if (this.instructionType() === CommandType.L) {
      return this.currentInstruction.slice(1, -1);
    } else {
      throw new Error("Invalid instruction type");
    }
  }

  dest(): string {
    if (this.currentInstruction.includes("=")) {
      return this.currentInstruction.split("=")[0];
    }
    return "";
  }

  comp(): string {
    if (this.currentInstruction.includes("=")) {
      return this.currentInstruction.split("=")[1];
    } else if (this.currentInstruction.includes(";")) {
      return this.currentInstruction.split(";")[0];
    }
    return "";
  }

  jump(): string {
    if (this.currentInstruction.includes(";")) {
      return this.currentInstruction.split(";")[1];
    }
    return "";
  }

  reset(): void {
    this.current = 0;
    this.currentInstruction = "";
  }
}
