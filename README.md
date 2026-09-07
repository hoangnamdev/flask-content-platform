# Flask Content Platform

Lightweight blog web application built with Python, Flask, SQLite, and Docker.

## Overview

This is a content management system made in Flask. It includes post creation, tagging, dynamic routing, image uploads, and session-based authentication for administrative actions.

## Tech Stack

- Python 3.11
- Flask (Web framework)
- Werkzeug (Password hashing and filename security)
- SQLite3 (Database)
- Gunicorn (WSGI HTTP server)
- Docker & Docker Compose (Containerization)

## Architectural Choices

### SQLite and Local Static Storage
The scope of the project is intentionally kept small and self-contained, relying on an embedded SQLite database and local static file storage (`static/assets/`). This approach avoids introducing third-party cloud database services, which are unnecessary external overheads.

The benefits are:
- Minimal, easy-to-maintain configuration.
- Low resource usage.

### Security Implementation
Security features are kept simple and practical:

- Parameterized SQL Queries: Parameter binding prevents SQL injection.
- Password Hashing: Relies on Werkzeug's cryptographic password hashing.
- File Upload Sanitization: Processed with `secure_filename()`, preventing path traversal attacks.
- Session Protection: Administrative routes protected with `@login_required` decorator.
- Cache Headers: HTTP response headers prevent proxy caching on sensitive pages.

### Containerization
The application is containerized with Docker and Docker Compose to ensure deployment consistency and easy setup across environments.

## Getting Started

### Using Docker Compose (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/hoangnamdev/flask-content-platform
   cd flask-content-platform
   ```

2. Start the application:
   ```bash
   docker-compose up -d --build
   ```

3. Open `http://localhost:5000` in your web browser.

### Running Locally

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the app:
   ```bash
   python app.py
   ```

## Project Structure

```text
.
├── app.py              # Application routes and logic
├── blogposts.db        # SQLite database
├── Dockerfile          # Container definition
├── docker-compose.yml  # Docker service and volume configuration
├── requirements.txt    # Python dependencies
├── static/             # Static files
│   └── assets/         # Uploaded assets and images
└── templates/          # HTML templates
```
