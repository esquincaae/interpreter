from interpreter import get_parser, Interpreter

# Definir una función para ejecutar el script
def execute(script):
    parser = get_parser()
    tree = parser.parse(script)
    interpreter = Interpreter()
    interpreter.transform(tree)
    output = '\n'.join(interpreter.output)
    return output

# Testear el intérprete con un script básico
script = """
var cad x = "Hello, world!";
imprimir(x);
"""

