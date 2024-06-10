# Project Creator Module

from modules.main_file_creator import MainFileCreator
from modules.branch_file_creator import BranchFileCreator
from modules.leaf_file_creator import LeafFileCreator
from modules.test_file_creator import TestFileCreator
from modules.simple_file_creator import SimpleFileCreator

class ProjectCreator:
    def __init__(self, project_name):
        self.project_name = project_name

    def create_project(self):
        pass
