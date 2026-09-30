from typing import Any
from .db import enqueue_task, list_tasks, update_task

class TaskQueue:
    def enqueue(self, command: str, priority: str = "normal", assigned_agent: str | None = None) -> dict[str, Any]:
        return enqueue_task(command, priority, assigned_agent)

    def list(self, status: str | None = None) -> list[dict[str, Any]]:
        return list_tasks(status)

    def update(self, task_id: str, status: str, result: str | None = None) -> dict[str, Any] | None:
        return update_task(task_id, status, result)

queue = TaskQueue()
