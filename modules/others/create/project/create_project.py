from rmsectkf.core.modules.others.create.create_module import CreateModule
from pathlib import Path


class CreateProjectModule(CreateModule):

    def init_module(self):
        self.option_name = self.option_handler.create_option("name", "project name",
                                                             short_name="n",
                                                             required=True,
                                                             needs_value=True)
        self.option_url = self.option_handler.create_option("url", "url of the project (if available)",
                                                            short_name="u",
                                                            required=False,
                                                            needs_value=True)

    def run_module(self):
        super().run_module()
        project_name = self.option_name.value
        project_path = Path(project_name)

        if project_path.exists():
            print("Error: Project folder already exist!")
            return
        project_settings_path = project_path.joinpath(".rm_sec_proj")
        notes_path = project_path.joinpath("notes")
        flags_path = project_path.joinpath("flags")
        custom_scripts_path = project_path.joinpath("project_scripts")

        project_settings_path.mkdir(parents=True)
        notes_path.mkdir()
        flags_path.mkdir()
        custom_scripts_path.mkdir()

        project_settings_path.joinpath(".rmsectk_custom_paths").write_text(str(project_path.absolute()))
        project_path.joinpath("challenge.txt").write_text("url: {}\n".format(self.option_url.value))
        notes_path.joinpath("general.txt").write_text("General Notes:\n------------------\n")


        print("project created")


def get_module():
    return CreateProjectModule()
