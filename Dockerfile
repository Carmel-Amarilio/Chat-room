#Carmel & Max
FROM python:3.9-slim 

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY chat-backend.py /app/
COPY templates /app/templates/

EXPOSE 5000

ENV FLASK_APP=chat-backend.py
ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]


