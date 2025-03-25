from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from loguru import logger
from app.services.video import generate_video, create_video_with_scenes, generate_voice,get_video_progress,generate_video_background
from app.schemas.video import VideoGenerateRequest, VideoGenerateResponse, StoryScene, VideoGenerateProgress
import os
import json
import uuid
from app.utils.utils import extract_id

router = APIRouter()

@router.post("/generate")
async def generate_video_endpoint(
    request: VideoGenerateRequest,
    background_tasks: BackgroundTasks
):
    """生成视频（异步任务）"""
    try:
        task_id = str(uuid.uuid4())
        # 创建初始任务状态
        from app.services.video import update_task_progress
        update_task_progress(task_id, 0, "pending", "")
        
        # 启动后台任务
        background_tasks.add_task(generate_video_background, task_id, request)
        
        return VideoGenerateResponse(
            success=True,
            data={"task_id": task_id}
        )
    except Exception as e:
        logger.error(f"Failed to start video generation: {str(e)}")
        return VideoGenerateResponse(
            success=False,
            message=str(e)
        )

@router.post("/progress")
async def generate_video_progress(
    task_id: str = Query(..., description="任务ID")
):
    """查询视频生成进度"""
    try:
        from app.services.video import get_task_progress
        status = get_task_progress(task_id)
        
        if not status:
            return VideoGenerateResponse(
                success=False,
                message="任务不存在"
            )
            
        response_data = {
            "progress": status["progress"],
            "status": status["state"]
        }
        
        if status["state"] == "completed":
            response_data["video_url"] = status["result"]
        elif status["state"] == "failed":
            response_data["error"] = status["error"]
            
        return VideoGenerateResponse(
            success=True,
            data=response_data
        )
    except Exception as e:
        logger.error(f"查询进度失败: {str(e)}")
        return VideoGenerateResponse(
            success=False,
            message=str(e)
        )


