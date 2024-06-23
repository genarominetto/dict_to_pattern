from modules.helpers.helper import Helper

class ConcreteBuilderCreator:
    def __init__(self, filename):
        self.filename = filename
        self.helper = Helper(filename)

    def create_concrete_builder_file(self, project_structure):
        pass
