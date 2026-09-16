pipeline {
    agent any

    stages {

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