pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/cCh0sen1/flask-student-api-test.git'
            }
        }

        stage('Run Test') {
            steps {
                sh '''
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