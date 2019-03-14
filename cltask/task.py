import os
import argparse
import json
from pathlib import Path

home = str(Path.home())
task_directory_location = home+"/.cltask" #The directory of the saved task list
task_file_location = home+"/.cltask/tasks.json" #The location of the saved task list

#----- File Handling Functions -----#
def create_task_file():
    """This gets called when the task file does not yet exist"""
    with open(task_file_location, 'w') as f:
        f.write('{"Example Task": 5, "COMPLETE" : []}')

def ensure_file_exists():
    try:
        os.makedirs(task_directory_location)
        create_task_file()
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
    return data

#----- Adding and Removing Tasks -----#
def add_task(task_name, priority, task_dictionary):
    """Add tasks to the working task dictionary"""
    if task_name in task_dictionary.keys():
        print("There is already a task by that name in the list. No new tasks were added.")
    else:
        task_dictionary[task_name] = priority

def get_matched_tasks(task_dictionary, string_to_match):
    matched_tasks = []
    for task in task_dictionary.keys():
        if task.find(string_to_match) >= 0:
            matched_tasks.append(task)
    return matched_tasks

def delete_task(task_dictionary, task_name):
    del task_dictionary[task_name]

def task_done(task_name, delete_tasks, task_dictionary):
    """Marks tasks that contain 'task_name' in their name as 
    completed, or deletes them if the terminal command is delete"""
    tasks_to_mark = get_matched_tasks(task_dictionary, task_name)

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
                    task_dictionary["COMPLETE"].append(task)
                delete_task(task_dictionary, str(task))
            print("\tDone.")
        else:
            print("\tNo changes made.")
    else:
        print("\tNo tasks match '{}'".format(task_name))

#----- Listing Tasks -----#
def list_active_tasks(task_dictionary):
    """List the tasks in order of priority, with some nice formatting"""
    active_tasks = task_dictionary.copy()
    #We need to make a copy so we can ignore the "COMPLETED" key in the dictionary
    del active_tasks["COMPLETE"]
    sorted_tasks = sorted(zip(active_tasks.values(), active_tasks.keys()))
    print("\tActive Tasks: ")
    for index, task in enumerate(sorted_tasks, 1):
        print('{i:>9}. {task:-<50}> priority {p} '.format('-', i=index, task=task[1]+' ', p=task[0]))

def list_completed_tasks(task_dictionary):
    """List the tasks in order of priority, with some nice formatting"""
    print("\tCompleted Tasks: ")
    for index, task in enumerate(task_dictionary["COMPLETE"], 1):
        print('{i:>9}. {task}'.format('-', i=index, task=task))

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
    user_input = ' '.join(args.input)

    ensure_file_exists()
    task_dictionary = load_tasks()

    print(' ')
    #Main body
    if args.command == "list":
        #List is the default functionality if no other commands given
        list_active_tasks(task_dictionary)
    if args.command == "completed":
        list_completed_tasks(task_dictionary)
    if args.command == "add":
        #Input is stored as a list because of the nargs. Here we convert it to a string split with spaces
        add_task(user_input, args.priority, task_dictionary)
        list_active_tasks(task_dictionary)
    if args.command == "done":
        task_done(user_input, False, task_dictionary)
    if args.command == "delete":
        task_done(user_input, True, task_dictionary)
    save_tasks(task_dictionary)
    print(' ')

if __name__ == "__main__":
    main()

