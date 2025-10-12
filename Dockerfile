
# build this file with: docker build -t stock-price-assistant:1.0 .
# create and run the container with: docker run --name stock-price-assistant-container -p 8000:8000 --env-file .env stock-price-assistant:1.0
# start container with: docker start stock-price-assistant-container
# to see real-time logs after starting the container: docker logs -f stock-price-assistant-container
# stop container with: docker stop stock-price-assistant-container
# remove container with: docker rm stock-price-assistant-container
# 1. Base image
FROM python:3.11-slim

# 2. Set working directory inside container
WORKDIR /app

# 3. Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy app and model files
COPY src ./src

# 5. Expose port (FastAPI default)
EXPOSE 8000

# 6. Run the FastAPI app with Uvicorn
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

#6. use this instead since we are running application with run.py file:
CMD ["python", "-m", "src.main"]    
