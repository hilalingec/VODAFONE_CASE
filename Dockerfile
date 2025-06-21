FROM python:3.11

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./app /code/app
COPY ./tests /code/tests

ENV PYTHONPATH=/code

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]