# modules/simple_file_creator.py

from modules.helpers.helper import Helper

class SimpleFileCreator:
    def __init__(self, filename):
        self.filename = filename
        self.helper = Helper(filename)

    def create_simple_file(self, content):
        self.helper.write_code_line(0, content)
        self.helper.save()
