# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Streamlit port
EXPOSE 8080

# Run Streamlit app
CMD ["streamlit", "run", "app_ui.py", "--server.port=8080", "--server.address=0.0.0.0"]
