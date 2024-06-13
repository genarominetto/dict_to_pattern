# modules/test_file_creator.py

from modules.helpers.helper import Helper

class TestFileCreator:
    def __init__(self, filename):
        self.filename = filename
        self.helper = Helper(filename)

    def create_test_file(self, root_class, subcomponents):
        self.helper.write_import_line("pytest", "")
        self.helper.write_import_line(f"{root_class.lower()}.{root_class.lower()}", root_class)
        
        self.helper.write_empty_line()
        self.helper.write_code_line(0, "@pytest.fixture")
        self.helper.write_code_line(0, f"def {root_class.lower()}():")
        self.helper.write_code_line(1, f"return {root_class}()")
        
        for component in subcomponents:
            method_name = component.replace(".", "_").lower()
            self.helper.write_empty_line()
            self.helper.write_code_line(0, f"def test_{method_name}_operation({root_class.lower()}):")
            self.helper.write_code_line(1, f"{root_class.lower()}.{component}.operation()")
            self.helper.write_code_line(1, "# Add assertions or checks if needed")
        
        self.helper.save()
