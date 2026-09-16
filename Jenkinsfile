pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/cCh0sen1/flask-student-api-test.git'
            }
        }

        stage('Check Directory') {
    steps {
        sh '''
        pwd
        ls -la
        find . -maxdepth 2 -name requirements.txt
        '''
    }
}

    }
}