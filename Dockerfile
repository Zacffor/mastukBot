-rython:3.11-slim

WORKDIR /app

COPY requirements.txt
RUN pip install --nopip -r requirements.txt

COPY . .

CMD ["python", "main.py"]