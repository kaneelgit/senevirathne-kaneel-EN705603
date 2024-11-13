FROM python:3.10-slim

WORKDIR /textwave

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3001

CMD ["python", "app.py"]