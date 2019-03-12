import argparse
import json
from pathlib import Path

home = str(Path.home())
task_dictionary = {} #The working task dictionary. Global
task_file_location = home+"/.cltask/tasks.json" #The location of the saved task list

def init_argparse():
    """Setup the argument parser"""
    app_description = "cltask is a simple command line task manager"
    parser = argparse.ArgumentParser(description=app_description)
    parser.add_argument('command',
            help="Which command to run",
            choices=["add", "done", "delete", "list"], default="list", nargs='?')
    parser.add_argument('input',
            help="The data that the command needs to work with", nargs='*')
    parser.add_argument('-p', '--priority',
            help="How important this task is between 1 and 9. 1 is most important",
            type=int, choices=[i for i in range(1,10)], default=5)
    return parser.parse_args()

def save_tasks(task_dictionary):
    """Save the working task dictionary to the task file"""
    with open(task_file_location, 'w') as f:
        json.dump(task_dictionary, f)

def load_tasks():
    """Parses the task file and returns the data as a dictionary object"""
    with open(task_file_location, 'r') as f:
        data = json.load(f)
    return data

def add_task(task_name, priority):
    """Add tasks to the working task dictionary"""
    if task_name in task_dictionary.keys():
        print("There is already a task by that name in the list. No new tasks were added.")
    else:
        task_dictionary[task_name] = priority

def task_file_exists():
    """Check if there is a task file. Returns true if there is, false if not"""
    try:
        file=open(task_file_location, 'r')
    except FileNotFoundError:
        return False
    #If we get here, the file exists. Return true
    return True

def create_task_file():
    """This gets called when the task file does not yet exist"""
    with open(task_file_location, 'w') as f:
        f.write('{"Example Task": 5}')

if __name__ == "__main__":
    #Parse arguments
    args = init_argparse()

    #Load tasks if file exists, otherwise create it
    if task_file_exists():
        task_dictionary = load_tasks()
    else:
        create_task_file()

    #Operate on arguments
    if args.command == "list":
        #List is the default functionality if no other commands given
        print("Tasks:")
    if args.command == "add":
        #Input is stored as a list because of the nargs. Here we convert it to a string split with spaces
        task_name = ' '.join(args.input)
        add_task(task_name, args.priority)
        save_tasks(task_dictionary)
    if args.command == "done":
        print("Done")
    if args.command == "delete":
        print("Delete")

