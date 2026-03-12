from ninja import NinjaAPI, Schema
from .models import Task

api = NinjaAPI()

class TaskSchema(Schema):
    id: int
    title: str
    description: str
    completed: bool

class TaskCreateSchema(Schema):
    title: str
    description: str = ""

class TaskUpdateSchema(Schema):
    title: str = None
    description: str = None
    completed: bool = None

@api.get('/tasks', response=list[TaskSchema])
def list_tasks(request):
    return Task.objects.all()

@api.post('/tasks', response=TaskSchema)
def create_task(request, payload: TaskCreateSchema):
    task = Task.objects.create(**payload.dict())
    return task

@api.put('/tasks/{task_id}', response=TaskSchema)
def update_task(request, task_id: int, payload: TaskUpdateSchema):
    task = Task.objects.get(id=task_id)
    for attr, value in payload.dict(exclude_none=True).items():
        setattr(task, attr, value)
    task.save()
    return task

@api.delete('/tasks/{task_id}')
def delete_task(request, task_id: int):
    task = Task.objects.get(id=task_id)
    task.delete()
    return {"success": True}