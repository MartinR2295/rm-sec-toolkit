from .base_command import BaseCommand
from ..module.module_loader import ModuleLoader
import sys


class NoteCommand(BaseCommand):

    def handle_option(self, option):
        module_loader = ModuleLoader(ModuleLoader.get_available_paths())
        module_path = "others/add/note"

        module = module_loader.get_rm_module_with_absolute_category_path(module_path)
        # load and run module
        if module:
            sys.argv = ["-n"] + option.value
            module = module.import_and_get_class()
            module.init_module()
            module.start_module()
            return True
