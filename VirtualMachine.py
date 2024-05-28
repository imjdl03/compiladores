from collections import namedtuple
import pickle
from Cuadruplo import Cuadruplo
from Memory import Memory


class VirtualMachine:
    def __init__(self, filename="test_file.obj"):
        self.cuadruplos, self.memory = self.load_from_obj("test_file.obj")
        self.ip = 0  
        self.jump_stack = []

    def load_from_obj(self, filename):
        with open(filename, "rb") as f:
            data = pickle.load(f)
        cuadruplos = data["quads"]
        memory = Memory()
        memory.data = data["memory"]  # Restore the data dictionary

        for index, cuadruplo in enumerate(cuadruplos):
            print(index+1, ".- ", cuadruplo.operador, cuadruplo.operandoIzq, cuadruplo.operandoDer, cuadruplo.resultado)
        return cuadruplos, memory
    

    def run(self):
        while 0 <= self.ip < len(self.cuadruplos):
            cuad = self.cuadruplos[self.ip]
            self.execute(cuad)
            self.ip += 1

        print("memory execution -> ", self.memory.get_data_by_segment())

    def execute(self, cuad):
        op, left_addr, right_addr, result_addr = (
            cuad.operador,
            cuad.operandoIzq,
            cuad.operandoDer,
            cuad.resultado,
        )

        left_val = self.memory.load(left_addr) if left_addr is not None else None
        right_val = self.memory.load(right_addr) if right_addr is not None else None
        # print(left_addr, op, right_addr)


        match op:
            case 1:  # "+"
                result = left_val + right_val # type: ignore
            case 2:  # "-"
                result = left_val - right_val# type: ignore
            case 3:  # "*"
                result = left_val * right_val# type: ignore
            case 4:  # "/"
                if right_val == 0:
                    raise ZeroDivisionError("Division by zero")
                result = left_val / right_val# type: ignore
            case 5:  # "=" (Assignment)
                if result_addr is None:
                    raise ValueError("Assignment operation requires a result address")
                self.memory.update_value(left_val, result_addr)
                return  # No need to calculate a 'result'
            case 6:  # "<"
                result = left_val <  right_val# type: ignore
            case 7:  # ">"
                result = left_val >  right_val# type: ignore
            case 8:  # "<="
                result = left_val <=  right_val# type: ignore
            case 9:  # ">="
                result = left_val >=  right_val# type: ignore
            case 10:  # "=="
                result = left_val ==  right_val# type: ignore
            case 11:  # "!="
                result = left_val !=  right_val# type: ignore
            case 12:  # "GOTO"
                self.ip = result_addr - 2
                return
            case 13:  # "GOTOF"
                if not left_val:
                    self.ip = result_addr - 2
                return
            case 14:  # "GOTOV"
                if left_val:
                    self.ip = result_addr - 2
                return
            case 15:  # "PRINT"
                print(self.memory.load(result_addr) ) # Assuming you want to print the left operand
                return  # No need to store a result
            case _:
                raise ValueError(f"Unknown operation code: {op}")

        if result_addr is not None:
            self.memory.update_value(result, result_addr)

