pipeline {
  agent any
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Install Dependencies') { steps { sh 'python3 -m venv .venv && .venv/bin/pip install -r requirements.txt' } }
    stage('Lint') { steps { sh '.venv/bin/flake8 app database --select=E9,F63,F7,F82' } }
    stage('Tests') { steps { sh 'mkdir -p reports && .venv/bin/pytest -v --cov=app --junitxml=reports/test-results.xml tests/' } }
    stage('Docker Build') { steps { sh 'docker build -t student-academic-platform:v1.0.0 .' } }
    stage('Minikube Deploy') {
      when { expression { return env.ENABLE_MINIKUBE == 'true' } }
      steps { sh 'minikube image load student-academic-platform:v1.0.0 && kubectl apply -f k8s/ && kubectl rollout status deployment/student-academic-deployment --timeout=120s' }
    }
  }
  post { always { junit allowEmptyResults: true, testResults: 'reports/test-results.xml' } }
}
