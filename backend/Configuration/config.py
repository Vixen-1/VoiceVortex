from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()

Hugging_Face_Api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")

# Initialize MongoDB client
mongo_client = MongoClient(mongo_uri)
db = mongo_client[db_name]