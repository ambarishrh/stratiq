FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY server.py .
COPY stratiq_8.html .

EXPOSE 3000

CMD ["python", "server.py"]
