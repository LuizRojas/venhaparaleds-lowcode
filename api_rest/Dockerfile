FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

EXPOSE 5000

# p/ iniciar a aplicação usando Gunicorn (servidor WSGI)
# usando gunicorn por se recomendado para servir aplicações Flask em produção
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
