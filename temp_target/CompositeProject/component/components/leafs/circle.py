from component.components.leafs.abstract.leaf import Leaf

# Concrete class for a circle
class Circle(Leaf):
    def __init__(self, *, name: str, size: float, is_active: bool):
        super().__init__(name=name, size=size, is_active=is_active)
