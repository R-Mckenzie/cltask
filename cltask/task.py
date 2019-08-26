#!/usr/bin/env python3
import os
import argparse
import json
from datetime import date
from pathlib import Path

home = str(Path.home())
task_directory_location = home+"/.cltask" #The directory of the saved task list
task_file_location = home+"/.cltask/tasks.json" #The location of the saved task list

'''
#-- The saved task file is a dictionary containing two dictionaries of tasks
{
    Active: [{'task1':3, 'task2':1}, etc...],
    Complete: [{'task x':3, 'complete date':DATE}, {**:**, **:**}, ...],
}
'''

#----- File Handling Functions -----#
def ensure_file_exists():
    """This function makes sure that there is a task file for the app to work with"""
    def create_example_file():
        """returns a string of json representing the example task dictionary"""
        example_task_dictionary = {
                "Active": {"Example task":5, "Example 2":3},
                "Complete": [{"Example completed task":5, "Date": str(date.today())}],}
        return json.dumps(example_task_dictionary)

    # create .cltask directory if it doesn't exist
    try:
        os.makedirs(task_directory_location)
    except (IsADirectoryError, FileExistsError):
        pass

    # create a new task file with example data if necessary
    try:
        with open(task_file_location, 'xt') as f:
            f.write(create_example_file())
    except FileExistsError:
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
    if task_name in task_dictionary["Active"].keys():
            print("There is already a task by that name in the list. No new tasks were added.")
    else:
        task_dictionary["Active"][task_name] = priority

def delete_task(task_name, task_dictionary):
    del task_dictionary["Active"][task_name]

def complete_task(task_tuple, task_dictionary):
    task_name = task_tuple[0]
    # Add the date to the task and add it to complete list
    completed = {task_name: task_tuple[1], "Date": str(date.today())}
    task_dictionary["Complete"].append(completed)
    delete_task(task_name, task_dictionary)

def task_done(task_name, delete_tasks, task_dictionary):
    """Marks tasks that contain 'task_name' in their name as 
    completed, or deletes them if the terminal command is delete"""
    active_tasks = get_active_tasks_ordered(task_dictionary)
    if active_tasks:
        list_active_tasks(task_dictionary)
        task_count = len(active_tasks)
        task_to_complete = input("\n\tWhich task have you completed? (1-{}): ".format(task_count))

        # Only use valid input. We subtract one to get the correct array index
        if task_to_complete.isdigit() and (0 <= int(task_to_complete)-1 < task_count):
            task_tuple = active_tasks[int(task_to_complete)-1]
            if not delete_tasks:
                complete_task(task_tuple, task_dictionary)
                print("\t'{}' marked as complete.".format(task_tuple[0]))
            else:
                delete_task(task_tuple[0], task_dictionary)
                print("\t'{}' deleted.".format(task_tuple[0]))
        else:
            print("\tThat is not a valid input. Nothing has been completed.")
    else:
        print("\tThere are no active tasks to complete.")

#----- Listing Tasks -----#
def get_active_tasks_ordered(task_dictionary):
    """Returns a list of tuples of the active tasks in order of priority"""
    sorted_tasks = sorted(task_dictionary["Active"].items(), key=lambda x: x[1])
    return sorted_tasks

def list_active_tasks(task_dictionary):
    """List the tasks in order of priority, with some nice formatting"""
    if get_active_tasks_ordered(task_dictionary):
        print("\tActive Tasks: ")
        for index, task in enumerate(get_active_tasks_ordered(task_dictionary), 1):
            print('{i:>9}. {task:-<50}> priority {p} '.format('-', i=index, task=task[0]+' ', p=task[1]))
    else:
        print("\tYour task list is empty!")

def list_completed_tasks(task_dictionary):
    """List the tasks in order of priority, with some nice formatting"""
    print("\tCompleted Tasks: ")
    complete_list = task_dictionary["Complete"]
    for task in complete_list:
        task_name = ""
        task_date = ""
        for k, v in task.items():
            if k != "Date":
                task_name = k
            else:
                task_date = v
        print('{i:>9} {task:-<50}> completed: {p} '.format(i='*', task=task_name+' ', p=task_date))


def init_argparse():
    """Setup the argument parser"""
    app_description = "cltask is a simple command line task manager."
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
