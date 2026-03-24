from typing import List, Optional
from uuid import UUID
from todolist.schemas import Task
from todolist.repository import TaskRepository

class TaskService:
    def __init__(self):
        self.repository = TaskRepository()

    def create_task(self, task: Task) -> Task:
        return self.repository.save(task)

    def get_tasks(self) -> List[Task]:
        return self.repository.find_all()

    def get_task(self, task_id: UUID) -> Optional[Task]:
        return self.repository.find_by_id(task_id)

    def update_task(self, task_id: UUID, task: Task) -> Optional[Task]:
        return self.repository.update(task_id, task)

    def delete_task(self, task_id: UUID) -> bool:
        return self.repository.delete(task_id)