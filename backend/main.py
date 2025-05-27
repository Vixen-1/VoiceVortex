from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from psycopg2.extras import RealDictCursor
import google.generativeai as genai
import re
from gemini_function.prompt import format_answer_with_gemini, get_gemini_embeddings
from utils.nlp_utils import extract_sub_questions, fetch_answers_from_db, analyze_results
from models.pydantic import QueryRequest
from Configuration.config import db_pool, Api_key

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
genai.configure(api_key=Api_key)

# List of gratitude patterns (case-insensitive)
GRATITUDE_PATTERNS = [
    r"\bthanks?\b",
    r"\bthank you\b",
    r"\bappreciate\b",
    r"\bgrateful\b",
    r"\bcheers\b",
    r"\bty\b",
]

# List of greeting patterns (case-insensitive)
GREETING_PATTERNS = [
    r"\bhi\b",
    r"\bhii\b",
    r"\bhello\b",
    r"\bhey\b",
    r"\bhowdy\b",
    r"\bgreetings?\b",
    r"\bheya?\b",
    r"\bwhat'?s up\b",
    r"\bsup\b",
]

@app.post("/api/chatbot/chat")
async def ask_question(request: QueryRequest):
    query = request.message

    query_lower = query.lower().strip()
    if any(re.search(pattern, query_lower) for pattern in GREETING_PATTERNS):
        return {
            "answers": f"Welcome! How can I assist you today?",
            "ambiguous_data": []
        }
    if any(re.search(pattern, query_lower) for pattern in GRATITUDE_PATTERNS):
        return {
            "answers": f"Happy to help! Please let me know if further help is needed.",
            "ambiguous_data": []
        }

    try:
        # Extract sub-questions
        sub_questions = extract_sub_questions(query)

        # Generate embeddings inline
        query_embeddings = get_gemini_embeddings(sub_questions)

        conn = db_pool.getconn()

        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            answers = []
            ambiguous_data = []

            for sub_query, query_embedding in zip(sub_questions, query_embeddings):
                results = fetch_answers_from_db(cursor, query_embedding)
                answer = analyze_results(sub_query, results)
                # Collect ambiguous suggestions
                if answer["type"] == "ambiguous":
                    ambiguous_data.extend([s["question"] for s in answer.get("suggestions", [])])
                answers.append(answer)

            # Format final response inline
            formatted_response = format_answer_with_gemini(answers, query)
            return {
                "answers": formatted_response,
                "ambiguous_data": ambiguous_data
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        finally:
            cursor.close()
            db_pool.putconn(conn)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")