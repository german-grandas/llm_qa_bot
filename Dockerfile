
FROM python:3.11-slim

RUN pip install poetry

WORKDIR /server

COPY pyproject.toml poetry.lock /server/
COPY scripts/entrypoint.sh /entrypoint.sh

RUN poetry install --only main

COPY ./server/ /server/

EXPOSE ${CHAT_PORT} ${API_PORT} ${STREAMLIT_PORT}

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
