# data_preprocess/prepare_data.py
import glob
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")

# Initialize MongoDB client
mongo_client = MongoClient(mongo_uri)
db = mongo_client[db_name]
qna_collection = db["qna"]

# Initialize LangChain embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# === GET LANGCHAIN EMBEDDING ===
def get_langchain_embedding(text):
    try:
        return embedding_model.embed_query(text)
    except Exception as e:
        print(f"Embedding error: {e}")
        return [0.0] * 384  # Fallback vector (384 dimensions)

# === STEP 1: READ EXCEL FILES ===
all_files = glob.glob("data/client_data/*.xlsx")
print("Found Excel files:", all_files)

df_list = []
for file in all_files:
    try:
        xl = pd.ExcelFile(file)
        sheet_name = xl.sheet_names[0]
        df = xl.parse(sheet_name)
        print(f"Processing: {file}, Sheet: {sheet_name}")

        # Normalize column names
        df.columns = [col.strip().lower() for col in df.columns]
        if "questions" in df.columns and "chat bot reply" in df.columns:
            df_filtered = df[["questions", "chat bot reply"]].copy()
            df_filtered.columns = ["Questions", "Chat Bot Reply"]
            df_list.append(df_filtered)
        else:
            print(f"Skipped {file}: Required columns not found")
    except Exception as e:
        print(f"Error reading {file}: {e}")

# === STEP 2: CLEAN + SAVE CSV ===
if not df_list:
    raise Exception("No valid Excel files to process.")

combined_df = pd.concat(df_list, ignore_index=True)
combined_df["Questions"] = combined_df["Questions"].str.lower().str.strip()
combined_df.drop_duplicates(subset="Questions", inplace=True)
combined_df.to_csv("qna_dataset.csv", index=False)
combined_df["question"] = combined_df["Questions"].str.lower()
print("Chatbot data cleaned successfully!")

# === STEP 3: GENERATE EMBEDDINGS ===
questions = combined_df["Questions"].tolist()
embeddings = []
print("Generating embeddings...")
for i in range(0, len(questions), 4):
        batch = questions[i:i + 4]
        batch_embeddings = [get_langchain_embedding(q) for q in batch]
        embeddings.extend(batch_embeddings)
print("Embeddings generated successfully.")

# === STEP 4: INITIALIZE COLLECTIONS AND LOAD INTO MONGODB ===
print("Initializing MongoDB collections...")
print("Connecting to MongoDB...")
qna_collection.drop()

# Prepare documents
documents = [
    {
        "question": row.Questions,
        "answer": row._2,
        "normalized_question": row.Questions.lower(),
        "question_embedding": embedding
    }
    for row, embedding in zip(combined_df.itertuples(), embeddings)
]

# Batch insert into MongoDB
qna_collection.insert_many(documents)
print("✅ Data loaded into MongoDB successfully.")

mongo_client.close()