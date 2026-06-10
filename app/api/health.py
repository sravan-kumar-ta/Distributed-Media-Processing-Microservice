from fastapi import APIRouter

from app.services.redis_service import redis_client
from app.storage.factory import get_storage

import pika

router = APIRouter()


@router.get("/health")
def health():

    health_status = {
        "status": "ok",
        "redis": "unknown",
        "rabbitmq": "unknown",
        "storage": "unknown",
    }

    # Redis
    try:
        redis_client.ping()
        health_status["redis"] = "connected"
    except Exception:
        health_status["redis"] = "failed"

    # RabbitMQ
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host="rabbitmq",
                credentials=pika.PlainCredentials(
                    "media",
                    "password123",
                ),
            )
        )

        connection.close()

        health_status["rabbitmq"] = "connected"

    except Exception as exc:
        health_status["rabbitmq"] = f"failed: {exc}"

    # Storage
    try:
        storage = get_storage()

        health_status["storage"] = storage.__class__.__name__

    except Exception:
        health_status["storage"] = "failed"

    return health_status
