import requests
import os
from .menu_helper import MenuHelper
import rmsectkf.core.module.module_loader as module_loader


class UpdateHelper(object):

    @staticmethod
    def get_newest_version_number():
        session = requests.session()
        r = session.get("https://github.com/MartinR2295/rm-sec-toolkit/releases/latest")
        if r.status_code == 200:
            return r.request.url.split("/")[-1:][0][1:]
        print("Version number couldn't be fetched. Maybe there are problems with the internet connection.")
        return False

    '''
    format with {{number: x.x.x}} is choosen to easy replace from the update script
    '''
    @staticmethod
    def get_current_version_number():
        version_number = "{{number: 0.2.4}}"
        return version_number.replace("{{number: ", "").replace("}}", "")


    @staticmethod
    def get_current_modules_version_file_name():
        return ".version_number"

    @staticmethod
    def do_pip_update():
        print("try to update with pip3 ...")
        os.system("pip3 install rm-sec-toolkit --upgrade")
        modules_path = module_loader.ModuleLoader.get_default_modules_location_path()
        os.system("rm -rf {}".format(modules_path.absolute()))
        print("restart rm-sec-toolkit to finish the update")
        exit()

    @staticmethod
    def update_modules():
        if not UpdateHelper.is_modules_folder_up_to_date():
            print("update modules from github ...")
            modules_path = module_loader.ModuleLoader.get_default_modules_location_path()
            version_number_path = modules_path.joinpath(UpdateHelper.get_current_modules_version_file_name())
            print("delete current modules folder ...")
            os.system("rm -rf {}".format(modules_path.absolute()))
            module_loader.ModuleLoader.load_default_modules_from_github()

    @staticmethod
    def get_current_modules_version():
        version_number_path = module_loader.ModuleLoader.get_default_modules_location_path() \
            .joinpath(UpdateHelper.get_current_modules_version_file_name())

        if version_number_path.exists():
            return version_number_path.read_text()
        return None

    @staticmethod
    def is_modules_folder_up_to_date():
        newest_version = UpdateHelper.get_newest_version_number()
        current_module_version = UpdateHelper.get_current_modules_version()
        return newest_version == current_module_version

    @staticmethod
    def handle_update():
        menu_content = [
            "check if new version is available",
            "do update if available",
            "do only modules update"
        ]

        selection = MenuHelper.choose_selection_from_list(menu_content, "Update")
        if selection == menu_content[0]:
            newest_version = UpdateHelper.get_newest_version_number()
            current_version = UpdateHelper.get_current_version_number()
            if newest_version == current_version:
                print("Your version is the current version {}".format(newest_version))
            else:
                print("New Version is available: {}".format(newest_version))
        elif selection == menu_content[1]:
            newest_version = UpdateHelper.get_newest_version_number()
            current_version = UpdateHelper.get_current_version_number()
            if newest_version == current_version:
                print("Your version is the current version {}".format(newest_version))
            else:
                UpdateHelper.do_pip_update()
        elif selection == menu_content[2]:
            newest_version = UpdateHelper.get_newest_version_number()
            current_module_version = UpdateHelper.get_current_modules_version()
            if newest_version == current_module_version:
                print("Your version is the current version {}".format(newest_version))
            else:
                UpdateHelper.update_modules()
