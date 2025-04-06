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

    async def create(self, full, short):
        try:
            collection = self.db_client[self.collection_name]

            if not short:
                short = shortuuid.ShortUUID().random(length=11)

            existing_doc = await collection.find_one({"short": short})
            if existing_doc:
                print(f"Short URL '{short}' already exists.")
                return False, short

            data = {
                "full": full,
                "short": short,
                "clicks": 0,
            }
            await collection.insert_one(data)
            return True, short

        except Exception as e:
            print(f"Error inserting data: {e}")
            return False, short

    async def info(self, short):
        try:
            collection = self.db_client[self.collection_name]
            doc = await collection.find_one({"short": short})

            if doc:
                data = {
                    "full": doc.get("full", ""),
                    "short": doc.get("short", ""),
                    "clicks": doc.get("clicks", 0),
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

    async def list(self):
        try:
            items = []
            collection = self.db_client[self.collection_name]

            async for doc in collection.find({}):
                items.append(
                    {
                        "full": doc.get("full", ""),
                        "short": doc.get("short", ""),
                        "clicks": doc.get("clicks", 0),
                    }
                )

            return True, items

        except Exception as e:
            print(f"Error fetching data: {e}")
            return False, []
