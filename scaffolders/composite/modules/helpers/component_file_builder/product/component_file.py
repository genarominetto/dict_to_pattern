class ComponentFile:
    def __init__(self, component_file_type):
        self.component_file_type = component_file_type

    def __str__(self):
        return (f"ComponentFile of type {self.component_file_type} with .")
