# main.py
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import re
from gemini_function.prompt import format_answer_with_langchain, get_langchain_embeddings
from utils.nlp_utils import extract_sub_questions
from models.pydantic import QueryRequest
from Configuration.config import db
import threading
from queue import Queue
from threads.search_count_thread import update_search_counts
from threads.answer_retrieval_thread import retrieve_answers
from pydantic import ValidationError
from utils.patterns import GRATITUDE_PATTERNS, GREETING_PATTERNS, FILLER_PHRASES
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

@router.post("/chat/")
async def ask_question(request: QueryRequest):
    try:
        query = request.question

        # Check if the query matches a greeting or gratitude pattern
        query_lower = query.lower().strip()
        if any(re.search(pattern, query_lower) for pattern in GREETING_PATTERNS):
            return {
                "answers": "Welcome! How can I assist you today?",
                "ambiguous_data": []
            }
        if any(re.search(pattern, query_lower) for pattern in GRATITUDE_PATTERNS):
            return {
                "answers": "Happy to help! Please let me know if you need further assistance.",
                "ambiguous_data": []
            }

        # Extract sub-questions
        sub_questions = extract_sub_questions(query)

        # Generate embeddings
        query_embeddings = get_langchain_embeddings(sub_questions)

        # Create queues for thread results
        search_count_queue = Queue()
        answer_queue = Queue()

        # Start threads
        search_thread = threading.Thread(
            target=update_search_counts,
            args=(sub_questions, query_embeddings, search_count_queue)
        )
        answer_thread = threading.Thread(
            target=retrieve_answers,
            args=(sub_questions, query_embeddings, answer_queue)
        )

        search_thread.start()
        answer_thread.start()

        # Wait for threads to complete
        search_thread.join()
        answer_thread.join()

        # Check search count thread result
        search_result = search_count_queue.get()
        if isinstance(search_result, tuple) and search_result[0] == "error":
            raise HTTPException(status_code=500, detail=f"Search count update error: {search_result[1]}")

        # Get answer thread result
        answer_result = answer_queue.get()
        if isinstance(answer_result, tuple) and answer_result[0] == "error":
            raise HTTPException(status_code=500, detail=f"Answer retrieval error: {answer_result[1]}")

        # Return formatted response
        return answer_result[1]

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/popular-questions/")
async def get_popular_questions():
    try:
        popular_questions = db["popular_question"].find(
            {},  # No filter needed
            {"question": 1, "_id": 0}
        ).sort("search_count", -1).limit(5)
        questions = [doc["question"] for doc in popular_questions]
        return {
            "popular_questions": questions,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.post("/search/")
async def search_question(request: QueryRequest):
    try:
        query = request.question.strip()

        logger.info(f"Searching for query: '{query}'")

        # Use qna collection
        collection = db["qna"]

        # Clean query: remove filler phrases
        query_lower = query.lower()
        for filler in FILLER_PHRASES:
            query_lower = re.sub(filler, " ", query_lower, flags=re.IGNORECASE)
        query_lower = re.sub(r"\s+", " ", query_lower).strip()

        # Split query into keywords, preserving known multi-word phrases
        keywords = []
        known_phrases = ["basic sourcing", "payment terms", "request for quotation", "rfq"]
        query_words = query_lower.split()
        i = 0
        while i < len(query_words):
            found_phrase = False
            for phrase in known_phrases:
                phrase_words = phrase.split()
                if i + len(phrase_words) <= len(query_words):
                    if " ".join(query_words[i:i + len(phrase_words)]) == phrase:
                        keywords.append(phrase)
                        i += len(phrase_words)
                        found_phrase = True
                        break
            if not found_phrase:
                keywords.append(query_words[i])
                i += 1

        # Filter out empty or irrelevant keywords
        keywords = [k.strip() for k in keywords if k.strip() and k not in ["some", "questions"]]
        if not keywords:
            logger.info("No valid keywords in query")
            return {"matching_questions": []}

        # Build MongoDB query
        query_filter = {
            "$and": [{"normalized_question": {"$regex": keyword, "$options": "i"}} for keyword in keywords]
        }
        results = collection.find(query_filter, {"question": 1, "_id": 0})
        questions = [doc["question"] for doc in results]
        logger.info(f"Found {len(questions)} matching questions")

        return {
            "matching_questions": questions
        }
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

app.include_router(router, prefix="/api")