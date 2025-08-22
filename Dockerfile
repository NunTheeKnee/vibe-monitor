FROM python:3.12-slim-bookworm

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY server.py .
EXPOSE 5000
ENTRYPOINT ["python3", "server.py"]