pipeline {
    agent any
    environment {
        POSTGRES_PASSWORD = credentials('POSTGRES_PASSWORD')
        POSTGRES_USER = credentials('POSTGRES_USER')
        POSTGRES_DBNAME = credentials('POSTGRES_DBNAME')
        POSTGRES_HOST = credentials('POSTGRES_HOST')
        REACT_APP_BACKEND_URL = credentials('REACT_APP_BACKEND_URL')
        PATH = "/usr/local/bin:${env.PATH}"
    }
    stages {
        stage('Clone Project Repository') {
            steps {
                git url: 'https://github.com/ctrltan/react-flask-note-app.git', branch: 'main'
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
                        sh 'docker compose ps'
                        sh 'docker compose exec backend pytest -s'
                    } finally {
                        sh 'echo "Tests failed"'
                        sh 'docker compose down'
                    }
                }
            }
        }
        stage('Push Images to Docker Hub') {
            steps {
                withCredentials([userNamePassword(credentialsId:'dockerHubLogin', passwordVariable:'dockerHubPassword', usernameVariable:'dockerHubUser')]) {
                    sh 'echo "Logging into Docker Hub..."'
                    sh 'docker login -u ${env.dockerHubUser} -p ${env.dockerHubPassword}'
                    sh 'echo "Pushing images to Docker Hub"'
                    sh 'docker push st333phanie/react-flask-note-app-backend:latest'
                    sh 'docker push st333phanie/react-flask-note-app-frontend:latest'
                }
            }
        }
    }
}
post {
    always {
        sh 'docker logout'
    }
}
