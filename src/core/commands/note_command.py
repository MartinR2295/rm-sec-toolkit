from .base_command import BaseCommand
from ..module.module_loader import ModuleLoader
import sys


class NoteCommand(BaseCommand):

    def handle_option(self, option):
        module_loader = ModuleLoader()
        module_path = "others/add/note"

        # load and run module
        if module_loader.is_folder_in_path_a_module(module_path):
            sys.argv = option.value
            module = module_loader.import_module_from_folder(module_path)
            module.init_module()
            module.run_module()
