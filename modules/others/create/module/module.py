from rmsectkf.core.modules.others.create.create_module import CreateModule
from rmsectkf.core.module.rm_module import RMModuleJson
from pathlib import Path


class CreateProjectModule(CreateModule):

    def __init__(self):
        super().__init__()

    def init_module(self):
        super().init_module()
        self.option_name = self.option_handler.create_option("name", "module name",
                                                             short_name="n",
                                                             required=True,
                                                             needs_value=True)
        self.option_short_name = self.option_handler.create_option("short-name", "module short name",
                                                                   short_name="sn",
                                                                   required=True,
                                                                   needs_value=True)
        self.option_description = self.option_handler.create_option("description", "module description",
                                                                    short_name="d",
                                                                    required=True,
                                                                    needs_value=True)
        self.option_author = self.option_handler.create_option("author", "module's author",
                                                               short_name="a",
                                                               required=True,
                                                               needs_value=True)
        self.option_super_class = self.option_handler.create_option("super-class", "super class",
                                                                    short_name="s",
                                                                    required=True,
                                                                    default_value="BaseModule",
                                                                    needs_value=True)
        self.option_super_class_path = self.option_handler.create_option("super-class-path", "super class path",
                                                                         short_name="sp",
                                                                         required=True,
                                                                         default_value="rmsectkf.core.modules.base_module",
                                                                         needs_value=True)
        self.option_class_name = self.option_handler.create_option("class-name", "name of the class",
                                                                   short_name="c",
                                                                   required=True,
                                                                   default_value="CustomModule",
                                                                   needs_value=True)

    def run_module(self):
        if not super().run_module():
            return False
        template_path = Path(__file__).parent.absolute().joinpath("module.template")

        print("create module folder ...")
        path = Path(self.option_short_name.value)
        if path.exists():
            print("Module already exists")
            return

        path.mkdir()

        print("generate module json ...")
        module_json = RMModuleJson()
        module_json.name = self.option_name.value
        module_json.short_name = self.option_short_name.value
        module_json.author = self.option_author.value
        module_json.version = 1.0
        module_json.description = self.option_description.value
        module_json.module = "module.py"
        module_json.save_to_file(path.joinpath(RMModuleJson.get_rm_module_json_file_name()))

        print("generate __init__.py ...")
        path.joinpath("__init__.py").touch()

        print("generate module.py ...")
        with open(template_path, "r") as file:
            template = file.read()
            with open(path.joinpath(module_json.module), "w") as module_file:
                module_file.write(template.replace("{{super_class_path}}", self.option_super_class_path.value)
                                  .replace("{{super_class}}", self.option_super_class.value)
                                  .replace("{{module_name}}", self.option_class_name.value))

        print("new module was created successfully in {}".format(path.absolute()))


def get_module():
    return CreateProjectModule()


# start the module if it's executed directly
if __name__ == "__main__":
    get_module().init_module()
    get_module().start_module()
