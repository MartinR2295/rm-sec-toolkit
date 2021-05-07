from .base_command import BaseCommand
from ..module.module_loader import ModuleLoader
import sys
import os


class CreateCommand(BaseCommand):

    def handle_option(self, option):
        module_loader = ModuleLoader()
        module_loader.append_to_current_path("others/create")
        exists = False
        for module in os.listdir(module_loader.current_path):
            if os.path.isdir(module_loader.combine_with_current_path(module)) \
                    and module_loader.is_folder_in_path_a_module(module):
                module_json = module_loader.get_module_json(module)
                if module_json.short_name == option.value[0]:
                    exists = True
                    sys.argv = option.value
                    module = module_loader.import_module_with_module_json(module_json)
                    module.init_module()
                    module.run_module()

        return exists
