FROM python:3.9-slim

WORKDIR /spectate_rest_app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./spectate_rest_app ./spectate_rest_app

EXPOSE 8000

RUN python spectate_rest_app/create_tables.py

CMD ["uvicorn", "spectate_rest_app.main:app", "--host", "0.0.0.0", "--port", "8000"]