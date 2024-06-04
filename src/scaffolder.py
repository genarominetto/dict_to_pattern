from src.scaffolder_modules.diff import IntelligentDiff

class Scaffolder(IntelligentDiff):
    def __init__(self, file1_path=None, file2_path=None):
        super().__init__(file1_path, file2_path)



