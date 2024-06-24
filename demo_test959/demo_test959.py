
import json
import importlib.util
import sys
import os

def load_task_json(json_path):
    with open(json_path, 'r') as json_file:
        return json.load(json_file)

def run_task(task):
    for subtask in task["subtasks"]:
        for step in subtask["steps"]:
            file_path = step["file_path"]
            function_name = step["function_name"]
            params = step["params"]
            module_name = os.path.splitext(os.path.basename(file_path))[0]
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            print(getattr(module, function_name)(**params))

if __name__ == "__main__":
    task = load_task_json("./demo_test959/task_structure.json")
    run_task(task["task"])
        