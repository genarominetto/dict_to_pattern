from modules.helpers.helper import Helper

class TestFileCreator:
    def __init__(self, filename):
        self.filename = filename
        self.helper = Helper(filename)

    def create_test_file(self, project_structure):
        pass
