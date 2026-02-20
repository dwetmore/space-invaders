# Space Invaders

## What it is
A Pygame-based game project packaged for local play and Kubernetes-hosted browser access.

## What it does
- Runs the classic Space Invaders loop with tuned gameplay progression.
- Supports container build and deployment to MicroK8s.
- Exposes remote gameplay through noVNC in browser-capable environments.

## Why it matters
It shows that interactive graphical apps can follow the same CI/CD and GitOps discipline as backend services.

A simple Space Invaders game built with Pygame.

## Run

```bash
pip install pygame
python3 main.py
```

## Deploy To MicroK8s

```bash
docker build -t localhost:32000/space-invaders:latest .
docker push localhost:32000/space-invaders:latest
microk8s kubectl apply -f k8s/deployment.yaml
microk8s kubectl get pods -l app=space-invaders
```

Open in browser:

```bash
http://localhost:30080/vnc.html
```
