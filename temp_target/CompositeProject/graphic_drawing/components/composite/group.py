from graphic_drawing.base.graphic import Graphic
from graphic_drawing.components.leafs.abstract.leaf import Leaf

# Composite
class Group(Graphic):
    def __init__(self, name: str):
        self.name: str = name
        self.graphics: list[Graphic] = []

    def add(self, graphic: Graphic):
        self.graphics.append(graphic)

    def remove(self, graphic: Graphic):
        self.graphics.remove(graphic)

    def get_all_nested_leaves(self) -> list[Graphic]:
        leaves = []
        for graphic in self.graphics:
            leaves.extend(graphic.get_all_nested_leaves())
        return leaves

    def get_structure_as_dict(self) -> dict:
        structure = {self.name: []}
        for graphic in self.graphics:
            structure[self.name].append(graphic.get_structure_as_dict())
        return structure

    def calculate_total_size(self) -> float:
        total_size = 0
        for graphic in self.graphics:
            total_size += graphic.calculate_total_size()
        return total_size

    def calculate_average_size(self) -> tuple[float, int]:
        total_size = 0
        leaf_count = 0
        for graphic in self.graphics:
            size, count = graphic.calculate_average_size()
            total_size += size
            leaf_count += count
        return total_size, leaf_count

    def is_active(self) -> bool:
        for graphic in self.graphics:
            if isinstance(graphic, Leaf):
                if graphic.is_active:
                    return True
            elif isinstance(graphic, Group):
                if graphic.is_active():
                    return True
        return False

    def __str__(self, level=0, prefix=""):
        result = f"{' ' * (level * 4)}{prefix}{self.name}/\n"
        for i, graphic in enumerate(self.graphics):
            new_prefix = "├── " if i < len(self.graphics) - 1 else "└── "
            result += graphic.__str__(level + 1, new_prefix)
        return result
