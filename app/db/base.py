from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

client = AsyncIOMotorClient(settings.DATABASE_URL)
database = client[settings.DEFAULT_DATABASE]