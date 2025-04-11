from redis import Redis
from typing import Any, Optional
import json
import logging

logger = logging.getLogger(__name__)

class CacheService:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        self.redis = Redis(host=host, port=port, db=db)
        
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            value = self.redis.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            logger.error(f"Cache get error: {str(e)}")
            return None
            
    async def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """Set value in cache with expiration"""
        try:
            serialized = json.dumps(value)
            return self.redis.setex(key, expire, serialized)
        except Exception as e:
            logger.error(f"Cache set error: {str(e)}")
            return False
            
    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        try:
            return bool(self.redis.delete(key))
        except Exception as e:
            logger.error(f"Cache delete error: {str(e)}")
            return False
            
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        try:
            return bool(self.redis.exists(key))
        except Exception as e:
            logger.error(f"Cache exists error: {str(e)}")
            return False
            
    async def clear(self) -> bool:
        """Clear all cache"""
        try:
            return self.redis.flushdb()
        except Exception as e:
            logger.error(f"Cache clear error: {str(e)}")
            return False 