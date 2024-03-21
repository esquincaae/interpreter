from lark import Transformer, Token, Tree

class Interpreter(Transformer):
    def __init__(self):
        self.variables = {}
        self.declared_vars = set()

    def var_decl(self, items):
        var_keyword, var_type_tree, var_name_token, equal_token, value_tree, semicolon_token = items
        var_name_str = var_name_token.value
        if var_name_str in self.declared_vars:
            raise Exception(f"La variable '{var_name_str}' ya ha sido declarada.")
        self.declared_vars.add(var_name_str)
        if not value_tree.children:
            raise Exception("Estructura del árbol de valor vacía o incorrecta.")
        value_token = value_tree.children[0]
        self.variables[var_name_str] = int(value_token.value)

    def _extract_text(self, node):
        if isinstance(node, Token):
            return node.value
        elif isinstance(node, Tree):
            if not node.children:
                raise Exception("Nodo de árbol sin hijos.")
            return self._extract_text(node.children[0])
        else:
            raise Exception("Nodo no reconocido durante la extracción de texto.")
