from graphic_drawing.components.leafs.abstract.leaf import Leaf

# Leaf 1
class Circle(Leaf):
    def __init__(self, name: str, size: float, is_active: bool):
        super().__init__(name, size, is_active)
