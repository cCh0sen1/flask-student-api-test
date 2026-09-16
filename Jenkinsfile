pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check') {
            steps {
                sh '''
                pwd
                ls -la
                '''
            }
        }

        stage('Run Test') {
            steps {
                sh '''
                docker run --rm \
                -v ${WORKSPACE}:/app \
                -w /app \
                python:3.12 \
                bash -c "pip install -r requirements.txt && pytest"
                '''
            }
        }

    }
}