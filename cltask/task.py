import argparse

def init_argparse():
    app_description = "cltask is a simple command line task manager"
    parser = argparse.ArgumentParser(description=app_description)
    parser.add_argument('command',
            help="What to do. E.g. 'add', 'done', 'list', 'delete'",
            choices=["add", "done", "delete", "list"])
    parser.add_argument('input',
            help="The data that the command needs to work with")
    parser.add_argument('-p', '--priority',
            help="How important this task is between 1 and 9. 1 is most important",
            type=int, choices=[i for i in range(1,10)], default=5)
    return parser.parse_args()

task_dictionary = {}

def save_tasks(task_file):
    """Save the working task dictionary to the task file"""

def load_tasks(task_file):
    """Load tasks from the saved list into the working dictionary"""

def add_task(task_name, priority):
    """Add tasks to the working task dictionary"""
    if task_name in task_dictionary.keys():
        print("There is already a task by that name in the list. No new tasks were added.")
    else:
        task_dictionary[task_name] = priority

if __name__ == "__main__":
    args = init_argparse()
    if args.command == "add":
        add_task(args.input, args.priority)
        print(task_dictionary)

