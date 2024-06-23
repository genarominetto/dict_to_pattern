from modules.helpers.helper import Helper

class ProductFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_product_file(self, project_structure):
        pass
