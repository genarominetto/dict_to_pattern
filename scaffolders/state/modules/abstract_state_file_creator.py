from modules.helpers.helper import Helper

class AbstractStateFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_abstract_state_file(self, project_structure):
        properties = project_structure.get("properties", [])
        methods = project_structure.get("methods", [])
        state_transitions = project_structure.get("state_transitions", {})

        # Write the class definition for the abstract state
        self.helper.write_code_line(0, 'class State:')
        self.helper.write_code_line(1, 'def __init__(self):')
        self.helper.write_code_line(2, 'self.name = None')

        # Initialize properties dynamically
        for prop in properties:
            self.helper.write_code_line(2, f'self.{prop} = None')

        self.helper.write_empty_line()

        # Define state transition methods
        for state in state_transitions.keys():
            method_name = f'set_state_to_{self.helper.convert_to_snake_case(state)}'
            self.helper.write_code_line(1, f'def {method_name}(self, context):')
            self.helper.write_code_line(2, 'raise NotImplementedError')
            self.helper.write_empty_line()

        # Define additional methods
        for method in methods:
            self.helper.write_code_line(1, f'def {method}(self):')
            self.helper.write_code_line(2, 'raise NotImplementedError')
            self.helper.write_empty_line()

        # Define the __str__ method to display state information
        self.helper.write_code_line(1, 'def __str__(self):')
        
        # Construct the string for __str__ method in the required format
        str_content = 'f"State: {self.name}'
        for prop in properties:
            str_content += f'\\n- {prop.replace("_", " ").capitalize()}: {{self.{prop}}}'
        str_content += '"'

        self.helper.write_code_line(2, f'return {str_content}')

        # Save the file
        self.helper.save()
