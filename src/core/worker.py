import asyncio
from arq.connections import RedisSettings
from src.core.config import settings
import structlog

logger = structlog.get_logger()

async def sample_task(ctx, x: int, y: int):
    logger.info("Running sample background task", x=x, y=y)
    await asyncio.sleep(1)
    return x + y

async def parse_and_score_resume_task(ctx, resume_id: str, job_id: str):
    logger.info("Starting background resume parse and score task", resume_id=resume_id, job_id=job_id)
    await asyncio.sleep(2)  # Simulate heavy async parsing and ML scoring
    logger.info("Successfully completed background resume parse and score task", resume_id=resume_id, job_id=job_id)
    return {"status": "success", "resume_id": resume_id, "job_id": job_id, "score": 88.5}

class WorkerSettings:
    functions = [sample_task, parse_and_score_resume_task]
    redis_settings = RedisSettings.from_dsn(getattr(settings, "redis_url", "redis://localhost:6379"))
    health_check_interval = 3600
