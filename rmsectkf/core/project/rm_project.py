from pathlib import Path


class RMProject(object):

    def __init__(self):
        self.path = Path()
        self.settings_path = Path(RMProject.get_project_settings_folder_name())
        self.notes_path = Path(RMProject.get_notes_folder_name())
        self.flags_path = Path(RMProject.get_flags_folder_name())
        with open(self.settings_path.joinpath(RMProject.get_project_custom_file_name()), "r") as file:
            self.custom_paths = [Path(p.strip()) for p in file.readlines() if Path(p.strip()).exists()]

    @staticmethod
    def get_project_from_current_path():
        path = Path()
        if path.joinpath(RMProject.get_project_settings_folder_name()).exists():
            return RMProject()
        return None

    @staticmethod
    def get_project_settings_folder_name():
        return ".rm_sec_proj"

    @staticmethod
    def get_notes_folder_name():
        return "notes"

    @staticmethod
    def get_flags_folder_name():
        return "flags"

    @staticmethod
    def get_custom_scripts_folder_name():
        return "custom_scripts"

    @staticmethod
    def get_project_custom_file_name():
        return ".rmsectk_custom_paths"
