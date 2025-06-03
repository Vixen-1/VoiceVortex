# gemini_function/prompt.py
from fastapi import HTTPException
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from Configuration.config import Hugging_Face_Api_key
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize LangChain embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Initialize Hugging Face LLM
try:
    llm = HuggingFaceHub(
        repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
        huggingfacehub_api_token=Hugging_Face_Api_key,
        model_kwargs={"temperature": 0.7, "max_length": 512}
    )
    logger.info("Hugging Face LLM initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Hugging Face LLM: {str(e)}")
    raise Exception(f"Hugging Face LLM initialization failed: {str(e)}")

def get_langchain_embeddings(texts):
    try:
        embeddings = []
        for text in texts:
            embedding = embedding_model.embed_query(text)
            if len(embedding) != 384:
                raise ValueError(f"Embedding for '{text}' has length {len(embedding)}, expected 384")
            embeddings.append(embedding)
        return embeddings
    except Exception as e:
        logger.error(f"Embedding error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Embedding error: {str(e)}")

def format_answer_with_langchain(answers, original_query):
    try:
        # Define prompt template
        prompt_template = PromptTemplate(
            input_variables=["answers", "original_query"],
            template="""
You are given a list of answers to sub-questions related to a user query: '{original_query}'.

Your task is to format these answers into a clear and well-structured markdown response with the following rules:

1. **General Formatting**:
   - Use **bold headings** for different topics or sections, except as specified below.
   - Use **bullet points** to list out key information or steps.
   - Use proper **markdown syntax** (e.g., `**` for bold text).
   - Do not use bullet points if there is only a single point under a bold heading.

2. **Single Answer Handling**:
   - If there is only one answer and it is **ambiguous**, return **exactly** this message without any heading: "Please provide more clarity or select from the options below."
   - If there is only one answer and it is **non-ambiguous**, add a relevant heading and format the content with bullet points if applicable.
   - If there is only one answer and it is **no_match**, add a relevant heading (e.g., "No Match Found") and state the message.

3. **Multiple Answer Handling**:
   - If multiple sub-questions have related **non-ambiguous** answers, combine them into a single cohesive section with a bold heading.
   - **Ambiguous answers must be treated as separate sections** with a relevant heading (e.g., "Basic Sourcing") and return **exactly** this message: "Please provide more clarity or select from the options below." **Do not modify, truncate, or combine this message with other answers.**
   - If an answer contains `"no_match"`, create a separate section with a heading and explicitly state the message.

4. **Special Cases**:
   - For ambiguous answers, **do not include** the suggestions (possible questions) in the response, as they will be handled separately.
   - For `"no_match"`, explicitly state the message (e.g., "No match found for this query.").

5. **Important Notes**:
   - Do **not** use the original query as a heading.
   - Do **not** add or infer any content on your own—only format the provided data.
   - Keep the structure clean, readable, and concise.
   - Ensure each sub-question's answer has its own section with a relevant heading for multiple answers, except for a single ambiguous answer.

Answers:
{answers}

Return the final result in **markdown format** only.
"""
        )

        # Create LLM chain
        chain = LLMChain(llm=llm, prompt=prompt_template)
        response = chain.run(answers=answers, original_query=original_query)
        logger.info("Answer formatted successfully")
        return response
    except Exception as e:
        logger.error(f"Formatting error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Formatting error: {str(e)}")