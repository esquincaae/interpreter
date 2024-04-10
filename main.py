from lark import Lark
from interpreter import Interpreter
from lexer import Transformador

with open("grammar.lark", "r") as file:
    grammar = file.read()

#def execute_lexico(script):
#    lxr = Transformador()
#    parser = Lark(grammar, start='start', parser='lalr', transformer=lxr)
#    tree = parser.parse(script)
#    return "\n".join(result for result in tree if result)

def execute_python(script):
    print(script)
    interpreter = Interpreter()
    parser = Lark(grammar, start='start', parser='lalr', transformer=interpreter)
    parser.parse(script)
    return interpreter 