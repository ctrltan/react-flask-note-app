FROM --platform=linux/amd64 python:3.11-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=8000
EXPOSE 8000
CMD sh -c "celery -A note_app.make_celery worker --loglevel INFO --pool=solo & exec gunicorn --bind 0.0.0.0:${PORT} 'note_app.server:create_app()'""
