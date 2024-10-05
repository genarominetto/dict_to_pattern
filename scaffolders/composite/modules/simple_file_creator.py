# modules/simple_file_creator.py

from modules.helpers.helper import Helper

class SimpleFileCreator:
    def __init__(self, filepath):
        self.filepath = filepath
        self.helper = Helper(filepath)

    def create_simple_file(self, content):
        # Add the content to the helper's lines list
        self.helper.lines = content.splitlines(keepends=True)
        
        # Save the file using the helper's save method
        self.helper.save()
