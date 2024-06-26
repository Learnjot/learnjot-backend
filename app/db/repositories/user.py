from bson import ObjectId
from pydantic import EmailStr
from motor.motor_asyncio import AsyncIOMotorDatabase
from db.models.user import User

class UserRepository:
    def __init__(self, database: AsyncIOMotorDatabase):
        """
        Initialises the UserRepository.
        This contains the class that will be used to manipulate the User Model
        
        Args:
            database (AsyncIOMotorDatabase): The database connection
        """
        
        self.database = database
        
    async def create_user(self, user: User):
        await self.database["users"].insert_one(user.model_dump())
        
    async def get_user_by_email(self, email: EmailStr):
        return await self.database["users"].find_one({"email": email})
    
    async def get_user_by_id(self, user_id: str):
        user_id = user_id if not isinstance(user_id, str) else ObjectId(user_id)
        return await self.database["users"].find_one({"_id": user_id})
    
    async def update_user(self, user_id: str, updated_data: dict):
        user_id = user_id if not isinstance(user_id, str) else ObjectId(user_id)
        await self.database["users"].update_one({"_id": user_id}, {"$set": updated_data})
        
    async def delete_user(self, user_id: str):
        user_id = user_id if not isinstance(user_id, str) else ObjectId(user_id)
        await self.database["users"].delete_one({"_id": user_id})