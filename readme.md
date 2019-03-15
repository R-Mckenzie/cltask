# Cltask

Cltask is a command line task lister written in Python.

## Installation

Cltask has not been uploaded to PyPi yet. To install, clone the repository and run pip install in the top level dorectory:

```bash
git clone https://github.com/R-Mckenzie/cltask.git
cd cltask
pip install -e .
```

## Usage

Add a new task "Task name" to the task list using the default priority of 5:
```bash
task add Task name
```
Add a new task "Task with priority to the task list with priority 3:
```bash
task add Task with priority -p 3 
```
Prompt user on marking all tasks that contain "Task" as complete:
```bash
task done Task 
```
Prompt user on deleting all tasks that contain "Task":
```bash
task delete Task 
```
List active tasks:
```bash
task list
```
List completed tasks:
```bash
task completed
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
