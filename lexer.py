from lark import Transformer, Token

class Transformador(Transformer):
    descriptions = {
        "VAR": "palabra reservada",
        "FUNC": "palabra reservada",
        "FOR": "palabra reservada",
        "PRINT": "palabra reservada",
        "IF": "palabra reservada",
        "ELSE": "palabra reservada",
        "IDENTIFIER": "variable",
        "EQUAL": "asignacion",
        "SEMICOLON": "semicolon",
        "ent": "numero",
        "flot": "numero",
        "bool": "booleano",
        "cad": "string",
        "car": "carácter",
        "OPERATOR": "operador",
        "PM": "incremento/decremento"
    }

    def __default__(self, data, children, meta):
        results = []
        for child in children:
            if isinstance(child, Token):
                description = self.descriptions.get(child.type, "desconocido")
                results.append(f"{child.value} : {description}")
            else:
                results.extend(child)
        return results
