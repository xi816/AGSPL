# Function Block
class CodeBlock:
    def __init__(self, type, code):
        self.type = type
        self.code = code

    def __repr__(self):
        return f"{self.type} {'{'+self.code+'}'}"