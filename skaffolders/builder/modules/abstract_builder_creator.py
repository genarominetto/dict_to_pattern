from modules.helpers.helper import Helper

class AbstractBuilderCreator:
    def __init__(self, filename):
        self.filename = filename
        self.helper = Helper(filename)

    def create_abstract_builder_file(self, project_structure):
        pass
