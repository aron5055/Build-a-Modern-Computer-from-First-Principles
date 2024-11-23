class SymbolTable:
    NEXT_ADDRESS = 16

    def __init__(self):
        self.table = {
            'SP': 0,
            'LCL': 1,
            'ARG': 2,
            'THIS': 3,
            'THAT': 4,
            'SCREEN': 16384,
            'KBD': 24576,
        }

        for i in range(self.NEXT_ADDRESS):
            self.table[f'R{i}'] = i

        self.next_address = self.NEXT_ADDRESS

    def add_entry(self, symbol: str, address: int):
        self.table[symbol] = address

    def contains(self, symbol: str) -> bool:
        return symbol in self.table

    def get_address(self, symbol: str) -> int:
        return self.table[symbol]

    def add_new_variable(self, symbol: str):
        self.add_entry(symbol, self.next_address)
        self.next_address += 1


symbol_table = SymbolTable()
