from fastapi import HTTPException
import google.generativeai as genai
from Configuration.config import Api_key

genai.configure(api_key=Api_key)

def get_gemini_embeddings(texts):
    try:
        embeddings = []
        for text in texts:
            response = genai.embed_content(
                model="models/text-embedding-004",
                content=text,
                task_type="retrieval_document"
            )
            embedding = response["embedding"]
            if len(embedding) != 768:
                raise ValueError(f"Embedding for '{text}' has length {len(embedding)}, expected 768")
            embeddings.append(embedding)
        return embeddings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")

def format_answer_with_gemini(answers, original_query):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
You are given a list of answers to sub-questions related to a user query: '{original_query}'.
 
Your task is to format these answers into a clear and well-structured markdown response with the following rules:
 
1. **General Formatting**:
   - Use **bold headings** for different topics or sections.
   - Use **bullet points** to list out key information or steps.
   - Use proper **markdown syntax** (e.g., `**` for bold text).
   - Do not use bullet point if there is only single point and with the bold headings
 
2. **Answer Grouping**:
   - If multiple sub-questions have related answers, combine them into a single cohesive section.
   - If there's only one answer, add a relevant heading and use bullet points for the content if applicable.
 
3. **Special Cases**:
   - If an answer contains `"no_match"` or `"ambiguous"`, explicitly state this.
   - For ambiguous answers, **do not include** the suggestions (possible questions) in the response, as they will be handled separately.
   - For ambiguous answers, only include the message (e.g., "Multiple possible matches found. Please select or rephrase your question.").
 
4. **Important Notes**:
   - Do **not** use the original query as a heading.
   - Do **not** add or infer any content on your own—only format the provided data.
   - Keep the structure clean, readable, and concise.
 
Answers:
{answers}
 
Return the final result in **markdown format** only.
"""
 
        response = model.generate_content(prompt)
        print(response)
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini formatting error: {str(e)}")