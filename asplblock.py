# Function Block
class Block:
    def __init__(self, code):
        self.code = code

    def __repr__(self):
        return f"{'{'+self.code+'}'}"

class Nilad(Block): pass
class Monad(Block): pass
class Dyad(Block): pass
class Infiniad(Block): pass

