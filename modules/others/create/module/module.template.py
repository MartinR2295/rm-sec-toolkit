#!/usr/bin/env python3
from {{super_class_path}} import {{super_class}}


'''
{{module_name}}
'''


class {{module_name}}({{super_class}}):

    def __init__(self):
        super().__init__(self)

    def init_module(self):
        super.__init__()
        self.option_custom = self.option_handler.create_option("custom", "custom option",
                                                             short_name="c",
                                                             required=True,
                                                             needs_value=True)

    def run_module(self):
        super().run_module()

        #put your code here
        custom = self.option_custom.value


def get_module():
    return {{module_name}}()


# start the module if it's executed directly
if __name__ == "__main__":
    get_module().init_module()
    get_module().start_module()
