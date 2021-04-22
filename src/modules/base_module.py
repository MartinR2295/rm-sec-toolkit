from rmoptions import RMOptionHandler

class BaseModule(object):

    def __init__(self):
        self.option_handler = RMOptionHandler()

    def init_module(self):
        print("Start Module")

    def run_module(self):
        if not self.option_handler.check():
            self.show_usage()
            return

    def show_usage(self):
        print("usage")

    def show_menu(self):
        print("Menu")