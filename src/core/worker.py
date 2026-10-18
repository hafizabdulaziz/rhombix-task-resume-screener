import asyncio
from arq.connections import RedisSettings
from src.core.config import settings
import structlog

logger = structlog.get_logger()

async def sample_task(ctx, x: int, y: int):
    logger.info("Running sample background task", x=x, y=y)
    await asyncio.sleep(1)
    return x + y

class WorkerSettings:
    functions = [sample_task]
    redis_settings = RedisSettings.from_dsn(getattr(settings, "redis_url", "redis://localhost:6379"))
    # Health check interval
    health_check_interval = 3600
