pipeline {
    agent any

    stages {

        stage('Run Test') {
    steps {
        sh '''
        docker run --rm \
        -v $(pwd):/app \
        -w /app \
        python:3.12 \
        bash -c "pip install -r requirements.txt && pytest"
        '''
    }
}

    }
}