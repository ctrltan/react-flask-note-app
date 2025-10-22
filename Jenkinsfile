pipeline {
    agent any
    environment {
        POSTGRES_PASSWORD = credentials('POSTGRES_PASSWORD')
        POSTGRES_USER = credentials('POSTGRES_USER')
        POSTGRES_DBNAME = credentials('POSTGRES_DBNAME')
        POSTGRES_HOST = credentials('POSTGRES_HOST')
        REACT_APP_BACKEND_URL = credentials('REACT_APP_BACKEND_URL')
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
                sh '/usr/local/bin/docker build -t st333phanie/react-flask-note-app-backend:latest -f backend/Dockerfile backend'

                sh 'echo "Building frontend image..."'
                sh 'usr/local/bin/docker build -t st333phanie/react-flask-note-app-frontend:latest -f frontend/Dockerfile frontend'
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    try {
                        withCredentials([string(credentialsId:'postgresPass', variable:'POSTGRES_PASSWORD')]) {
                            sh 'usr/local/bin/docker compose -f compose.db.yml -f compose.test.yml up -d'
                        }
                        sh 'usr/local/bin/docker compose exec backend pytest -s'
                    } finally {
                        sh 'echo "Tests failed"'
                        sh 'usr/local/bin/docker compose down'
                    }
                }
            }
        }
        stage('Push Images to Docker Hub') {
            steps {
                withCredentials([userNamePassword(credentialsId:'dockerHubLogin', passwordVariable:'dockerHubPassword', usernameVariable:'dockerHubUser')]) {
                    sh 'echo "Logging into Docker Hub..."'
                    sh 'usr/local/bin/docker login -u ${env.dockerHubUser} -p ${env.dockerHubPassword}'
                    sh 'echo "Pushing images to Docker Hub"'
                    sh 'usr/local/bin/docker push st333phanie/react-flask-note-app-backend:latest'
                    sh 'usr/local/bin/docker push st333phanie/react-flask-note-app-frontend:latest'
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