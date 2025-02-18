import os
import faiss
import time
from google.cloud import storage
from fastapi import FastAPI, Query
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import uvicorn
import numpy as np
import json
import openai

# Google Cloud Storage details
BUCKET_NAME = "arize_rag"
FAISS_INDEX_FILE = "faiss_index"
LOCAL_FAISS_PATH = "/tmp/faiss_index_local.idx"  # Temporary local path
LOGS_FILE = "processed_network_logs.json"
logs_mapping = {}

try:
    with open(LOGS_FILE, "r") as f:
        logs_data = json.load(f)
        logs_mapping = {i: log["text"] for i, log in enumerate(logs_data)}
        print(f"Loaded {len(logs_mapping)} logs into memory.")
except FileNotFoundError:
    print("Logs file not found! Make sure 'processed_network_logs.json' exists.")

app = FastAPI()
faiss_index = None


@app.on_event("startup")
async def load_faiss():
    """Downloads FAISS index from GCS and loads it into memory asynchronously."""
    global faiss_index
    print("📥 Downloading FAISS index from GCS...")

    start_time = time.time()
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(FAISS_INDEX_FILE)

    blob.download_to_filename(LOCAL_FAISS_PATH)
    print(f"✅ FAISS index downloaded in {time.time() - start_time:.2f} seconds.")

    start_time = time.time()
    faiss_index = faiss.read_index(LOCAL_FAISS_PATH)
    print(f"✅ FAISS index loaded in {time.time() - start_time:.2f} seconds.")

openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is missing!")
print(f"✅ OpenAI API Key Loaded: {openai_api_key[:5]}...")

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=openai_api_key)

@app.get("/query")
async def query_security_logs(query: str = Query(..., description="Security-related query")):
    """Retrieve relevant network logs based on a security query and analyze them using GPT-4."""
    global faiss_index
    print(f"Received query: {query}")

    if faiss_index is None:
        return {"error": "FAISS index is still loading. Please try again in a few seconds."}

    # Convert query into an embedding
    query_vector = np.array(embedding_model.embed_query(query))

    # Search FAISS index
    _, indices = faiss_index.search(query_vector.reshape(1, -1), k=100)  # Retrieve top 10 logs

    # Extract log texts
    retrieved_logs = [logs_mapping.get(int(i), "Log not found.") for i in indices[0] if i >= 0]
    
    # Format logs for GPT
    formatted_logs = "\n".join(retrieved_logs)

    # GPT prompt
    gpt_prompt = f"""
    You are a cybersecurity expert analyzing network logs.
    The user asked: "{query}"

    Here are the most relevant network logs:
    {formatted_logs}

    Based on the logs, do you detect any suspicious activity? Provide a brief explanation.
    """

    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": "You are a security analyst."},
                  {"role": "user", "content": gpt_prompt}]
    )

    gpt_analysis = response.choices[0].message.content

    # Return only the analysis, not the logs.
    return {"query": query, "gpt_analysis": gpt_analysis}



if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)
