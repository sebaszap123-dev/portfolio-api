from redis.asyncio import Redis

from app.settings.base import settings


redis_client = Redis.from_url(settings.redis.url)