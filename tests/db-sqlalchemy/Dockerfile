FROM python:3.12-slim

WORKDIR /app

ENV TEST_PATH=tests/db-sqlalchemy

COPY ${TEST_PATH}/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ${TEST_PATH} .

COPY backend /app/backend

CMD ["pytest", "-v"]
