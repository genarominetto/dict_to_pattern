# modules/main_file_creator.py

from modules.helpers.helper import Helper

class MainFileCreator:
    def __init__(self, filename):
        self.filename = filename
        self.helper = Helper(filename)

    def create_main_file(self, project_structure):
        root_class = self._extract_root_class(project_structure)
        subcomponents = self._extract_subcomponents(project_structure[root_class])
        
        self.helper.write_import_line(f"{root_class.lower()}.{root_class.lower()}", root_class)
        self.helper.write_empty_line()
        self.helper.write_code_line(0, 'if __name__ == "__main__":')
        self.helper.write_code_line(1, f'my_{root_class.lower()} = {root_class}()')

        for component in subcomponents:
            self.helper.write_code_line(1, f'my_{root_class.lower()}.{component}.operation()')

        self.helper.save()

    def _extract_root_class(self, structure):
        return next(iter(structure))

    def _extract_subcomponents(self, structure, prefix=''):
        components = []
        for key, value in structure.items():
            current_prefix = f"{prefix}.{key.lower()}" if prefix else key.lower()
            if value:
                components.extend(self._extract_subcomponents(value, current_prefix))
            else:
                components.append(current_prefix)
        return components

# Example usage
if __name__ == "__main__":
    project_structure = {
        "Car": {
            "Engine": {
                "Cylinders": {},
                "Pistons": {}
            },
            "Chassis": {}
        }
    }
    
    main_creator = MainFileCreator("main.py")
    main_creator.create_main_file(project_structure)
