# modules/leaf_file_creator.py

from modules.helpers.helper import Helper

class LeafFileCreator:
    def __init__(self, filename):
        self.filename = filename
        self.helper = Helper(filename)

    def create_leaf_file(self, class_name):
        # Write the class definition
        self.helper.write_code_line(0, f'class {class_name}:')
        self.helper.write_code_line(1, 'def __init__(self):')
        self.helper.write_code_line(1, 'pass')
        self.helper.write_empty_line()
        self.helper.write_code_line(1, 'def operation(self):')
        self.helper.write_code_line(2, f'print("{class_name} operation executed.")')

        self.helper.save()

# Example usage for LeafFileCreator
if __name__ == "__main__":
    leaf_creator = LeafFileCreator("chassis.py")
    leaf_creator.create_leaf_file("Chassis")