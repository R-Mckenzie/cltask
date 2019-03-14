import unittest
import task

class TestAddingRemoving(unittest.TestCase):

    def setUp(self):
        self.task_one = "Example task 1"
        self.task_two = "Example task 2"
        self.task_dictionary = {
                self.task_one : 5,
                self.task_two : 2,
                }

    def test_add_task(self):
        task_name = "TESTING TASK"
        priority = 9
        self.assertNotIn(task_name, self.task_dictionary)
        task.add_task(task_name, priority, self.task_dictionary)
        self.assertIn(task_name, self.task_dictionary)

    def test_remove_task(self):
        self.assertIn(self.task_one, self.task_dictionary)
        task.delete_task(self.task_dictionary, self.task_one)
        self.assertNotIn(self.task_one, self.task_dictionary)

if __name__ == "__main__":
    unittest.main()
