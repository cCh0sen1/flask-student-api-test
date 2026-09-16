pipeline {
    agent any

    stages {

        stage('Test') {
            steps {
                sh '''
                docker run --rm \
                -v /workspace:/app \
                -w /app \
                python:3.12 \
                bash -c "pip install -r requirements.txt && pytest"
                '''
            }
        }

    }
}