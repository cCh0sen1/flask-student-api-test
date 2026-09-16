pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                deleteDir()
                checkout scm
            }
        }

        stage('Run Test') {
            steps {
                sh '''
                ls -la

                docker run --rm \
                -v ${WORKSPACE}:/app \
                -w /app \
                python:3.12 \
                bash -c "ls -la && pip install -r requirements.txt && pytest"
                '''
            }
        }

    }
}