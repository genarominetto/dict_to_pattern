from modules.helpers.helper import Helper

class CompositeFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_composite_file(self, project_structure):
        pass
