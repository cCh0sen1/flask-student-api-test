pipeline {
    agent any

    options {
        timestamps()
    }

    stages {

        stage('Verify Docker') {
            steps {
                sh '''
                    set -eu
                    docker version
                    docker compose version
                '''
            }
        }


        stage('Build and Test') {
            steps {
                sh '''
                    set -eu
                    docker compose -p "student-api-${BUILD_NUMBER}" up \
                        --build \
                        --abort-on-container-exit \
                        --exit-code-from test
                '''
            }
        }

        stage('Publish Test Report') {
            steps {
                sh '''
                    set -eu
                    docker compose -p "student-api-${BUILD_NUMBER}" cp \
                        test:/app/test-result.xml test-result.xml
                '''
                junit 'test-result.xml'
            }
        }
    }


    post {
        always {
            sh '''
                docker compose -p "student-api-${BUILD_NUMBER}" down \
                    --volumes \
                    --remove-orphans || true
            '''
        }
    }
}
