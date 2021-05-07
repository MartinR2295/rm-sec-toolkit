from rmsectkf.core.modules.others.create.create_module import CreateModule
import os


class CreateProjectModule(CreateModule):

    def show_usage(self):
        print("create a project folder structure")

    def run_module(self):
        project_name = None
        while not project_name:
            project_name = input("project name:")
            if os.path.exists(project_name):
                project_name = None
                print("Error: Project folder already exist!")

            os.mkdir(project_name)
            os.mkdir(project_name+"/.rm_sec_proj")
            os.mkdir(project_name+"/notes")
            os.mkdir(project_name+"/flags")

            with open(project_name+"/challenge.txt", "w+") as file:
                challenge_url = input("Url of Challenge: ")
                file.write(challenge_url)

            with open(project_name+"/notes/general.txt", "w+") as file:
                file.write("General Notes:\n-------------------")

            print("project created")



def get_module():
    return CreateProjectModule()
