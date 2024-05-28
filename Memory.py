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
                "float": (2500, 2699),
                "string": (2700, 2999)
            },
            "temp": {
                "int": (3000, 3499),
                "float": (3500, 3999),
                "bool": (4000, 4500)
            },
        }
        self.next_address = {
            "global": {"int": 1000, "float": 1500},
            "constant": {"int": 2000, "float": 2500, "string": 2700},
            "temp": {"int": 3000, "float": 3500, "bool": 4000},
        }

    def get_next_address(self, segment, data_type):
        next_address = self.next_address[segment][data_type]
        self.next_address[segment][data_type] += 1
        return next_address

    def store(self, value, data_type="int", segment="global"):
        address = self.get_next_address(segment, data_type)
        if data_type == "int":
            self.data[address] = int(value)
        elif data_type == "float":
            self.data[address] = float(value)
        else:
            self.data[address] = value # Strip quotes for strings
        
        return address
    
    def update_value(self, value, address):
        self.data[address] = value
        return address


    def load(self, address):
        if address in self.data:
            return self.data[address]
        else:
            raise MemoryError(f"Value not found at address {address}")
            
    def get_data_by_segment(self):
        segmented_data = {segment: {} for segment in self.adresses_segments}

        for address, value in self.data.items():
            for segment, types in self.adresses_segments.items():
                for data_type, (start, end) in types.items():
                    if start <= address <= end:
                        segmented_data[segment].setdefault(data_type, {})[address] = value
                        break  # Found the segment, stop inner loops

        return segmented_data