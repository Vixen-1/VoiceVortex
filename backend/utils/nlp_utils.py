# utils/nlp_utils.py
from typing import List, Dict, Any
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_sub_questions(query: str) -> List[str]:
    doc = nlp(query)
    sub_questions = []

    sentences = [sent.text.strip() for sent in doc.sents]

    for sent in sentences:
        sent_doc = nlp(sent)
        clauses = []
        current_clause = []

        for token in sent_doc:
            if token.lower_ in ["and"]:
                if current_clause:
                    clauses.append(" ".join(current_clause).strip())
                    current_clause = []
            else:
                current_clause.append(token.text)

        if current_clause:
            clauses.append(" ".join(current_clause).strip())

        for clause in clauses:
            clause = clause.lower().strip()
            if clause and clause not in sub_questions:
                sub_questions.append(clause)

    return sub_questions if sub_questions else [query.lower().strip()]

def fetch_answers_from_db(collection, embedding: List[float]) -> List[Dict[str, Any]]:
    results = collection.aggregate([
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "question_embedding",
                "queryVector": embedding,
                "numCandidates": 100,
                "limit": 5
            }
        },
        {
            "$project": {
                "question": 1,
                "answer": 1,
                "score": {"$meta": "vectorSearchScore"},
                "_id": 0
            }
        }
    ])
    return list(results)

def analyze_results(sub_query: str, results: List[Dict[str, Any]]) -> Dict[str, Any]:
    if results:
        best_result = results[0]
        distance = 1 - best_result["score"]
        if distance < 0.3:
            return {
                "question": sub_query,
                "answer": best_result["answer"],
                "type": "exact"
            }
        else:
            possible_questions = [
                {"question": r["question"], "distance": 1 - r["score"]}
                for r in results if (1 - r["score"]) < 0.5
            ]
            if possible_questions:
                return {
                    "question": sub_query,
                    "answer": "Multiple possible matches found. Please select or rephrase your question.",
                    "type": "ambiguous",
                    "suggestions": possible_questions
                }
    return {
        "question": sub_query,
        "answer": "Sorry, I couldn't find an answer for this question.",
        "type": "no_match"
    }