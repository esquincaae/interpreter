from lark import Lark
from interpreter import Interpreter

with open("grammar.lark", "r") as file:
    grammar = file.read()

def execute(script):
    interpreter = Interpreter()
    parser = Lark(grammar, start='start', parser='lalr', transformer=interpreter)
    tree = parser.parse(script)
    print(tree.pretty())
    return interpreter 