# Security Log Analytics - Backend (FastAPI)

## Overview
This is the backend service for the **Security Log Analytics Assistant**, a tool that enables querying of security-related network logs using **FAISS** for retrieval and **GPT-4-turbo** for analysis.

## Features
- **Retrieval-Augmented Generation (RAG)** using **FAISS** for efficient log search.
- **FastAPI** for a lightweight and scalable API.
- **Google Cloud Run** deployment for cloud accessibility.

## Setup Instructions

### 1️⃣ Install Dependencies
```sh
cd backend
pip install -r requirements.txt
