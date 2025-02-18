# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy only requirements first to leverage Docker's caching mechanism
COPY requirements.txt .

# Install system dependencies & Python packages
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the project files
COPY . .

# Expose the FastAPI port
EXPOSE 8080  

# Run FastAPI with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
