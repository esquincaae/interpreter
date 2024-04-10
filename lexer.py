from lark import Transformer, Token, Tree

class MyTransformer(Transformer):
    def __init__(self):
        self.tokens = []

    def add_token(self, token_type, token_value):
        self.tokens.append((token_type, str(token_value)))

    def start(self, items):
        for item in items:
            self._process_item(item)

    def _process_item(self, item):
        if isinstance(item, Token):
            self.add_token(item.type, str(item))
        elif isinstance(item, Tree):
            for child in item.children:
                self._process_item(child)

    def get_tokens(self):
        return self.tokens
