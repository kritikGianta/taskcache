# TaskCache

A minimal backend project built with **FastAPI and Redis** to gain hands-on experience with Redis and its integration into real-world backend applications.

## 🚀 Tech Stack

* Python
* FastAPI
* Redis
* Docker
* Docker Compose

## ✨ Features

* REST API for task management
* Redis-based data storage
* Caching with TTL
* Cache hit/miss tracking
* Redis data structures
* Activity tracking
* Counters and statistics
* Basic rate limiting
* Dockerized development environment

## 🏗️ Architecture

```text
Client
  │
  ▼
FastAPI
  │
  ▼
Redis
 ├── Task Data
 ├── Cache
 ├── Statistics
 ├── Activity
 └── Rate Limiting
```

## ⚙️ Setup

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/taskcache.git
cd taskcache
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start Redis:

```bash
docker compose up -d
```

Run the application:

```bash
uvicorn app.main:app --reload
```

API documentation:

```text
http://localhost:8000/docs
```

## 🐳 Docker

Run the complete application using:

```bash
docker compose up --build
```

## 📚 Concepts Practiced

This project focuses on practical Redis concepts including:

* Caching
* TTL and expiration
* Redis data structures
* Counters
* Rate limiting
* Cache invalidation
* FastAPI + Redis integration
* Docker and Docker Compose

## 🎯 Purpose

The project is primarily a hands-on learning project designed to understand how Redis can be integrated into backend applications for fast data access, caching, temporary data, and other common use cases.

## 👨‍💻 Author

**Kritik Gianta**
