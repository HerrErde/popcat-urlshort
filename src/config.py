import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG", False)

DB_HOST = os.getenv("MONGODB_HOST")
DB_USER = os.getenv("MONGODB_USER")
DB_PASS = os.getenv("MONGODB_PASS")
DB_CLUSTER = os.getenv("MONGODB_CLUSTER")
DB_NAME = os.getenv("MONGODB_DATABASE", "webservice")
DB_COLLECTION = os.getenv("MONGODB_COLLECTION", "urlshort")


PORT = os.getenv("PORT", 5000)
HOST = os.getenv("HOST", "0.0.0.0")
