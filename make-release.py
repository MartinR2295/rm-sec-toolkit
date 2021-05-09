#!/usr/bin/env python3
from rmoptions import RMOptionHandler
from rmsectkf.core.helpers.update_helper import UpdateHelper
from pathlib import Path
import os

def print_and_execute(command):
    os.system(command)

option_handler = RMOptionHandler()
option_major = option_handler.create_option("major", "increase major version",
                                            needs_value=False,
                                            quit_after_this_option=True)
option_minor = option_handler.create_option("minor", "increase minor version",
                                            needs_value=False,
                                            quit_after_this_option=True)
option_patch = option_handler.create_option("patch", "increase patch version",
                                            needs_value=False,
                                            quit_after_this_option=True)

if not option_handler.check():
    option_handler.print_error()
    option_handler.print_usage()
    exit()

current_version = UpdateHelper.get_current_version_number()
current_version_list = current_version.split(".")
new_version = None

if option_major.in_use:
    new_version = current_version_list
    new_version[0] = str(int(new_version[0])+1)
    new_version = ".".join(new_version)
elif option_minor.in_use:
    new_version = current_version_list
    new_version[1] = str(int(new_version[1])+1)
    new_version = ".".join(new_version)
elif option_patch.in_use:
    new_version = current_version_list
    new_version[2] = str(int(new_version[2])+1)
    new_version = ".".join(new_version)

if not new_version:
    print("Error: Specify at least one option (major, minor or patch)!")
    option_handler.print_usage()
    exit()

print("change current version {} to new version {}".format(current_version, new_version))
print("write to rmsectkf/core/helpers/update_helper.py ...")
update_helper_path = Path("rmsectkf/core/helpers/update_helper.py")
with open(update_helper_path, "r") as file:
    file_content = file.read()
    file_content = file_content.replace("{{{{number: {}}}}}".format(current_version),
                                        "{{{{number: {}}}}}".format(new_version))
    with open(update_helper_path, "w") as update_file:
        update_file.write(file_content)

print("write to rmsectkf/core/helpers/update_helper.py ...")
print_and_execute("git add .")
commit_message = input("please input a commit message: ")
print_and_execute("git commit -m \"{}\"".format(commit_message))
print("push the finished source code")
print_and_execute("git push")
print("create a release tag and push it to trigger git workflow scripts")
print_and_execute("git tag v{}".format(new_version))
print_and_execute("git push --tags")
print("Release is pushed. Please check the status of the github actions.")