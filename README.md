# FastApi-Gateway

## Описание

Этот проект реализует шлюз на FastAPI, который фильтрует запросы и распределяет их равномерно на конечный сервис. Шлюз использует Celery для обработки задач, Redis в качестве кеша приложения и RabbitMQ в качестве брокера задач.

## Запуск проекта

### Запуск RabbitMQ

```powershell
docker run -d --rm --name rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management
```
### Запуск Redis

```powershell
docker run -d --rm --name redis -p 6379:6379 redis:latest
```

### Запуск Worker

```powershell
celery -A gateway.tasks worker -Q github -c 8 -l info -P eventlet -n worker1@%h
```

### Запуск Flower

```powershell
celery -A gateway.tasks flower
```

### Запуск beat

```powershell
celery -A gateway.tasks beat —loglevel=info
```

### Запуск gateway

```powershell
py ./gateway/main.py
```

### Запуск ping

```powershell
py ./ping/main.py
```

### Запуск pong

```powershell
py ./pong/main.py
```
