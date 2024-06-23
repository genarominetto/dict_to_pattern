from modules.helpers.helper import Helper

class AbstractBuilderFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_abstract_builder_file(self, project_structure):
        pass
