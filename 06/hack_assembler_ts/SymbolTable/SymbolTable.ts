class SymbolTable {
  private static readonly PREDEFINED_SYMBOLS: Record<string, number> = {
    SP: 0,
    LCL: 1,
    ARG: 2,
    THIS: 3,
    THAT: 4,
    SCREEN: 16384,
    KBD: 24576,
  } as const;
  private table: Map<string, number>;
  private nextAddress: number;

  constructor() {
    this.table = new Map(Object.entries(SymbolTable.PREDEFINED_SYMBOLS));
    for (let i = 0; i < 16; ++i) {
      this.table.set(`R${i}`, i);
    }
    this.nextAddress = 16;
  }

  addEntry(symbol: string, address: number): void {
    this.table.set(symbol, address);
  }

  contains(symbol: string): boolean {
    return this.table.has(symbol);
  }

  getAddress(symbol: string): number {
    const address = this.table.get(symbol);
    if (address === undefined) {
      throw new Error(`Symbol ${symbol} not found`);
    }
    return address;
  }

  getNextAddress(): number {
    return this.nextAddress++;
  }
}

const symbolTable = new SymbolTable();
export default symbolTable;
