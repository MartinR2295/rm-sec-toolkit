from .rm_module import RMModuleJson, RMModule
from ..helpers.print_helper import PrintHelper
from ..project.rm_project import RMProject
from pathlib import Path
import os
import rmsectkf.core.helpers.update_helper as update_helper

'''
Handles the actions with modules
'''


class ModuleLoader(object):

    @staticmethod
    def load_default_modules_from_github():
        modules_path = ModuleLoader.get_default_modules_location_path()
        version_number_path = modules_path.joinpath(update_helper.UpdateHelper.get_current_modules_version_file_name())
        if not modules_path.exists():
            print("load modules from github ...")
            modules_path.parent.mkdir(parents=True, exist_ok=True)
            bak = os.getcwd()
            os.chdir(modules_path.parent.absolute())
            os.system("git clone https://github.com/MartinR2295/rm-sec-toolkit.git")
            os.system("mv rm-sec-toolkit/modules ./modules")
            os.system("rm -rf rm-sec-toolkit")
            version_number_path.write_text(update_helper.UpdateHelper.get_current_version_number())
            os.chdir(bak)

    @staticmethod
    def get_default_modules_location_path():
        return Path("/usr/local/share/rm-sec-toolkit/modules")

    @staticmethod
    def get_available_paths():
        paths = [ModuleLoader.get_default_modules_location_path()]

        # search in home directory
        home_file = Path.home().joinpath(ModuleLoader.get_home_custom_file_name())
        if home_file.exists():
            with open(home_file, "r") as file:
                for path in file.readlines():
                    path = path.strip()
                    p = Path(path)
                    if p and p.exists():
                        paths.append(p)

        # search in project directory if available
        rm_project = RMProject.get_project_from_current_path()
        if rm_project:
            paths += rm_project.custom_paths

        return paths

    @staticmethod
    def get_home_custom_file_name():
        return ".rmsectk_custom_paths"

    def __init__(self, paths):
        self.modules = []
        self.current_path = Path("")
        self.modules_tree = {}
        self.current_tree = self.modules_tree
        for path in paths:
            self.modules += self.load_modules_from_path(path)

        for module in self.modules:
            category_path = module.get_category_path()
            current_tree_part = self.modules_tree
            parts = category_path.parts
            for part in parts[:-1]:
                if part not in current_tree_part:
                    current_tree_part[part] = {}
                current_tree_part = current_tree_part[part]
            current_tree_part[parts[-1:][0]] = module

    # load all modules from a path (with subdirectories)
    def load_modules_from_path(self, path: Path):
        modules = []
        for module_json_path in [f for f in path.glob("**/{}"
                                                              .format(RMModuleJson.get_rm_module_json_file_name()))]:
            modules.append(RMModule(path, module_json_path.parent))
        return modules

    # get a list of folders which are categories
    def get_list_of_categories_of_current_path(self):
        categories = []
        for key in self.current_tree.keys():
            if self.is_folder_in_path_a_category(key):
                categories.append(key)
        return categories

    # get a list of folders which are modules
    def get_list_of_modules_of_current_path(self):
        modules = []
        for key in self.current_tree.keys():
            if self.is_folder_in_path_a_module(key):
                modules.append(key)
        return modules

    # determine if the current path is in the root path of modules
    def current_path_is_root_path(self):
        return self.current_tree == self.modules_tree

    # navigte one step back if possible
    def navigate_back(self):
        if not self.current_path_is_root_path():
            self.current_path = self.current_path.parent
            self.sync_current_tree_with_current_path()

    # sync the current path with the current tree
    def sync_current_tree_with_current_path(self):
        self.current_tree = self.modules_tree
        for part in self.current_path.parts:
            self.current_tree = self.current_tree[part]

    # check if a folder in the current path is a module
    def is_folder_in_path_a_module(self, folder):
        return type(self.current_tree[folder]) is RMModule

    # check if a folder in the current path is a category
    def is_folder_in_path_a_category(self, folder):
        return type(self.current_tree[folder]) is dict

    # append an existing part to the current path
    def append_to_current_path(self, add_part):
        add_path = Path(add_part)
        tmp_tree = self.current_tree

        for part in add_path.parts:
            if part in tmp_tree:
                tmp_tree = tmp_tree[part]
            else:
                return False

        self.current_path = self.current_path.joinpath(add_part)
        self.current_tree = tmp_tree

    # get rm_module object with the absolute category path like remote/gathering/scanner/tcp_syn_scan
    def get_rm_module_with_absolute_category_path(self, path):
        tmp_tree = self.modules_tree
        for part in Path(path).parts:
            if part in tmp_tree:
                tmp_tree = tmp_tree[part]
            else:
                return None

        if type(tmp_tree) is RMModule:
            return tmp_tree

        return None

    # get RMModule from selection
    def get_module_with_selection(self, selection):
        if self.is_folder_in_path_a_module(selection):
            return self.current_tree[selection]

    # show list of categories and modules, and return the selection
    # back navigations returns None
    def show_list_and_get_selection(self):
        # load categories and modules
        categories = self.get_list_of_categories_of_current_path()
        modules = self.get_list_of_modules_of_current_path()

        # print categories and modules
        print("\nContents")
        PrintHelper.print_seperator_line()
        for index, category in enumerate(categories):
            print("({}) - {} (C)".format(index + 1, category))

        for index, module in enumerate(modules):
            print("({}) - {} (M)".format(index + len(categories) + 1, module))

        # print back option if there are steps back available
        PrintHelper.print_seperator_line()
        print("(u) - check for new updates")
        if not self.current_path_is_root_path():
            print("(b) - back")
        print("(q) - quit")
        # get selection
        selection = None
        while selection is None:
            inp = input("\nPlease choose one element: ")

            # handle back navigation and quit
            if inp == "b" and not self.current_path_is_root_path():
                self.navigate_back()
                return None
            elif inp == "q" or inp == "quit":
                print("See you")
                exit()
            elif inp == "u" or inp == "update":
                update_helper.UpdateHelper.handle_update()
                return None

            # handle the selection and return it
            if inp.isdigit():
                inp = int(inp) - 1
                if 0 <= inp < len(categories) + len(modules):
                    return (lambda: categories[inp]
                    if inp < len(categories)
                    else modules[inp - len(categories)])()
