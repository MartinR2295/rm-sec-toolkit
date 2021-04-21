#!/usr/bin/env python3
from rmoptions import RMOptionHandler
import os
import json
import importlib

option_handler = RMOptionHandler()
option_create = option_handler.create_option("create", "create a resource", short_name="c", required=False, needs_value=True)

if not option_handler.check():
    option_handler.print_error()
    option_handler.print_usage()
    exit()

root_path = os.path.dirname(os.path.realpath(__file__))+"/"
module_path = "modules/"

def main():
    if option_create.in_use:
        create_path = root_path+module_path+"others/create/"
        found = False
        for m in os.listdir(create_path):
            current_path = create_path+m
            if os.path.isdir(current_path) and "rm_module.json" in os.listdir(current_path):
                with open(current_path+"/rm_module.json", "r") as file:
                    data = json.load(file)
                    if data["short-name"] == option_create.value:
                        found = True
                        import_path = current_path.replace(root_path, "").replace("/", ".")+"."+data["module"].replace(".py", "")
                        current_module = importlib.import_module(import_path).get_module()
                        current_module.init_module()
                        current_module.show_usage()
                        current_module.run_module()


        if not found:
            print("Error")
        exit()

    print_menu(root_path+module_path)

def print_menu(current_path):
    contents = os.listdir(current_path)
    folders = []
    modules = []
    root = (current_path == root_path+module_path)

    for content in contents:
        path = current_path+content
        if os.path.isdir(path) and not content.startswith("__"):
            if "rm_module.json" in os.listdir(path):
                with open(path+"/rm_module.json") as module_json:
                    modules.append((content, json.load(module_json)))
            else:
                folders.append(content)

    #print folders
    for index, content in enumerate(folders+modules):
        #for modules show the name from json
        if index < len(folders):
            print("({}) - {}".format(index+1, content))
        else:
            print("({}) - {}".format(index+1, content[1]['name']))

    if not root:
        print("(b) - back")

    input_number = 0
    while input_number < 1 or input_number > len(folders+modules):
        inp = input("Input: ")
        if inp.isdigit():
            input_number = int(inp)
            continue

        if inp == "b" and not root:
            print_menu("/".join(current_path.split("/")[:-2])+"/")
            return


    input_number -= 1 #to get the real list index
    #folder handling
    if input_number < len(folders):
        print_menu(current_path+folders[input_number]+"/")
    else: #module handling
        module = modules[input_number-len(folders)]
        import_path = current_path.replace(root_path, "").replace("/", ".")+module[0]+"."+module[1]["module"].replace(".py", "")
        current_module = importlib.import_module(import_path).get_module()
        current_module.init_module()
        current_module.show_usage()
        current_module.run_module()


if __name__ == "__main__":
    main()