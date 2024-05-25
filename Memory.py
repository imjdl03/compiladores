class Memory:
    def __init__(self):
        self.data = {}
        self.adresses_segments = {
            "global": {
                "int": (1000, 1499),
                "float": (1500, 1999),
            },
            "constant": {
                "int": (2000, 2499),
                "float": (2500, 2999),
            },
            "temp": {
                "int": (3000, 3499),
                "float": (3500, 3999),
            },
        }
        self.next_address = {
            "global": {"int": 1000, "float": 1500},
            "constant": {"int": 2000, "float": 2500},
            "temp": {"int": 3000, "float": 3500},
        }

    def get_next_address(self, segment, data_type):
        next_address = self.next_address[segment][data_type]
        self.next_address[segment][data_type] += 1
        return next_address

    # def _validate_address(self, address, segment):
    #     start, end = self.segments[segment]
    #     if not (start <= address <= end):
    #         raise MemoryError(f"Invalid address {address} for segment {segment}")

    # def _validate_type(self, value, data_type):
    #     if not isinstance(value, self.types[data_type]):
    #         raise TypeError(f"Invalid type for value {value}, expected {data_type}")

    def store(self, value, data_type="int", segment="global"):
        address = self.get_next_address(segment, data_type)
        self.data[address] = value
        return address
    
    def update_value(self, value, address):
        self.data[address] = value
        return address


    def load(self, address):
        if address in self.data:
            return self.data[address]
        else:
            raise MemoryError(f"Value not found at address {address}")