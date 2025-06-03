# threads/answer_retrieval_thread.py
from queue import Queue
from typing import List
from Configuration.config import db
from utils.nlp_utils import fetch_answers_from_db, analyze_results
from gemini_function.prompt import format_answer_with_langchain
import re
from utils.compute_text_similarity import compute_text_similarity
from utils.patterns import no_answer_patterns

def retrieve_answers(sub_questions: List[str], query_embeddings: List[List[float]], result_queue: Queue):
    """Retrieve and format answers from qna, logging unanswered questions to error_logs with similarity check."""
    try:
        collection = db["qna"]
        error_logs = db["error_logs"]
        answers = []
        ambiguous_data = []

        for sub_query, query_embedding in zip(sub_questions, query_embeddings):
            results = fetch_answers_from_db(collection, query_embedding)
            answer = analyze_results(sub_query, results)
            if answer["type"] == "ambiguous":
                ambiguous_data.extend([s["question"] for s in answer.get("suggestions", [])])
            answers.append(answer)

        # Format response
        formatted_response = format_answer_with_langchain(answers, " ".join(sub_questions))

        for sub_query, answer in zip(sub_questions, answers):
            if any(re.search(pattern, formatted_response, re.IGNORECASE) for pattern in no_answer_patterns):
                existing_questions = [doc["question"] for doc in error_logs.find({})]
                should_insert = True
                for existing_question in existing_questions:
                    similarity = compute_text_similarity(sub_query, existing_question)
                    if similarity >= 0.8:
                        should_insert = False
                        break
                if should_insert:
                    error_logs.insert_one({"question": sub_query})

        result_queue.put(("success", {"answers": formatted_response, "ambiguous_data": ambiguous_data}))
    except Exception as e:
        result_queue.put(("error", str(e)))