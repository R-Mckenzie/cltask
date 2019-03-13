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
            choices=["add", "done", "delete", "list", "completed"], default="list", nargs='?')
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
        f.write('{"Example Task": 5, "COMPLETE" : []}')

def list_active_tasks():
    """List the tasks in order of priority, with some nice formatting"""
    active_tasks = task_dictionary.copy()
    #We need to make a copy so we can ignore the "COMPLETED" key in the dictionary
    del active_tasks["COMPLETE"]
    sorted_tasks = sorted(zip(active_tasks.values(), active_tasks.keys()))
    print("\tActive Tasks: ")
    for index, task in enumerate(sorted_tasks, 1):
        print('{i:>9}. {task:-<50}> priority {p} '.format('-', i=index, task=task[1]+' ', p=task[0]))

def list_completed_tasks():
    """List the tasks in order of priority, with some nice formatting"""
    print("\tCompleted Tasks: ")
    for index, task in enumerate(task_dictionary["COMPLETE"], 1):
        print('{i:>9}. {task}'.format('-', i=index, task=task))

def task_done(task_name):
    """Marks tasks that contain 'task_name' in their name as completed"""
    tasks_to_mark = []
    for task in task_dictionary.keys():
        if task.find(task_name) >= 0:
            tasks_to_mark.append(task)
    if len(tasks_to_mark) > 0:
        print("\tDo you want to mark these tasks as completed?: ")
        for task in tasks_to_mark:
            print("\t -{}".format(task))
        delete_confirmation = input("\n\ty/n: ")
        if delete_confirmation == 'y':
            for task in tasks_to_mark:
                task_dictionary["COMPLETE"].append(task)
                del task_dictionary[str(task)]
            print("\n\tMarked as complete")
    else:
        print("\tNo tasks match '{}'".format(task_name))

if __name__ == "__main__":
    #Parse arguments
    args = init_argparse()
    user_input = ' '.join(args.input)

    #Load tasks if file exists, otherwise create it
    if task_file_exists():
        task_dictionary = load_tasks()
    else:
        create_task_file()

    print(' ')
    #Main body
    if args.command == "list":
        #List is the default functionality if no other commands given
        list_active_tasks()
    if args.command == "completed":
        list_completed_tasks()
    if args.command == "add":
        #Input is stored as a list because of the nargs. Here we convert it to a string split with spaces
        add_task(user_input, args.priority)
        list_active_tasks()
    if args.command == "done":
        task_done(user_input)
    if args.command == "delete":
        print("Delete")

    save_tasks(task_dictionary)
    print(' ')

