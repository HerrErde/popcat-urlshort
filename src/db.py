import datetime

import shortuuid
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import errors

import config

db_host = config.DB_HOST
db_user = config.DB_USER
db_pass = config.DB_PASS
db_cluster = config.DB_CLUSTER
client = config.DB_NAME
collection = config.DB_COLLECTION

if db_cluster:
    MONGODB_URI = f"mongodb+srv://{db_user}:{db_pass}@{db_host}/?retryWrites=true&w=majority&appName={db_cluster}"
else:
    MONGODB_URI = (
        f"mongodb://{db_user}:{db_pass}@{db_host}/?retryWrites=true&w=majority"
    )


class DBHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBHandler, cls).__new__(cls)
        return cls._instance

    async def initialize(self):
        if hasattr(self, "initialized") and self.initialized:
            return

        try:
            self.client = AsyncIOMotorClient(MONGODB_URI)
            self.db_client = self.client[client]
            self.collection_name = collection
            self.initialized = True
            print("Successfully connected to MongoDB")
        except errors.ConfigurationError as e:
            print(f"ConfigurationError: {e}")
        except errors.ConnectionFailure as e:
            print(f"ConnectionFailure: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    async def create(self, full: str, short: str | None = None, max_attempts: int = 5):
        try:
            collection = self.db_client[self.collection_name]

            attempts = 0
            while not short or await collection.find_one({"short": short}):
                if attempts >= max_attempts:
                    logging.error(
                        "Failed to generate unique short after %d attempts",
                        max_attempts,
                    )
                    return False, None
                short = shortuuid.ShortUUID().random(length=config.SHORT_LEN)
                attempts += 1

            data = {
                "full": full,
                "short": short,
                "clicks": 0,
                "date": datetime.datetime.now(tz=datetime.timezone.utc),
            }
            await collection.insert_one(data)
            return True, short

        except Exception as e:
            logging.exception("Error inserting data")
            return False, None

    async def info(self, short):
        try:
            collection = self.db_client[self.collection_name]
            doc = await collection.find_one({"short": short})

            if doc:
                data = {
                    "full": doc.get("full", ""),
                    "short": doc.get("short", ""),
                    "clicks": doc.get("clicks", 0),
                    "date": doc.get("date", 0),
                }
                return True, data
            return False, None

        except Exception as e:
            print(f"Error fetching data: {e}")
            return False, None

    async def redirect(self, short):
        try:
            collection = self.db_client[self.collection_name]
            doc = await collection.find_one({"short": short})

            if doc:
                await collection.update_one({"short": short}, {"$inc": {"clicks": 1}})
                return doc.get("full", "")

            return None

        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    async def list(self, page: int = 1, per_page: int = 48):
        try:
            collection = self.db_client[self.collection_name]
            skip_count = (page - 1) * per_page

            total = await collection.count_documents({})

            cursor = collection.find({}).skip(skip_count).limit(per_page)
            items = [
                {
                    "full": doc.get("full", ""),
                    "short": doc.get("short", ""),
                    "clicks": doc.get("clicks", 0),
                }
                async for doc in cursor
            ]

            return True, items, total

        except Exception as e:
            print(f"Error fetching data: {e}")
            return False, [], 0
