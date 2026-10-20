pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('GitHub Checkout') {
            steps {
                echo 'GitHub source code loaded'
                checkout scm
            }
        }

        stage('Check Environment') {
            steps {
                sh '''
                    python3 --version
                    git --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Python Syntax Check') {
            steps {
                sh '''
                    . .venv/bin/activate
                    python -m compileall -q app database
                '''
            }
        }

        stage('Automated Tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    mkdir -p reports
                    python -m pytest -v tests


