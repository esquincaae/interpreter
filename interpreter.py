from lark import Lark, Transformer

# Importar la gramática desde el archivo externo
with open("grammar.lark") as file:
    grammar = file.read()

class Interpreter(Transformer):
    def __init__(self):
        self.variables = {}  # Almacena valores y tipos de variables
        self.declared_vars = set()  # Almacena nombres de variables declaradas

    def var_decl(self, items):
        _, var_type, var_name, _, value, _ = items
        var_name_str = str(var_name)

        # Registrar la variable como declarada
        self.declared_vars.add(var_name_str)

        # Asignar valor inicial verificando el tipo
        var_value = value.children[0]
        self.check_type_and_assign(var_type, var_name_str, var_value)

    def check_type_and_assign(self, var_type, var_name, var_value):
        # Verificar el tipo y asignar el valor
        if var_type == "ent" and not isinstance(var_value, int):
            raise TypeError(f"Tipo incorrecto para la variable '{var_name}'. Esperaba un entero.")
        elif var_type == "flot" and not isinstance(var_value, float):
            raise TypeError(f"Tipo incorrecto para la variable '{var_name}'. Esperaba un flotante.")
        elif var_type == "bool" and not isinstance(var_value, bool):
            raise TypeError(f"Tipo incorrecto para la variable '{var_name}'. Esperaba un booleano.")
        elif var_type == "cad" and not isinstance(var_value, str):
            raise TypeError(f"Tipo incorrecto para la variable '{var_name}'. Esperaba una cadena.")
        elif var_type == "car" and (not isinstance(var_value, str) or len(var_value) != 1):
            raise TypeError(f"Tipo incorrecto para la variable '{var_name}'. Esperaba un carácter.")
        
        # Asignar el valor
        self.variables[var_name] = var_value

    def print(self, items):
        _, value, _ = items
        # Verificar si el identificador ha sido declarado
        if value.data == 'identifier':
            var_name = str(value.children[0])
            if var_name not in self.declared_vars:
                raise NameError(f"Variable '{var_name}' no declarada.")
            self.output.append(self.variables.get(var_name, ''))
        else:
            self.output.append(value.children[0].strip('"'))

    def statement(self, items):
        if items[0].data == 'print':
            self.print(items[0])


# Función para crear y retornar el parser
def get_parser():
    return Lark(grammar, start='start', parser='lalr')
