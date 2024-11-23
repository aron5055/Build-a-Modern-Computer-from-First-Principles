class SymbolTable {
    constructor() {
        this.table = new Map(Object.entries(SymbolTable.PREDEFINED_SYMBOLS));
        for (let i = 0; i < 16; ++i) {
            this.table.set(`R${i}`, i);
        }
        this.nextAddress = 16;
    }
    addEntry(symbol, address) {
        this.table.set(symbol, address);
    }
    contains(symbol) {
        return this.table.has(symbol);
    }
    getAddress(symbol) {
        const address = this.table.get(symbol);
        if (address === undefined) {
            throw new Error(`Symbol ${symbol} not found`);
        }
        return address;
    }
    getNextAddress() {
        return this.nextAddress++;
    }
}
SymbolTable.PREDEFINED_SYMBOLS = {
    SP: 0,
    LCL: 1,
    ARG: 2,
    THIS: 3,
    THAT: 4,
    SCREEN: 16384,
    KBD: 24576,
};
const symbolTable = new SymbolTable();
export default symbolTable;
