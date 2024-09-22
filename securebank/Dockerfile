FROM python:3.10-slim

WORKDIR /securebank

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install pyarrow

RUN pip install fastparquet

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
