from fastapi import APIRouter, HTTPException, Query, status
from typing import Literal
from schemas import EmailPayload, TaskStatusUpdate, TaskUpdatePayload
import services

router = APIRouter()

# --------------- GET ------------------- #
# GET All Tasks
@router.get(
        "/tasks", 
        status_code=status.HTTP_200_OK,
        summary="List and Filter Tasks",
        description="""
            Returns a list of all tasks in the system.

            Allows filtering by status or priority
        """,
        responses={
            200: {
                "description": "Task list returned successfully."
            },
            401: {"description": "User not authenticated."},
        }
    )
def get_tasks(
    status: Literal["pending", "in_progress", "completed"] | None = Query(default=None),
    priority: Literal["low", "medium", "high"] | None = Query(default=None)
): 
    return services.get_all_tasks(status_filter=status, priority_filter=priority)

# GET all overdue tasks
@router.get(
    "/tasks/overdue", 
    status_code=status.HTTP_200_OK,
    summary="List overdue tasks",
    description="Returns all pending tasks whose due date has already passed.",
    responses={
        200: {
            "description": "Overdue task list returned successfully."
        },
        401: {"description": "User not authenticated."},
    }
)
def get_overdue_tasks_endpoint():
    return services.get_overdue_tasks()

# GET a summary of the task in the system
@router.get(
    "/tasks/summary", 
    status_code=status.HTTP_200_OK,
    summary="Task statistical summary",
    description="Returns a summary containing the total count of tasks grouped by status and priority level.",
    responses={
        200: {
            "description": "Summary generated successfully.",
        },
        401: {"description": "User not authenticated."},
    }
)
def get_tasks_summary_endpoint():
    all_tasks = services.get_all_tasks()
    summary = {
        "total": len(all_tasks),
        "by_status": {"pending": 0, "in_progress": 0, "completed": 0},
        "by_priority": {"low": 0, "medium": 0, "high": 0}
    }
    for task in all_tasks:
        s_val = task.get("status")
        p_val = task.get("priority")
        if s_val in summary["by_status"]:
            summary["by_status"][s_val] += 1
        if p_val in summary["by_priority"]:
            summary["by_priority"][p_val] += 1
    return summary

# GET simulation of health status
@router.get(
    "/health", 
    status_code=status.HTTP_200_OK,
    summary="API Health Check",
    description="Utility endpoint to check if the API is online, operational, and returns the current version.",
    responses={
        200: {
            "description": "API operating normally.",
        }
    }
)
def health_check():
    return {"status": "healthy", "service": "Tasks API", "version": "1.0.0"}

# GET a task by ID
@router.get(
    "/tasks/{task_id}", 
    status_code=status.HTTP_200_OK,
    summary="Get task by ID",
    description="Returns the details of a single task based on the provided numerical ID.",
    responses={
        200: {
            "description": "Task found successfully."
        },
        404: {"description": "Task not found."},
        401: {"description": "User not authenticated."},
    }
)
def get_task_by_id_endpoint(task_id: int):
    task = services.find_task_in_csv(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tarefa com ID {task_id} não encontrada.")
    return task

# --------------- POST ------------------- #
# POST a new Task
@router.post(
    "/tasks", 
    status_code=status.HTTP_201_CREATED,
    summary="Create new task via AI",
    description="Processes free text/email using local AI to structurally extract data and create a new task.",
    responses={
        201: {
            "description": "Task created successfully."
        },
        409: {"description": "Conflict while processing or duplication."},
        500: {"description": "Internal error while processing with AI."},
        401: {"description": "User not authenticated."},
    }
)
def process_text_post_endpoint(payload: EmailPayload):
    new_row = {"texto": payload.email}
    try:
        return services.process_new_task(new_row)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))
    except RuntimeError as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))



# --------------- PUT ------------------- #
# PUT - Changes a task
@router.put(
    "/tasks/{task_id}", 
    status_code=status.HTTP_200_OK,
    summary="Fully update a task",
    description="Replaces or updates the provided editable data of a specific task.",
    responses={
        200: {
            "description": "Task updated successfully."
        },
        404: {"description": "Task not found."},
        500: {"description": "Internal persistence error."},
        401: {"description": "User not authenticated."},
    }
)
def update_task_endpoint(task_id: int, payload: TaskUpdatePayload):
    try:
        updated_data = {k: v for k, v in payload.model_dump().items() if v is not None}
        return services.update_full_task(task_id, updated_data)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except FileNotFoundError as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))



# --------------- PATCH ------------------- #
# PATCH - Change the status of a task
@router.patch(
    "/tasks/{task_id}/status", 
    status_code=status.HTTP_200_OK,
    summary="Update task status",
    description="Punctually updates the status of a specific task (e.g., pending, in_progress, completed).",
    responses={
        200: {
            "description": "Status updated successfully."
        },
        404: {"description": "Task not found."},
        401: {"description": "User not authenticated."},
    }
)
def patch_task_status(task_id: int, payload: TaskStatusUpdate):
    try:
        return services.change_task(task_id=task_id, new_status=payload.status)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))

# PATCH - Changes a task to completed
@router.patch(
    "/tasks/{task_id}/complete", 
    status_code=status.HTTP_200_OK,
    summary="Mark task as completed",
    description="Shortcut to directly change a specific task's status to 'completed'.",
    responses={
        200: {
            "description": "Task marked as completed successfully."
        },
        404: {"description": "Task not found."},
        401: {"description": "User not authenticated."},
    }
)
def complete_task_endpoint(task_id: int):
    try:
        return services.alterar_tarefa(task_id=task_id, new_status="completed")
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))



# --------------- DELETE ------------------- #
# DELETE a task
@router.delete(
    "/tasks/{task_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task",
    description="Permanently removes a task from the system based on the provided ID.",
    responses={
        204: {"description": "Task deleted successfully (no content returned)."},
        404: {"description": "Task not found for deletion."},
        401: {"description": "User not authenticated."},
    }
)
def remove_task(task_id: int):
    sucesso = services.delete_task_from_csv(task_id)
    if not sucesso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tarefa com ID {task_id} não encontrada para exclusão.")
    return None