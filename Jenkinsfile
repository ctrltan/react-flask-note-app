pipeline {
    agent any
    stages {
        stage('Clone Project Repository') {
            steps {
                git 'https://github.com/ctrltan/react-flask-note-app.git'
            }
        }
        stage('Build Docker Images') {
            steps {
                sh 'echo "Building backend image..."'
                sh 'docker build -t st333phanie/react-flask-note-app-backend:latest -f backend/Dockerfile backend'

                sh 'echo "Building frontend image..."'
                sh 'docker build -t st333phanie/react-flask-note-app-frontend:latest -f frontend/Dockerfile frontend'
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    try {
                        sh 'docker compose -f compose.db.yml -f compose.test.yml up -d'
                        sh 'docker compose exec backend pytest -s'
                    } finally {
                        sh 'docker compose down'
                    }
                }
            }
        }
        stage('Push Images to Docker Hub') {

        }
    }
}