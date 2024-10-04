from typing import Callable, List, Optional, Any, Dict, Union
from graphic.abstract.graphic import Graphic

class Leaf(Graphic):
    def __init__(self, name: str, size: int, is_active: bool):
        self.name = name

        self.size = size

        self.is_active = is_active

        super().__init__(name=self.name)

    def get_structure_as_dict(self) -> Dict:
        return {self.name: {}}

    def __str__(self, level=0) -> str:
        indent = "    " * level

        properties_list = [

            f"size: {{self.size}}",

            f"is_active: {{self.is_active}}"

        ]
        properties_str = "(" + ", ".join(properties_list) + ")"

        return f"{indent}{self.name}{properties_str}"

    def __hash__(self):
        return super().__hash__()

    def is_composite(self) -> bool:
        return False

    def is_leaf(self) -> bool:
        return True


    def any_active(self) -> bool:
        return self.is_active


    def get_components_recursively(
        self,
        condition_func: Optional[Callable[['Graphic', Any], bool]] = None,
        condition_args: Union[tuple, Any] = ()
    ) -> List['Graphic']:
        if condition_func:
            if condition_func(self, *self._ensure_tuple(condition_args)):
                return [self]
            else:
                return []
        return [self]

    def remove_components_recursively(
        self,
        condition_func: Callable[['Graphic', Any], bool],
        condition_args: Union[tuple, Any] = ()
    ) -> List['Graphic']:
        return []

    def execute_operation_recursively(
        self,
        operation_func: Callable[['Graphic', Any], Any],
        operation_args: Union[tuple, Any] = (),
        condition_func: Optional[Callable[['Graphic', Any], bool]] = None,
        condition_args: Union[tuple, Any] = (),
    ) -> List[Any]:
        operation_args = self._ensure_tuple(operation_args)
        condition_args = self._ensure_tuple(condition_args)
        results = []
        if condition_func is None or condition_func(self, *condition_args):
            result = operation_func(self, *operation_args)
            results.append(result)
        return results

    def calculate_depth(self) -> int:
        return 1  # A leaf has a depth of 1

    def add(self, component: 'Graphic') -> None:
        raise NotImplementedError("Cannot add components to a leaf.")

    def remove(self, component: 'Graphic') -> None:
        raise NotImplementedError("Cannot remove components from a leaf.")