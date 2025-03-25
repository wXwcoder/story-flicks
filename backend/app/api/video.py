from fastapi import APIRouter, HTTPException, Query
from loguru import logger
from app.services.video import generate_video, create_video_with_scenes, generate_voice
from app.schemas.video import VideoGenerateRequest, VideoGenerateResponse, StoryScene, VideoGenerateProgress
import os
import json
from app.utils.utils import extract_id

router = APIRouter()

@router.post("/generate")
async def generate_video_endpoint(
    request: VideoGenerateRequest
):
    """生成视频"""
    try:
        video_file = await generate_video(request)
        task_id = extract_id(video_file)
        # 转换为相对路径
        video_url = "https://backend-149289-6-1324589466.sh.run.tcloudbase.com/tasks/" + task_id + "/video.mp4"
        return VideoGenerateResponse(
            success=True,
            data={"video_url": video_url}
        )
    except Exception as e:
        logger.error(f"Failed to generate video: {str(e)}")
        return VideoGenerateResponse(
            success=False,
            message=str(e)
        )

@router.post("/progress")
async def generate_video_progress(
    request: VideoGenerateProgress
):
    """生成视频"""
    try:
        video_file = await generate_video(request)
        task_id = extract_id(video_file)
        # 转换为相对路径
        video_url = "https://backend-149289-6-1324589466.sh.run.tcloudbase.com/tasks/" + task_id + "/video.mp4"
        return VideoGenerateResponse(
            success=True,
            data={"video_url": video_url}
        )
    except Exception as e:
        logger.error(f"Failed to generate video: {str(e)}")
        return VideoGenerateResponse(
            success=False,
            message=str(e)
        )


