from lark import Transformer, Token, Tree

class Interpreter(Transformer):
    def __init__(self):
        super().__init__()
        self.output = ""  # Código Python generado

    def var_decl(self, items):
        # Se asume que el nombre de la variable es siempre un Token y el valor puede ser un Token o un Tree
        var_type, var_name, var_value = items[1], str(items[2]), items[4]
        if isinstance(var_value, Token):
            value = var_value.value
        elif isinstance(var_value, Tree):
            value = self.process_tree(var_value)
            
        self.output += f'{var_name} = {value}\n'

    def statement(self, items):
        action, expr = items[0], items[2]
        if action == "imprimir":
            if isinstance(expr, Token):
                if expr.type == 'STRING':
                    # Directamente imprimir el string, quitando las comillas
                    self.output += f'print({expr.value})\n'
                else:
                    # Si es un token pero no un string, se imprime directamente su valor
                    self.output += f'print({expr})\n'
            elif isinstance(expr, Tree):
                # Procesar la estructura Tree y generar código Python correspondiente
                expr_value = self.process_tree(expr)
                self.output += f'print({expr_value})\n'

    def process_tree(self, tree):
        # Diferentes ramas para cada tipo de nodo basado en su etiqueta
        if tree.data == 'var_decl':
            # Procesamiento para declaraciones de variable
            _, var_type, identifier, _, value, _ = tree.children
            var_name = identifier.value
            var_value = self.process_node(value)
            return f'{var_name} = {var_value}'
        elif tree.data == 'int':
            # Procesamiento para enteros
            return tree.children[0].value
        elif tree.data == 'float':
            # Procesamiento para flotantes
            return tree.children[0].value
        elif tree.data == 'boolean':
            # Asegura que se traduce correctamente de acuerdo al valor explícito
            if tree.children[0].value == 'verdadero':
                return 'True'
            elif tree.children[0].value == 'falso':
                return 'False'
            else:
                # Lanza un error si el valor no es ni 'verdadero' ni 'falso'
                raise Exception(f"Valor booleano no reconocido: {tree.children[0].value}")
        elif tree.data == 'string':
            # Para nodos de cadena, se extrae el texto entre comillas
            # Asumiendo que el primer hijo es el token de la cadena
            return tree.children[0].value
        elif tree.data == 'char':
            # Para nodos de carácter, se extrae el carácter entre comillas simples
            # Asumiendo que el primer hijo es el token del carácter
            char_value = tree.children[0].value
            # Verifica y procesa adecuadamente el carácter (quitar comillas y manejar escapes si es necesario)
            return repr(char_value)[1:-1]  # quita comillas adicionales en la representación Python
        else:
            raise Exception(f"No se puede procesar el nodo Tree de tipo: {tree.data}")

    def process_node(self, node):
        # Decide si el nodo es un Tree o un Token y lo procesa acordemente
        if isinstance(node, Tree):
            return self.process_tree(node)
        elif isinstance(node, Token):
            # Procesamiento directo para Tokens
            return node.value
        else:
            raise Exception(f"Tipo de nodo no reconocido: {type(node)}")
