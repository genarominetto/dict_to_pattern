from dir.sub_dir.graphic.components.leaves.abstract.leaf import Leaf

class Square(Leaf):
    def __init__(self, *, name: str, size: int, is_active: bool):
        super().__init__(name=name, size=size, is_active=is_active)