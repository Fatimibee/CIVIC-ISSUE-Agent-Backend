# 1. Use a Python base image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Install system dependencies (needed for PIL and ML libraries)
# 3. Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy requirements first to speed up rebuilds
COPY requirements.txt .
RUN pip install --no-cache-dir \
    --default-timeout=100 \
    -r requirements.txt

# 5. Copy everything from your root folder into /app
COPY . .

# 6. CRITICAL: Tell Python to treat /app as the root for imports
# This fixes "ModuleNotFoundError" for Agent, Core, etc.
ENV PYTHONPATH=/app

# 7. Expose the FastAPI port
EXPOSE 8000

# 8. Start the FastAPI server
# Syntax: uvicorn <FOLDER>.<FILE_NAME>:<VARIABLE_NAME>
CMD ["uvicorn", "App.app:app", "--host", "0.0.0.0", "--port", "8000"]