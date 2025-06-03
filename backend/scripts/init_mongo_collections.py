# scripts/init_mongo_collections.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")

mongo_client = MongoClient(mongo_uri)
db = mongo_client[db_name]

def create_collections_and_indexes():
    try:
        # Collection 1: qna
        qna_collection = db["qna"]
        try:
            qna_collection.create_index(
                [("question_embedding", "vector")],
                vectorOptions={
                    "type": "vector",
                    "dimensions": 384,
                    "similarity": "cosine"
                },
                name="vector_index"
            )
            print("Vector search index created for qna collection")
        except Exception as e:
            print(f"Vector index creation for qna skipped (manual creation may be required): {e}")

        qna_collection.create_index(
            [("normalized_question", "text")],
            name="text_index"
        )
        print("Text index created for qna.normalized_question")

        # Collection 2: popular_question
        popular_question_collection = db["popular_question"]
        popular_question_collection.create_index(
            [("question", 1)],
            unique=True,
            name="unique_question"
        )
        print("Unique index created for popular_question.question")

        try:
            popular_question_collection.create_index(
                [("question_embedding", "vector")],
                vectorOptions={
                    "type": "vector",
                    "dimensions": 384,
                    "similarity": "cosine"
                },
                name="vector_index"
            )
            print("Vector search index created for popular_question collection")
        except Exception as e:
            print(f"Vector index creation for popular_question skipped (manual creation may be required): {e}")

        popular_question_collection.create_index(
            [("search_count", -1)],
            name="search_count_index"
        )
        print("Index created for popular_question.search_count")

        # Collection 3: error_logs
        error_logs_collection = db["error_logs"]
        error_logs_collection.create_index(
            [("question", 1)],
            name="question_index"
        )
        print("Index created for error_logs.question")

        print("✅ All collections and indexes initialized successfully.")

    except Exception as e:
        print(f"Error initializing collections: {str(e)}")
    finally:
        mongo_client.close()

if __name__ == "__main__":
    create_collections_and_indexes()