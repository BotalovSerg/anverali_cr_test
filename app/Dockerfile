FROM python:3.11-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY . /code/
CMD ["python3", "main.py"]