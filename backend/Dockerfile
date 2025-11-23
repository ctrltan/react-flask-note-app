FROM --platform=linux/amd64 python:3.11-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "note_app.server:create_app()" ]