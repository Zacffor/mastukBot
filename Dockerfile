-python:3.11-slim

WORKDIR /app

COPY requirements.txt
RUN pip install --nopip -r requirements.txt

COPY . .

CMD ["paborts, "main.py"]