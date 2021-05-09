from rmsectkf.core.modules.others.add.add_module import AddModule
from rmsectkf.core.project.rm_project import RMProject
from pathlib import Path


class AddFlagModule(AddModule):

    def init_module(self):
        self.option_name = self.option_handler.create_option("name", "name of the flag",
                                                             short_name="n",
                                                             required=True)
        self.option_flag = self.option_handler.create_option("flag", "the flag itself",
                                                             short_name="f",
                                                             required=True)

    def run_module(self):
        super().run_module()
        rm_project = RMProject.get_project_from_current_path()

        if not rm_project:
            print("No rm-sec project found. Please navigate to a valid project folder.")
            return

        flag_path: Path = rm_project.flags_path.joinpath(self.option_name.value)
        flag_path.write_text("{}\n".format(self.option_flag.value))

        print("Flag added")


def get_module():
    return AddFlagModule()
