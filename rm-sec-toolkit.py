#!/usr/bin/env python3
from rmoptions import RMOptionHandler
from src.core.commands.module_command import ModuleCommand
from src.core.commands.create_command import CreateCommand
from src.core.module.module_loader import ModuleLoader

# create the option handler and set the commands
option_handler = RMOptionHandler()
option_create = option_handler.create_option("create", "create a resource",
                                             short_name="c", required=False,
                                             quit_after_this_option=True)

option_module = option_handler.create_option("module", "choose a module",
                                             short_name="m", required=False,
                                             quit_after_this_option=True)

# check the options
if not option_handler.check():
    option_handler.print_error()
    option_handler.print_usage()
    exit()

# handle the commands
if option_handler.activated_main_option:
    if option_handler.activated_main_option == option_module:
        module_command = ModuleCommand()
        module_command.handle_option(option_module)
    elif option_handler.activated_main_option == option_create:
        create_command = CreateCommand()
        create_command.handle_option(option_create)
    exit()


# interactive mode
def main():
    module_loader = ModuleLoader()
    while True:
        # print lists, get selections and load modules if selected
        selection = module_loader.show_list_and_get_selection()

        if selection:
            if module_loader.is_folder_in_path_a_category(selection):
                module_loader.append_to_current_path(selection)
            elif module_loader.is_folder_in_path_a_module(selection):
                module = module_loader.import_module_from_folder(selection)
                module.init_module()
                module.start_module()


if __name__ == "__main__":
    main()
