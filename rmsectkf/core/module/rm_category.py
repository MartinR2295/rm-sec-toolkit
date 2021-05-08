import json
from pathlib import Path


class RMCategory(object):

    def __init__(self, path: Path):
        self.path = path
        self.subcategories = []
        self.modules = []

    @staticmethod
    def get_rm_module_json_file_name():
        return "rm_category.json"
