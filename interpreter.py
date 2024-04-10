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

        print(f"{vtype} : {value}")    

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

        self.output += f'{var_name} = {value}\n'

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
