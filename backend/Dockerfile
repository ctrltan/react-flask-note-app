FROM python:3.11-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD [ "python", "-m", "note_app.server" ]