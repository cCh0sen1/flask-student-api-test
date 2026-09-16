pipeline {
    agent any

    stages {

        stage('Verify workspace') {
            steps {
                sh '''
                test -f "$WORKSPACE/requirements.txt"
                ls -la "$WORKSPACE"
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                docker run --rm \
                --volumes-from jenkins \
                --workdir "$WORKSPACE" \
                python:3.12-slim \
                sh -lc "pip install -r requirements.txt && pytest"
                '''
            }
        }

    }
}