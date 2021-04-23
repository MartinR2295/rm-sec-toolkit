from .base_command import BaseCommand
from ..module.module_loader import ModuleLoader
import sys


class ModuleCommand(BaseCommand):

    def handle_option(self, option):
        module_loader = ModuleLoader()
        module_path = option.value[0]

        # bring the inputted path in the correct format
        if module_path.startswith("/"):
            module_path = module_path[1:]
        if module_path.endswith("/"):
            module_path = module_path[:-1]

        # load and run module
        if module_loader.is_folder_in_path_a_module(module_path):
            sys.argv = option.value
            module = module_loader.import_module_from_folder(module_path)
            module.init_module()
            module.start_module()
