from lark import Lark
from interpreter import Interpreter

with open("grammar.lark", "r") as file:
    grammar = file.read()

def execute(script):
    interpreter = Interpreter()
    parser = Lark(grammar, start='start', parser='lalr', transformer=interpreter)
    parser.parse(script)
    return interpreter.variables
    #respuesta = '\n'.join(interpreter.output)
    #return respuesta