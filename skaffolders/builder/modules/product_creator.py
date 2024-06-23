from modules.helpers.helper import Helper

class ProductCreator:
    def __init__(self, filename):
        self.filename = filename
        self.helper = Helper(filename)

    def create_product_file(self, project_structure):
        pass
