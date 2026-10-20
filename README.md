# Student Record & Academic Management Platform - DevOps Mini Project

**Student:** Om Laware | **PRN:** 2125UDSM1022 | **Department:** AIDS, Second Year

**Based on:** Unit assignment teaching material: Enterprise Smart Library Management Platform, student academic adaptation (Section 8). This repository is a separate example implementation, not an AWS-hosted deployment.

## Components
- Python Flask REST endpoints for students, courses, enrollment, grades and GPA
- Validation: maximum 18 enrolled credits per semester and duplicate enrollment prevention
- pytest unit/API tests, flake8, Dockerfile, Jenkinsfile, Kubernetes manifests (3 replicas, NodePort 30090)

## Quick run on macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v tests/
python run.py
```
Open http://127.0.0.1:5000/api/health in a second terminal.

## Docker (requires Docker Desktop)
```bash
docker build -t student-academic-platform:v1.0.0 .
docker run -d --name student-academic -p 5000:5000 student-academic-platform:v1.0.0
docker ps
curl http://127.0.0.1:5000/api/health
```

## Kubernetes (requires Docker Desktop + Minikube + kubectl)
```bash
minikube start --driver=docker
minikube image load student-academic-platform:v1.0.0
kubectl apply -f k8s/
kubectl get pods
kubectl get svc student-academic-service
minikube service student-academic-service --url
```

## GitHub upload (run after extraction)
```bash
gh auth status
git init
git branch -M main
git add .
git commit -m "Build student academic DevOps project"
gh repo create omlaware07-code/student-academic-devops --public --source=. --remote=origin --push
```

## Notes
Jenkins needs a configured Jenkins server/agent with Python, Docker, kubectl and Minikube. Merely including a Jenkinsfile does not prove a successful CI run. Keep real screenshots/logs from your own execution as evidence.
