pipeline {
    agent any
    environment {
        POSTGRES_PASSWORD = credentials('POSTGRES_PASSWORD')
        POSTGRES_USER = credentials('POSTGRES_USER')
        POSTGRES_DBNAME = credentials('POSTGRES_DBNAME')
        POSTGRES_HOST = credentials('POSTGRES_HOST')
        REACT_APP_BACKEND_URL = credentials('REACT_APP_BACKEND_URL')
        AES_ENCRYPTION_KEY = credentials('AES_ENCRYPTION_KEY')
        AES_INITIALISATION_VECTOR = credentials('AES_INITIALISATION_VECTOR')
        JWT_SECRET_KEY = credentials('JWT_SECRET_KEY')
        PATH = "/usr/local/bin:${env.PATH}"
    }
    stages {
        stage('Clone Project Repository') {
            steps {
                git url: 'https://github.com/ctrltan/react-flask-note-app.git', branch: 'main'
            }
        }
        /* stage('Login to Docker') {
            steps {
                withCredentials([usernamePassword(credentialsId:'dockerHubLogin', passwordVariable:'dockerHubPassword', usernameVariable:'dockerHubUser')]) {
                    sh 'echo "Logging into Docker Hub..."'
                    sh "docker login -u ${env.dockerHubUser} -p ${env.dockerHubPassword} --password-stdin"
                }
            }
        } */
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
                        sh 'env | grep POSTGRES || true'
                        sh 'docker compose -f compose.defaultdb.yml -f compose.test.yml up --build -d'
                        sh 'docker compose -f compose.test.yml exec backend env | grep POSTGRES'
                        sh 'docker compose -f compose.test.yml exec db env | grep POSTGRES'
                        sh 'docker compose -f compose.defaultdb.yml ps'
                        sh 'docker compose -f compose.test.yml exec backend pytest -s'
                    } catch (err) {
                        sh 'echo "Tests failed uh oh"'
                    } finally {
                        sh 'docker compose -f compose.defaultdb.yml -f compose.test.yml down'
                    }
                }
            }
        }
        stage('Push Images to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId:'dockerHubLogin', passwordVariable:'dockerHubPassword', usernameVariable:'dockerHubUser')]) {
                    sh 'echo "Logging into Docker Hub..."'
                    sh "docker login -u ${env.dockerHubUser} -p ${env.dockerHubPassword}"
                    sh 'echo "Pushing images to Docker Hub"'
                    sh 'docker push st333phanie/react-flask-note-app-backend:latest'
                    sh 'docker push st333phanie/react-flask-note-app-frontend:latest'
                }
            }
        }
    }
    post {
        always {
            sh 'docker logout'
        }
    }
}
