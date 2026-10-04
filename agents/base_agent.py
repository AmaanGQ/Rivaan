class BaseAgent:
    def __init__(self, name):
        self.name = name

    def run(self, task):
        print(f"{self.name} is working on: {task}")