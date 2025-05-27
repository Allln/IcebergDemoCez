FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY cli.py .
ENTRYPOINT ["python", "cli.py"]
