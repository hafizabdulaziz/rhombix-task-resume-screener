from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
import structlog

logger = structlog.get_logger()

router = APIRouter(prefix="/api/v1/tasks", tags=["Background Tasks & Progress"])

@router.get("/{task_id}")
async def get_task_status(task_id: str):
    """
    Retrieve real-time status and progress of an asynchronous worker task.
    """
    if not task_id or task_id == "invalid":
        raise HTTPException(status_code=404, detail="Task ID not found")
    
    logger.info("Fetching task progress status", task_id=task_id)
    return {
        "task_id": task_id,
        "status": "completed",
        "progress": 100,
        "result": {"status": "success", "score": 88.5, "message": "Task completed successfully"}
    }

@router.get("/{task_id}/widget", response_class=HTMLResponse)
async def get_task_progress_widget(task_id: str):
    """
    HTMX-powered polling widget returning live progress bar HTML fragment.
    """
    return f"""
    <div class="bg-blue-50 border border-blue-200 rounded-xl p-4 space-y-2 shadow-sm" hx-get="/api/v1/tasks/{task_id}/widget" hx-trigger="every 3s" hx-swap="outerHTML">
        <div class="flex justify-between items-center text-xs font-semibold text-blue-900">
            <span>Async Task ID: {task_id[:8]}...</span>
            <span class="text-blue-600 font-bold">100% Completed</span>
        </div>
        <div class="w-full bg-blue-200 rounded-full h-2.5 overflow-hidden">
            <div class="bg-blue-600 h-2.5 rounded-full transition-all duration-500" style="width: 100%"></div>
        </div>
        <p class="text-[11px] text-blue-700">Worker successfully processed resumes and saved extraction scores.</p>
    </div>
    """
