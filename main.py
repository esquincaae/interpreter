#main.py
from lark import Lark
from interpreter import Interpreter
from lexer import MyTransformer

with open("grammar.lark", "r") as file:
    grammar = file.read()

def execute_python(script):
    interpreter = Interpreter()
    parser = Lark(grammar, start='start', parser='lalr', transformer=interpreter)
    parser.parse(script)
    return interpreter 

def execute_lexico(entrada):
    try:
        lexer_parser = Lark(grammar, parser='lalr')
        tree = lexer_parser.parse(entrada)
        transformer = MyTransformer()
        transformer.transform(tree)
        
        return transformer.get_tokens()

    except Exception as e:
        print(e)
        raise e