import os
import argparse
import json
from pathlib import Path

home = str(Path.home())
task_directory_location = home+"/.cltask" #The directory of the saved task list
task_file_location = home+"/.cltask/tasks.json" #The location of the saved task list
task_dictionary = {} #The working task dictionary. Global

#----- File Handling Functions -----#
def initialise_dictionary():
    task_dictionary["Example Task"] = 5
    task_dictionary['COMPLETE'] = []

def create_task_file():
    """Initialises the dictionary to factory settings and saves it to the a task file"""
    initialise_dictionary()
    save_tasks(task_dictionary)

def ensure_file_exists():
    try:
        os.makedirs(task_directory_location)
        create_task_file()
        print("MadeNew")
    except (FileExistsError, IsADirectoryError):
        pass

def save_tasks(task_dictionary):
    """Save the working task dictionary to the task file"""
    with open(task_file_location, 'w') as f:
        json.dump(task_dictionary, f)

def load_tasks():
    """Parses the task file and returns the data as a dictionary object"""
    with open(task_file_location, 'r') as f:
        data = json.load(f)
        print(data)
    return data

#----- Adding and Removing Tasks -----#
def add_task(task_name, priority):
    """Add tasks to the working task dictionary"""
    if task_name in task_dictionary.keys():
        print("There is already a task by that name in the list. No new tasks were added.")
    else:
        task_dictionary[task_name] = priority
    save_tasks(task_dictionary)

def task_done(task_name, delete_tasks):
    """Marks tasks that contain 'task_name' in their name as 
    completed, or deletes them if the terminal command is delete"""
    tasks_to_mark = []
    for task in task_dictionary.keys():
        if task.find(task_name) >= 0:
            tasks_to_mark.append(task)
    if len(tasks_to_mark) > 0:
        #Prompt depending on completing or deleting
        prompt = "Do you want to delete these tasks?" if delete_tasks else "Do you want to mark these tasks as completed?"
        print("\t{}: ".format(prompt))
        for task in tasks_to_mark:
            print("\t -{}".format(task))
        confirmation = input("\n\ty/n: ")
        if confirmation == 'y':
            for task in tasks_to_mark:
                if not delete_tasks:
                    task_dictionary['COMPLETE'].append(task)
                del task_dictionary[str(task)]
            print("\tDone.")
        else:
            print("\tNo changes made.")
    else:
        print("\tNo tasks match '{}'".format(task_name))

#----- Listing Tasks -----#
def list_active_tasks():
    """List the tasks in order of priority, with some nice formatting"""
    #We need to make a copy so we can delete the "COMPLETED" key in the dictionary
    active_tasks = task_dictionary.copy()
    sorted_tasks = sorted(zip(active_tasks.values(), active_tasks.keys()))
    print(sorted_tasks)
    print("\tActive Tasks: ")
    for index, task in enumerate(sorted_tasks, 1):
        print('{i:>9}. {task:-<50}> priority {p} '.format('-', i=index, task=task[1]+' ', p=task[0]))

def list_completed_tasks():
    """List the tasks in order of priority, with some nice formatting"""
    print("\tCompleted Tasks: ")
    if len(task_dictionary['COMPLETE']) > 0:
        for index, task in enumerate(task_dictionary['COMPLETE'], 1):
            print('{i:>9}. {task}'.format('-', i=index, task=task))
    else:
        print("\tNo completed tasks.")

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

def main():
    #Parse arguments
    args = init_argparse()
    user_input = ' '.join(args.input) #Input is a list of strings. Here we join them into one

    #Create task file if necessary and load tasks
    ensure_file_exists()
    task_dictionary = load_tasks()
    print(task_dictionary)

    print(' ')
    #Main body
    if args.command == "list": #Default functionality if no command is given
        list_active_tasks()
    if args.command == "completed": #Lists all completed tasks
        list_completed_tasks()
    if args.command == "add": #Add a new task
        add_task(user_input, args.priority)
        list_active_tasks()
    if args.command == "done": #Mark a task complete and add to completed list
        task_done(user_input, False)
    if args.command == "delete": #Delete a task without adding to completed list
        task_done(user_input, True)
    print(' ')


if __name__ == "__main__":
    main()
