import argparse

def init_argparse():
    app_description = "cltask is a simple command line task manager"
    parser = argparse.ArgumentParser(description=app_description)
    parser.add_argument('command',
            help="What to do. E.g. 'add', 'done', 'list', 'delete'")
    parser.add_argument('input',
            help="The data that the command needs to work with")
    parser.add_argument('-p', '--priority',
            help="How important this task is between 1 and 9. 1 is most important",
            type=int, choices=[i for i in range(1,10)])
    return parser.parse_args()

if __name__ == "__main__":
    args = init_argparse()
    print(args.command)
    print(args.input)
    print(args.priority)

