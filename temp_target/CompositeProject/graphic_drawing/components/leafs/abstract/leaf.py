from graphic_drawing.base.graphic import Graphic

# Leaf Base Class
class Leaf(Graphic):
    def __init__(self, name: str, size: float, is_active: bool):
        self.name: str = name
        self.size: float = size
        self.is_active: bool = is_active

    def get_all_nested_leaves(self) -> list[Graphic]:
        return [self]

    def get_structure_as_dict(self) -> dict:
        return {self.name: {}}

    def calculate_total_size(self) -> float:
        return self.size
    
    def calculate_average_size(self) -> float:
        return self.size

    def is_active(self) -> bool:
        return self.is_active

    def __str__(self, level=0, prefix=""):
        return f"{' ' * (level * 4)}{prefix}{self.name}\n"
