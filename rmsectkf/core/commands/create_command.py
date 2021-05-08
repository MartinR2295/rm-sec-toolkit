from .base_command import BaseCommand
from ..module.module_loader import ModuleLoader
import sys


class CreateCommand(BaseCommand):

    def handle_option(self, option):
        if len(option.value) < 1:
            return False
        module_loader = ModuleLoader(ModuleLoader.get_available_paths())
        module_loader.append_to_current_path("others/create")
        exists = False
        for module in module_loader.get_list_of_modules_of_current_path():
            rm_module = module_loader.current_tree[module]
            if rm_module.module_meta_data.short_name == option.value[0]:
                exists = True
                sys.argv = option.value
                module = rm_module.import_and_get_class()
                module.init_module()
                module.run_module()

        return exists
