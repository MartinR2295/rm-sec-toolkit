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
            module_json = module_loader.get_module_json(module_path)
            module = module_loader.import_module(module_loader.get_import_path_with_module_json(module_json))
            module.init_module()
            module.run_module()