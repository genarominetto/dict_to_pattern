from graphic_drawing.components.leafs.abstract.leaf import Leaf

# Leaf 2
class Square(Leaf):
    def __init__(self, name: str, size: float, is_active: bool):
        super().__init__(name, size, is_active)
