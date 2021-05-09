from rmoptions import RMOptionHandler
import sys
from ..helpers.print_helper import PrintHelper


class BaseModule(object):

    def __init__(self):
        self.option_handler = RMOptionHandler()
        self.option_run_instantly = self.option_handler.create_option("run", "run the module instantly",
                                                                      short_name="r",
                                                                      needs_value=False)

    # get the unparsed options from argv
    def get_raw_option_list(self):
        raw_options = []
        current_option = ""
        for arg in sys.argv[1:]:
            if arg.startswith("-"):
                if current_option != "":
                    raw_options.append(current_option)
                    current_option = ""
                while arg.startswith("-"):
                    arg = arg[1:]
                current_option += arg
            else:
                current_option += " {}".format(arg)
        if current_option != "":
            raw_options.append(current_option)
        return raw_options

    def get_raw_option_values(self, option):
        option_values = [opt for opt in self.get_raw_option_list()
                         if opt.startswith(option.long_name)
                         or (option.short_name is not None and opt.startswith(option.short_name))]
        return (lambda: " ".join(option_values[0].split(" ")[1:])
        if len(option_values) > 0
        else None)()

    def init_module(self):
        pass

    def start_module(self):
        ask_for_required_options_bak = self.option_handler.ask_for_required_options
        ask_for_missing_values_bak = self.option_handler.ask_for_missing_values
        self.option_handler.ask_for_required_options = False
        self.option_handler.ask_for_missing_values = False
        self.option_handler.check()
        self.option_handler.ask_for_required_options = ask_for_required_options_bak
        self.option_handler.ask_for_missing_values = ask_for_missing_values_bak
        if self.option_run_instantly.in_use:
            self.run_module()
            exit()

        if self.option_handler.help_option.in_use:
            self.option_handler.print_usage()
            exit()

        self.show_help()
        while True:
            inp = input("module> ")
            if inp == "c" or inp == "close":
                break
            elif inp == "q" or inp == "quit":
                exit()
            elif inp == "options":
                self.show_options()
            elif inp == "run" or inp == "exploit":
                self.run_module()
            elif inp.startswith("set") and len(inp.split(" ")) >= 3:
                option_name = inp.split(" ")[1]
                for opt in self.option_handler.options:
                    if opt.long_name == option_name or (opt.short_name is not None and opt.short_name == option_name):
                        # delete in the argv array if exists
                        for r_opt in self.get_raw_option_list():
                            if r_opt.startswith(opt.long_name) or (
                                    opt.short_name is not None and r_opt.startswith(opt.short_name)):
                                for i, arg in enumerate(sys.argv):
                                    if r_opt.startswith(arg.replace("-", "")):
                                        sys.argv[i] = arg.replace("-", "")
                                        sys.argv = " ".join(sys.argv).replace(r_opt, "").split(" ")
                                        sys.argv = [arg for arg in sys.argv if arg != ""]

                        # append to argv
                        sys.argv += ["--{}".format(opt.long_name)]
                        sys.argv += inp.split(" ")[2:]
            elif inp == "h" or inp == "help":
                self.show_help()

    def run_module(self):
        for option in self.option_handler.options:
            option.in_use = False
            if option.multiple_values:
                option.value = []
            else:
                option.value = None
        if not self.option_handler.check():
            self.option_handler.print_error()
            self.show_usage()
            return False
        return True

    def show_usage(self):
        self.option_handler.print_usage()

    def show_help(self):
        print("\nModule")
        PrintHelper.print_seperator_line()
        print("show help")
        print("\thelp\n\th")
        print("show options")
        print("\toptions")
        print("set a option")
        print("\tset {option-name} {value}")
        print("run the module")
        print("\trun")
        print("close the module")
        print("\tclose\n\tc")
        print("quit rm-sec-toolkit")
        print("\tquit\n\tq")

    def show_options(self):
        raw_options = self.get_raw_option_list()
        PrintHelper.print_seperator_line()
        PrintHelper.print_seperator_line()
        print("Options")
        PrintHelper.print_seperator_line()
        PrintHelper.print_seperator_line()
        print("\nRequired")
        PrintHelper.print_seperator_line()
        for option in self.option_handler.get_required_options():
            # get the values if set
            option_values = self.get_raw_option_values(option)

            print("{}".format(option.long_name))
            print("\t{}".format((lambda: option_values if option_values else "not set")()))
        print("\nOptional")
        PrintHelper.print_seperator_line()
        for option in self.option_handler.get_non_required_options():
            # skip the help option
            if option == self.option_handler.help_option or option == self.option_run_instantly:
                continue

            # get the values if set
            option_values = self.get_raw_option_values(option)

            print("{}".format(option.long_name))
            print("\t{}".format((lambda: option_values if option_values else "not set")()))
