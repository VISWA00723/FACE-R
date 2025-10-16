# Production Deployment Guide

This guide covers deploying the Face Recognition Attendance System to production.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Backend Deployment](#backend-deployment)
3. [Frontend Deployment](#frontend-deployment)
4. [Database Configuration](#database-configuration)
5. [Security Hardening](#security-hardening)
6. [Performance Optimization](#performance-optimization)
7. [Monitoring & Logging](#monitoring--logging)
8. [Backup & Recovery](#backup--recovery)

## Prerequisites

- Linux server (Ubuntu 20.04 LTS or higher recommended)
- Domain name with SSL certificate
- PostgreSQL database (managed or self-hosted)
- Minimum 4GB RAM, 2 CPU cores
- 50GB storage (for models and data)

## Backend Deployment

### Option 1: Deploy with Nginx + Gunicorn

#### 1. Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and PostgreSQL client
sudo apt install -y python3.12 python3-pip python3-venv postgresql-client nginx

# Install system dependencies for OpenCV
sudo apt install -y libgl1-mesa-glx libglib2.0-0
```

#### 2. Clone and Setup

```bash
# Create application directory
sudo mkdir -p /var/www/face-recognition
sudo chown $USER:$USER /var/www/face-recognition
cd /var/www/face-recognition

# Clone repository
git clone <your-repo-url> .

# Create virtual environment
cd backend
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Gunicorn
pip install gunicorn
```

#### 3. Configure Environment

```bash
# Create production .env
nano /var/www/face-recognition/.env
```

Add:

```env
# Database (use managed database URL)
DATABASE_URL=postgresql://user:password@db-host:5432/face_recognition_db

# Security
SECRET_KEY=<generate-strong-random-key>
ALGORITHM=HS256

# API
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=false

# Face Recognition
FACE_RECOGNITION_THRESHOLD=0.6
USE_FAISS=true

# CORS (your frontend domain)
CORS_ORIGINS=https://yourdomain.com

# Logging
LOG_LEVEL=WARNING
LOG_FILE=/var/log/face-recognition/app.log
```

#### 4. Create Systemd Service

```bash
sudo nano /etc/systemd/system/face-recognition.service
```

Add:

```ini
[Unit]
Description=Face Recognition Attendance System API
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/face-recognition/backend
Environment="PATH=/var/www/face-recognition/backend/venv/bin"
ExecStart=/var/www/face-recognition/backend/venv/bin/gunicorn \
    -k uvicorn.workers.UvicornWorker \
    -w 4 \
    -b 0.0.0.0:8000 \
    --timeout 120 \
    --access-logfile /var/log/face-recognition/access.log \
    --error-logfile /var/log/face-recognition/error.log \
    app.api.app:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 5. Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/face-recognition
```

Add:

```nginx
upstream face_recognition_api {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    # SSL Configuration (use Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Logging
    access_log /var/log/nginx/face-recognition-access.log;
    error_log /var/log/nginx/face-recognition-error.log;

    # Max body size (for image uploads)
    client_max_body_size 50M;

    location / {
        proxy_pass http://face_recognition_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts for face processing
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
    }
}
```

Enable and start:

```bash
# Create log directory
sudo mkdir -p /var/log/face-recognition
sudo chown www-data:www-data /var/log/face-recognition

# Enable site
sudo ln -s /etc/nginx/sites-available/face-recognition /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Enable and start service
sudo systemctl enable face-recognition
sudo systemctl start face-recognition
sudo systemctl status face-recognition
```

### Option 2: Docker Deployment

#### Create Dockerfile

```dockerfile
# Backend Dockerfile
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/ .

# Create necessary directories
RUN mkdir -p /app/data /app/logs /app/uploads

EXPOSE 8000

CMD ["uvicorn", "app.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: always

  backend:
    build: .
    environment:
      - DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@postgres:5432/${DB_NAME}
    env_file:
      - .env
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./uploads:/app/uploads
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    restart: always

volumes:
  postgres_data:
```

Deploy:

```bash
docker-compose up -d
```

## Frontend Deployment

### Build Production Bundle

```bash
cd frontend

# Install dependencies
npm install

# Build for production
npm run build
```

### Deploy with Nginx

```bash
sudo nano /etc/nginx/sites-available/face-recognition-frontend
```

Add:

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    root /var/www/face-recognition/frontend/dist;
    index index.html;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml+rss text/javascript;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

Enable:

```bash
sudo ln -s /etc/nginx/sites-available/face-recognition-frontend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Database Configuration

### PostgreSQL Production Setup

```bash
# Connect to PostgreSQL
sudo -u postgres psql

-- Create production user
CREATE USER face_recognition_user WITH PASSWORD 'strong-password';

-- Create database
CREATE DATABASE face_recognition_db OWNER face_recognition_user;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE face_recognition_db TO face_recognition_user;

\q
```

### Run Migrations

```bash
cd /var/www/face-recognition/database
python init_db.py
```

### Configure Backups

```bash
# Create backup script
sudo nano /usr/local/bin/backup-face-recognition.sh
```

Add:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/face-recognition"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="face_recognition_db"

mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U face_recognition_user $DB_NAME | gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Backup uploads and data
tar -czf $BACKUP_DIR/files_backup_$DATE.tar.gz /var/www/face-recognition/uploads /var/www/face-recognition/data

# Keep only last 7 days
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

Make executable and schedule:

```bash
sudo chmod +x /usr/local/bin/backup-face-recognition.sh

# Add to crontab (daily at 2 AM)
sudo crontab -e
# Add: 0 2 * * * /usr/local/bin/backup-face-recognition.sh
```

## Security Hardening

### 1. Firewall Configuration

```bash
# Allow SSH, HTTP, HTTPS
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 2. Fail2Ban

```bash
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 3. SSL Certificate (Let's Encrypt)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d api.yourdomain.com
```

### 4. Environment Variables

Never commit `.env` files. Use secrets management in production.

## Performance Optimization

### 1. Enable FAISS

Ensure `USE_FAISS=true` in `.env` for faster face matching.

### 2. Database Indexing

Already configured in `init_db.py`:
- Index on `employee_id`
- Index on `log_date`
- Composite index on `employee_id` and `log_date`

### 3. Caching

Consider adding Redis for caching:

```bash
sudo apt install -y redis-server
```

### 4. CDN for Static Assets

Use CDN (CloudFlare, AWS CloudFront) for frontend static files.

## Monitoring & Logging

### Application Logs

```bash
# View logs
sudo tail -f /var/log/face-recognition/app.log
sudo tail -f /var/log/face-recognition/access.log
sudo tail -f /var/log/face-recognition/error.log
```

### System Monitoring

Install monitoring tools:

```bash
# htop for system monitoring
sudo apt install -y htop

# Monitor service
sudo systemctl status face-recognition
```

### Log Rotation

```bash
sudo nano /etc/logrotate.d/face-recognition
```

Add:

```
/var/log/face-recognition/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload face-recognition > /dev/null 2>&1 || true
    endscript
}
```

## Health Checks

Create health check endpoint monitoring:

```bash
# Simple health check script
nano /usr/local/bin/health-check.sh
```

```bash
#!/bin/bash
HEALTH_URL="https://api.yourdomain.com/health"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL)

if [ $RESPONSE -ne 200 ]; then
    echo "Health check failed: HTTP $RESPONSE"
    # Send alert (email, Slack, etc.)
    systemctl restart face-recognition
fi
```

Schedule:

```bash
sudo chmod +x /usr/local/bin/health-check.sh
# Add to crontab: every 5 minutes
*/5 * * * * /usr/local/bin/health-check.sh
```

## Troubleshooting Production Issues

### Backend Not Starting

```bash
# Check logs
sudo journalctl -u face-recognition -n 50 -f

# Check service status
sudo systemctl status face-recognition

# Restart service
sudo systemctl restart face-recognition
```

### Database Connection Issues

```bash
# Test database connection
psql -h localhost -U face_recognition_user -d face_recognition_db

# Check PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-14-main.log
```

### High Memory Usage

Face recognition models use significant memory. Consider:
- Increasing server RAM
- Reducing number of Gunicorn workers
- Enabling swap space

## Maintenance

### Update Application

```bash
cd /var/www/face-recognition
git pull origin main

# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart face-recognition

# Frontend
cd ../frontend
npm install
npm run build
```

### Database Maintenance

```bash
# Vacuum database (reclaim storage)
psql -U face_recognition_user -d face_recognition_db -c "VACUUM ANALYZE;"

# Check database size
psql -U face_recognition_user -d face_recognition_db -c "SELECT pg_size_pretty(pg_database_size('face_recognition_db'));"
```

## Production Checklist

- [ ] Strong `SECRET_KEY` configured
- [ ] HTTPS enabled with valid SSL certificate
- [ ] Firewall configured
- [ ] Database backups scheduled
- [ ] Log rotation configured
- [ ] Monitoring and alerts set up
- [ ] Health checks implemented
- [ ] CORS properly configured
- [ ] File upload limits set
- [ ] Error tracking enabled
- [ ] Documentation updated with production URLs

## Support

For production issues:
- Check application logs
- Review Nginx error logs
- Monitor system resources
- Check database connections
- Verify SSL certificates

Keep your system updated and monitor security advisories for all dependencies.
