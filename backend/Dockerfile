FROM python:3.10-slim
 
WORKDIR /app
 
COPY . /app
 
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
 
EXPOSE 8000
 
ENV UVICORN_CMD="uvicorn main:app --host 0.0.0.0 --port 8001 --reload"
 
CMD ["sh", "-c", "$UVICORN_CMD"]