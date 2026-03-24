from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from todolist.schemas import Task
from todolist.service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])
service = TaskService()

@router.get("", response_model=List[Task])
def get_tasks():
    return service.get_tasks()

@router.get("/{task_id}", response_model=Task)
def get_task(task_id: UUID):
    task = service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: Task):
    return service.create_task(task)

@router.put("/{task_id}", response_model=Task)
def update_task(task_id: UUID, task: Task):
    updated = service.update_task(task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID):
    deleted = service.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    