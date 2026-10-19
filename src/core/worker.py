import asyncio
import json

import structlog
from arq.connections import RedisSettings

from src.core.config import settings

logger = structlog.get_logger()

async def sample_task(ctx, x: int, y: int):
    logger.info("Running sample background task", x=x, y=y)
    await asyncio.sleep(1)
    return x + y

async def parse_and_score_resume_task(ctx, resume_id: str, job_id: str):
    max_retries = 3
    retry_count = ctx.get("job_try", 1)
    
    logger.info("Starting background resume parse and score task", resume_id=resume_id, job_id=job_id, retry_count=retry_count)
    try:
        await asyncio.sleep(1)
        # Simulate parsing/scoring logic
        if resume_id == "fail-test":
            raise ValueError("Simulated resume parsing failure for DLQ testing")
        
        logger.info("Successfully completed background resume parse and score task", resume_id=resume_id, job_id=job_id)
        return {"status": "success", "resume_id": resume_id, "job_id": job_id, "score": 92.0}
    except Exception as e:
        logger.error("Error in background resume parse task", resume_id=resume_id, error=str(e), retry_count=retry_count)
        if retry_count < max_retries:
            logger.info("Retrying task...", resume_id=resume_id, next_try=retry_count + 1)
            raise e  # ARQ native retry
        else:
            logger.error("Max retries reached. Moving task to Dead-Letter Queue (DLQ)", resume_id=resume_id)
            # Push to DLQ representation in Redis if pool exists
            redis = ctx.get("redis")
            if redis:
                dlq_payload = json.dumps({"resume_id": resume_id, "job_id": job_id, "error": str(e)})
                await redis.lpush("arq:dlq", dlq_payload)
            raise e

class WorkerSettings:
    functions = [sample_task, parse_and_score_resume_task]
    redis_settings = RedisSettings.from_dsn(getattr(settings, "redis_url", "redis://localhost:6379"))
    health_check_interval = 3600
    max_jobs = 10
    job_timeout = 300
