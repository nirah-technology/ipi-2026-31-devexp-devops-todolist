import json
import os
from typing import List, Optional
from uuid import UUID
from todolist.schemas import Task

DB_FILE = "data.json"

class TaskRepository:
    def __init__(self):
        self.file_path = DB_FILE
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

    def _read_data(self) -> List[Task]:
        with open(self.file_path, "r") as f:
            try:
                data = json.load(f)
                return [Task(**item) for item in data]
            except json.JSONDecodeError:
                return []

    def _write_data(self, tasks: List[Task]):
        with open(self.file_path, "w") as f:
            # model_dump(mode='json') permet de sérialiser UUID et Enum correctement
            json.dump([t.model_dump(mode='json') for t in tasks], f, indent=4)

    def save(self, task: Task) -> Task:
        tasks = self._read_data()
        tasks.append(task)
        self._write_data(tasks)
        return task

    def find_all(self) -> List[Task]:
        return self._read_data()

    def find_by_id(self, task_id: UUID) -> Optional[Task]:
        tasks = self._read_data()
        for task in tasks:
            if task.id == task_id:
                return task
        return None

    def update(self, task_id: UUID, updated_task: Task) -> Optional[Task]:
        tasks = self._read_data()
        for index, task in enumerate(tasks):
            if task.id == task_id:
                updated_task.id = task_id  # On s'assure que l'ID reste cohérent
                tasks[index] = updated_task
                self._write_data(tasks)
                return updated_task
        return None

    def delete(self, task_id: UUID) -> bool:
        tasks = self._read_data()
        initial_count = len(tasks)
        tasks = [t for t in tasks if t.id != task_id]
        if len(tasks) < initial_count:
            self._write_data(tasks)
            return True
        return False