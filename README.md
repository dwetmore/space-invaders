# Space Invaders

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
microk8s kubectl apply -f k8s/pod.yaml
microk8s kubectl get pod space-invaders
```
