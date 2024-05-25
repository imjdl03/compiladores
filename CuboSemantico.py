# Cubo semantico definido como un diccionario anidado. La primera clave representa
# el primer operador, la segunda clave anidada, el segundo operador y el tercer nivel
# de anidación representa las opciones del tipo de dato resultante.
class CuboSemantico:
    def __init__(self):
        self.cuboSemantico = {
            # asignación
            '=': {
                'int': {
                    'int': True,
                    'float': False 
                },
                'float': {
                    'int': True,
                    'float': True
                },
                'string': {
                    'string': True
                }
                # ... (otros tipos de datos) ...
            },
            # suma
            '+': {
                'int': {
                    'int': 'int',
                    'float': 'float'
                },
                'float': {
                    'int': 'float',
                    'float': 'float'
                }
            },
            # resta
            '-': {
                'int': {
                    'int': 'int',
                    'float': 'float'
                },
                'float': {
                    'int': 'float',
                    'float': 'float'
                }
            },
            # multiplicacion
            '*': {
                'int': {
                    'int': 'int',
                    'float': 'float'
                },
                'float': {
                    'int': 'float',
                    'float': 'float'
                }
            },
            # division
            '/': {
                'int': {
                    'int': 'float',
                    'float': 'float'
                },
                'float': {
                    'int': 'float',
                    'float': 'float'
                }
            },
            # mayor que
            '>': {
                'int': {
                    'int': 'bool',
                    'float': 'bool'
                },
                'float': {
                    'int': 'bool',
                    'float': 'bool'
                }
            },
            # menor que
            '<': {
                'int': {
                    'int': 'bool',
                    'float': 'bool'
                },
                'float': {
                    'int': 'bool',
                    'float': 'bool'
                }
            },
            # mayor o igual que
            '>=': {
                'int': {
                    'int': 'bool',
                    'float': 'bool'
                },
                'float': {
                    'int': 'bool',
                    'float': 'bool'
                }
            },
            # menor o igual que
            '<=': { 
                'int': {
                    'int': 'bool',
                    'float': 'bool'
                },
                'float': {
                    'int': 'bool',
                    'float': 'bool'
                }
            },
            # igual que
            '==': {
                'int': {
                    'int': 'bool',
                    'float': 'bool'
                },
                'float': {
                    'int': 'bool',
                    'float': 'bool'
                },
                'string': {
                    'string': 'bool'
                },
                'bool': {
                    'bool': 'bool'
                }
            },
            # diferente que
            '!=': {
                'int': {
                    'int': 'bool',
                    'float': 'bool'
                },
                'float': {
                    'int': 'bool',
                    'float': 'bool'
                },
                'string': {
                    'string': 'bool'
                },
                'bool': {
                    'bool': 'bool'
                }
            }
        }

    def check_operation(self, operator, typeIzq, typeDer):
        if operator in self.cuboSemantico:
            if typeIzq in self.cuboSemantico[operator]:
                if typeDer in self.cuboSemantico[operator][typeIzq]:
                    return self.cuboSemantico[operator][typeIzq][typeDer]
        return None  # Operación no válida
    
    def check_assignment(self, left_type, right_type):
        return self.cuboSemantico['='][left_type][right_type]