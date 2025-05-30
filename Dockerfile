FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --upgrade git+https://github.com/huggingface/transformers

COPY . .

EXPOSE 7860

CMD ["python", "app.py"]
