#interpreter.py
from lark import Transformer, Token, Tree

class Interpreter(Transformer):
    def __init__(self):
        super().__init__()
        self.output = ""
        self.variables = {}

    def var_decl(self, items):
            var_type, var_name, var_value = items[1], str(items[2]), items[4]
            if isinstance(var_value, Token):
                value = var_value.value
            elif isinstance(var_value, Tree):
                value = self.process_tree(var_value)

            if isinstance(var_type, Token):
                vtype = var_type.value
            elif isinstance(var_type, Tree):
                vtype = self.process_tree(var_type)

            if vtype == 'ent' and not isinstance(int(value), int):
                raise SyntaxError(f"Error de tipo: se esperaba un entero, se obtuvo {value}")
            elif vtype == 'flot' and not isinstance(float(value), float):
                raise SyntaxError(f"Error de tipo: se esperaba un flotante, se obtuvo {value}")
            elif vtype == 'bool':
                if value != 'True' and value != 'False':
                    raise SyntaxError(f"Error de tipo: se esperaba un booleano, se obtuvo {value}")
            elif vtype == 'cad' and not (isinstance(value, str) and value.startswith('"') and value.endswith('"')):
                raise SyntaxError(f"Error de tipo: se esperaba una cadena, se obtuvo {value}")
            elif vtype == 'car' and not (isinstance(value, str) and len(value) == 3):
                raise SyntaxError(f"Error de tipo: se esperaba un carácter, se obtuvo {value}")

            self.variables = {var_name:value}
            self.output += f'{var_name} = {value}\n'
        
        
 
    def for_decl(self, items):
        if items[2] is not None:
            self.var_decl(items[2])

        condition_expression = items[3] if isinstance(items[3], str) else ''
        increment_expression = items[5] if isinstance(items[5], str) else ''

        range_expression = condition_expression.split('<')[1].strip()  # Extraer la parte derecha de la condición
        range_expression = range_expression[:-1] if range_expression.endswith(';') else range_expression  # Eliminar el punto y coma si lo hay

        self.output += f'for i in range({range_expression}):\n'
        print("Debug: Cuerpo del bucle:")
        if isinstance(items[8], Tree):
            for child in items[8].children:
                self.process_tree(child)
        else:
            print("No hay instrucciones dentro del bucle.")
            self.output += '    pass\n'
        print("Fin del bucle for")




        
    print("Debug for_decl - End")
    def condition(self, items):
        # Este es un esquema básico; deberás adaptarlo a tu lógica específica.
        if len(items) == 3:
            identifier = items[0].value
            operator = items[1].value
            value = self.process_tree(items[2])  # Asume que items[2] es un Tree.
            return f"{identifier} {operator} {value}"
        return ""

    def increment(self, items):
        # Adaptar según cómo desees procesar los incrementos.
        if len(items) == 2:
            identifier = items[0].value
            operation = items[1].value  # ++ o --
            return f"{identifier} {operation}"
        return ""


    def statement(self, items):
        action, expr = items[0], items[2]
        if action == "imprimir":
            if isinstance(expr, Token):
                if expr.type == 'STRING':
                    self.output += f'print({expr.value})\n'
                else:
                    self.output += f'print({expr})\n'
            elif isinstance(expr, Tree):
                expr_value = self.process_tree(expr)
                self.output += f'print({expr_value})\n'

    def process_tree(self, tree):
        if tree.data == 'var_decl':
            _, type_node, identifier, _, value, _ = tree.children
            var_type = type_node.value
            var_name = identifier.value
            var_value = self.process_node(value)
            return f'{var_name} = {var_value}'
        elif tree.data == 'int':
            if tree.children[0].value.isdigit():
                return tree.children[0].value
            else:
                raise Exception(f"el tipo no coincide con el valor:  {tree.data}:{tree.children[0].value}")
        elif tree.data == 'float':
            return tree.children[0].value
        elif tree.data == 'boolean':
            if tree.children[0].value == 'verdadero':
                return 'True'
            elif tree.children[0].value == 'falso':
                return 'False'
            else:
                raise Exception(f"Valor booleano no reconocido: {tree.children[0].value}")
        elif tree.data == 'string':
            return tree.children[0].value
        elif tree.data == 'char':
            char_value = tree.children[0].value
            return repr(char_value)[1:-1]
        else:
            raise Exception(f"No se puede procesar el nodo Tree de tipo: {tree.data}")

    def process_node(self, node):
        if isinstance(node, Tree):
            return self.process_tree(node)
        elif isinstance(node, Token):
            return node.value
        else:
            raise Exception(f"Tipo de nodo no reconocido: {type(node)}")
