from celery import Celery

celery_app = Celery(
    "media_processor",
    broker="amqp://media:password123@localhost:5672//",
    backend="redis://localhost:6379/0",
    include=["app.tasks.process_job"],
)
