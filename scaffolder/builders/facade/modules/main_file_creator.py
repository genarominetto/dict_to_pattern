# modules/main_file_creator.py

from modules.helpers.helper import Helper

class MainFileCreator:
    def __init__(self, filename):
        self.filename = filename
        self.helper = Helper(filename)

    def create_main_file(self, project_structure):
        # Iterate through all root classes to write import lines
        for root_class in project_structure:
            self.helper.write_import_line(f"{root_class.lower()}.{root_class.lower()}", root_class)
        
        # Write an empty line
        self.helper.write_empty_line()
        
        # Write the if __name__ == "__main__" line
        self.helper.write_code_line(0, 'if __name__ == "__main__":')

        # Iterate through all root classes again to write instantiation and operation lines
        for root_class in project_structure:
            subcomponents = self._extract_subcomponents(project_structure[root_class])
            
            self.helper.write_code_line(1, f'my_{root_class.lower()} = {root_class}()')
            
            for component in subcomponents:
                self.helper.write_code_line(1, f'my_{root_class.lower()}.{component}.operation()')
            
            # Write an empty line after each root class instantiation block
            self.helper.write_empty_line()

        self.helper.save()

    def _extract_subcomponents(self, structure, prefix=''):
        components = []
        for key, value in structure.items():
            current_prefix = f"{prefix}.{key.lower()}" if prefix else key.lower()
            if value:
                components.extend(self._extract_subcomponents(value, current_prefix))
            else:
                components.append(current_prefix)
        return components


