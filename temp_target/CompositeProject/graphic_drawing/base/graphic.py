from abc import ABC, abstractmethod

# Component
class Graphic(ABC):
    @abstractmethod
    def get_all_nested_leaves(self) -> list['Graphic']:
        pass

    @abstractmethod
    def get_structure_as_dict(self) -> dict:
        pass

    @abstractmethod
    def calculate_total_size(self) -> float:
        pass

    @abstractmethod
    def calculate_average_size(self) -> float:
        pass

    @abstractmethod
    def is_active(self) -> bool:
        pass
