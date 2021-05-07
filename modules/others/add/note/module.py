from rmsectkf.core.modules.others.add.add_module import AddModule
from rmsectkf.core.helpers.menu_helper import MenuHelper
import os
import subprocess


class AddNoteModule(AddModule):
    def run_module(self):
        if ".rm_sec_proj" not in os.listdir():
            print("No rm-sec project found. Please navigate to a valid project folder.")
            return

        notes_path = os.path.abspath("notes")
        print("notes: {}".format(notes_path))
        note_file = None

        #choose the note file if more than one exists
        available_notes = [f for f in os.listdir(notes_path) if f.endswith(".txt")]
        print("avail: {}".format(len(available_notes)))
        if len(available_notes) > 1:
            note_file = MenuHelper.choose_content_from_path(notes_path, suffix=".txt")
        elif len(available_notes) == 1:
            note_file = available_notes[0]

        if not note_file:
            print("No note files available")
            return

        note_file = notes_path + "/" + note_file
        proc = subprocess.Popen(['tail', '-n', '10', note_file], stdout=subprocess.PIPE)
        last_lines = proc.stdout.read()

        print("\nTail of {}\n".format(note_file))
        print(last_lines.decode())
        print()

        with open(note_file, "a") as file:
            print("write your notes (quit with ':q')")
            lines = []
            while True:
                line = input()
                if line == ":q":
                    break
                lines.append(line+"\n")
            file.writelines(lines)




def get_module():
    return AddNoteModule()
