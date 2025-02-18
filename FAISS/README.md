### **FAISS Indexing (`FAISS/README.md`)**
```markdown
# Security Log Analytics - FAISS Indexing

## Overview
This module processes security log data and builds a **FAISS** vector index for fast retrieval. It generates embeddings using **text-embedding-3-small** and stores them in FAISS for efficient nearest-neighbor search.

## Features
- **FAISS-based similarity search** for fast and scalable log retrieval.
- **Google Cloud Storage (GCS)** integration for storing and retrieving the index.
- **LangChain + OpenAI embeddings** for RAG pipeline.

## Setup Instructions

### 1️⃣ Install Dependencies
```sh
cd FAISS
pip install -r requirements.txt
