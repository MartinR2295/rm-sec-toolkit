import os
from .print_helper import PrintHelper


class MenuHelper(object):

    @staticmethod
    def choose_selection_from_list(list, header="Selection"):
        while True:
            print("\n{}".format(header))
            PrintHelper.print_seperator_line()
            for index, content in enumerate(list):
                print("({}) - {}".format(index + 1, content))

            user_input = input("Input: ")
            if not user_input.isdigit():
                continue
            user_input = int(user_input) - 1
            if user_input < 0 or user_input >= len(list):
                continue

            return list[user_input]

    @staticmethod
    def choose_content_from_path(path, prefix=None,
                                 suffix=None,
                                 except_prefix=None,
                                 except_suffix=None,
                                 only_folders=None,
                                 only_files=None):
        if path.endswith("/"):
            path = path[:-1]
        contents = []

        # filter the contents
        for content in os.listdir(path):
            is_valid = True
            if prefix and not content.startswith(prefix):
                is_valid = False
            if suffix and not content.endswith(suffix):
                is_valid = False
            if except_prefix and content.startswith(except_prefix):
                is_valid = False
            if except_suffix and content.endswith(except_suffix):
                is_valid = False
            if only_folders and not os.path.isdir(path + "/" + content):
                is_valid = False
            if only_files and os.path.isdir(path + "/" + content):
                is_valid = False

            if is_valid:
                contents.append(content)

        while True:
            print("\nContents")
            PrintHelper.print_seperator_line()
            for index, content in enumerate(contents):
                print("({}) - {}".format(index + 1, content))

            user_input = input("Input: ")
            if not user_input.isdigit():
                continue
            user_input = int(user_input) - 1
            if user_input < 0 or user_input >= len(contents):
                continue

            return contents[user_input]
