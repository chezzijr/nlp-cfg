FROM python:3.11.10-alpine

WORKDIR /nlp
ENV ROOT=/nlp
ENV S_OUT=/nlp/output

COPY . .
RUN python -m venv .venv \
    && source .venv/bin/activate \
    && pip install -r requirements.txt
CMD [".venv/bin/python", "main.py"]
