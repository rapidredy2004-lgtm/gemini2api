FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY gemini_web2api/ ./gemini_web2api/
COPY config.example.json ./config.example.json
COPY render_start.py ./render_start.py
EXPOSE 8081

CMD ["python", "render_start.py"]
