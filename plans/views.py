from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from djapy.auth.dec import djapy_login_required

from djapy.data.dec import field_required, input_required
from djapy.pagination.dec import djapy_paginator
from djapy.wrappers.dec import method_to_view, node_to_json_response, model_to_json_node

from .models import Todo
from .types import TodoPathData


@input_required(['title', 'will_be_completed_at'], allow_empty_payloads=False)
@model_to_json_node(['id', 'title', 'will_be_completed_at', 'created_at'])
def todo_post(request, data, *args, **kwargs):
    todo = Todo.objects.create(
        title=data.title,
        will_be_completed_at=data.will_be_completed_at,
        user_id=request.user.id
    )
    return todo


@djapy_paginator([
    'id', 'title', 'will_be_completed_at', 'created_at',
    'user_id', 'username', 'user', 'completed_at'
], object_parser={
    'user_id': lambda todo: todo.user.id,
    'user': lambda todo: todo.user.username,
})
def todo_get(request, *args, **kwargs):
    todos = Todo.objects.all()
    todos = todos.filter(user=request.user)
    return todos


@field_required
@model_to_json_node
def todo_patch(request, data: TodoPathData, *args, **kwargs):
    todo = Todo.objects.get(id=data.id)
    todo.title = data.title if data.title else todo.title
    todo.will_be_completed_at = data.will_be_completed_at if data.will_be_completed_at else None
    todo.completed_at = timezone.now() if data.is_completed else todo.completed_at
    todo.save()
    return todo


@csrf_exempt
@djapy_login_required
@node_to_json_response
@method_to_view
def todo_view(request):
    return {
        'post': todo_post,
        'get': todo_get,
        'patch': todo_patch
    }
