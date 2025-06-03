# threads/search_count_thread.py
from queue import Queue
from typing import List
from Configuration.config import db
from utils.nlp_utils import fetch_answers_from_db

def update_search_counts(sub_questions: List[str], query_embeddings: List[List[float]], result_queue: Queue):
    """Update search counts in popular_question collection based on query similarity."""
    try:
        collection = db["qna"]
        popular_collection = db["popular_question"]

        for sub_query, query_embedding in zip(sub_questions, query_embeddings):
            results = fetch_answers_from_db(collection, query_embedding)
            if results:
                best_result = results[0]
                distance = 1 - best_result["score"]
                if distance < 0.3:  # Exact match threshold
                    question = best_result["question"]
                    popular_collection.update_one(
                        {"question": question},
                        {
                            "$inc": {"search_count": 1},
                            "$setOnInsert": {"question": question}
                        },
                        upsert=True
                    )

        result_queue.put(("success", "Search counts updated successfully"))
    except Exception as e:
        result_queue.put(("error", str(e)))