from abc import ABC, abstractmethod
from modules.helpers.helper import Helper

class ComponentFileBuilder(ABC):
    def __init__(self, filename, project_structure, root_module=None):
        self.filename = filename
        self.project_structure = project_structure
        self.root_module = root_module
        self.helper = Helper(filename, root_module)

    def get_component_file(self):
        return self.helper.save()
