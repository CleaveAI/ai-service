from typing import List, Optional, Type

from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.config import settings
from src.logger import logger
from src.utils.exceptions import DatabaseError


class MongoDBClient:
    _instance: Optional["MongoDBClient"] = None
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None

    def __new__(cls) -> "MongoDBClient":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def init_db(self, document_models: List[Type[Document]] | None = None):
        if self.client:
            logger.warning("Database connection already initialized.")
            return

        try:
            logger.info("Initializing database connection...")
            self.client = AsyncIOMotorClient(settings.MONGODB_URL)
            await self.client.server_info()

            self.db = self.client.get_default_database()
            if self.db is None:
                raise DatabaseError(
                    "Database not found in MongoDB URL. Please specify it."
                )

            if document_models:
                await init_beanie(database=self.db, document_models=document_models)

            logger.info("Database connection initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize database connection: {e}")
            if self.client:
                self.client.close()
                self.client = None
            raise DatabaseError(f"Could not connect to MongoDB: {e}") from e

    async def close_db(self):
        if self.client:
            logger.info("Closing database connection...")
            self.client.close()
            self.client = None
            self.db = None
            logger.info("Database connection closed.")

    @classmethod
    def get_instance(cls) -> "MongoDBClient":
        if cls._instance is None:
            cls._instance = MongoDBClient()
        return cls._instance


mongodb_client = MongoDBClient.get_instance()
