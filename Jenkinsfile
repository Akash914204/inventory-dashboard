pipeline {
    agent any

    environment {
        IMAGE_NAME = "inventory-dashboard"
        CONTAINER_NAME = "inventory-dashboard-container"
        PORT = "5000"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/Akash914204/inventory-dashboard.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Stop old container if running
                    sh "docker rm -f ${CONTAINER_NAME} || true"
                    // Run new container
                    sh "docker run -d --name ${CONTAINER_NAME} -p ${PORT}:${PORT} ${IMAGE_NAME}:latest"
                }
            }
        }

        stage('Health Check') {
            steps {
                script {
                    sh "sleep 5"
                    sh "curl -f http://127.0.0.1:${PORT} || echo 'App not reachable'"
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished!'
        }
    }
}
