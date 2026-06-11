# Distributed Media Processing Microservice

This project demonstrates how media processing can be handled by a dedicated microservice instead of the main application.

When users upload images or videos, tasks such as image resizing, thumbnail generation, video compression, metadata extraction, and watermarking can be CPU-intensive and time-consuming. Running these operations directly inside the main application can slow down requests and affect user experience.

To solve this, the main application creates a processing job and sends it to a queue. A separate media processing service consumes the job, processes the file, and stores the result. This allows the main application to respond immediately while heavy processing happens in the background.

The project uses FastAPI, Celery, RabbitMQ, Redis, FFmpeg, Pillow, and S3/Local Storage to build an asynchronous and scalable media processing pipeline.

## Architecture

```text
Client
   |
FastAPI
   |
RabbitMQ
   |
Celery Worker
   |
Media Processing
(Pillow / FFmpeg)

Redis
   |
Job Tracking

Storage
├── Local Storage
└── Amazon S3
```

## Features

- Image resize
- Image thumbnail generation
- Image watermarking
- Video thumbnail generation
- Video metadata extraction
- Video compression
- Audio extraction
- Asynchronous processing using Celery
- Job status tracking using Redis
- Local or S3-based file storage
- Docker Compose deployment

---

# Prerequisites

Install:

- Docker
- Docker Compose

Verify:

```bash
docker --version
docker compose version
```

---

# Environment Variables

Create `.env`

```env
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=ap-south-1
AWS_BUCKET_NAME=your_bucket

BROKER_URL=amqp://media:password123@rabbitmq:5672//
REDIS_URL=redis://redis:6379/0
```

---

# Running with Docker Compose

Build and start all services:

```bash
docker compose up --build
```

Services:

| Service     | Port  |
| ----------- | ----- |
| FastAPI     | 8000  |
| RabbitMQ    | 5672  |
| RabbitMQ UI | 15672 |
| Redis       | 6379  |

Open Swagger:

```text
http://localhost:8000/docs
```

Open RabbitMQ Dashboard:

```text
http://localhost:15672
```

Credentials:

```text
Username: media
Password: password123
```

---

# Running Without Docker

## Start Redis

```bash
redis-server
```

## Start RabbitMQ

```bash
sudo systemctl start rabbitmq-server
```

## Start Celery Worker

```bash
celery -A app.core.celery_app worker --loglevel=info
```

## Start FastAPI

```bash
uvicorn app.main:app --reload
```

---

# API Usage

## Upload File

```http
POST /upload
```

Response:

```json
{
  "file_id": "123"
}
```

---

## Create Job

```http
POST /jobs
```

Example:

```json
{
  "file_id": "123",
  "operation": "thumbnail"
}
```

---

## Check Job Status

```http
GET /jobs/{job_id}
```

Example Response:

```json
{
  "job_id": "...",
  "status": "completed",
  "result_path": "processed/file.jpg",
  "download_url": "/jobs/{job_id}/download"
}
```

---

## Download Result

```http
GET /jobs/{job_id}/download
```

---

# Supported Operations

## Image

```text
resize
thumbnail
watermark
```

## Video

```text
video_thumbnail
video_metadata
video_compress
audio_extract
```

# Storage Modes

## Local Storage

Files stored under:

```text
storage/
├── uploads/
└── processed/
```

## S3 Storage

Files stored inside configured S3 bucket.

Example:

```text
uploads/abc.jpg
processed/job123.jpg
```

---

# Project Structure

```text
app/
├── api/
├── core/
├── schemas/
├── services/
├── storage/
├── tasks/
│   ├── handlers/
│   ├── registry.py
│   └── process_job.py
└── main.py
```

---

# Future Improvements

- Scheduled Cleanup Task using celery beat
- PostgreSQL as source of truth
- Prometheus monitoring
- Grafana dashboards
- JWT Authentication
- Multi-user support
- Kubernetes deployment
- Distributed worker scaling

---

# License

For educational and portfolio purposes.
