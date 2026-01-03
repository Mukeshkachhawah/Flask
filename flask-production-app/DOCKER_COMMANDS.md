# Quick Docker Commands Reference
कैसे Docker चालू करें:
bash
# Docker containers start करने के लिए
docker-compose up
# Background में चलाने के लिए
docker-compose up -d
# Logs देखने के लिए (background में चल रहा हो तो)
docker-compose logs -f



कैसे Docker बंद करें:
bash
# Containers रोकने के लिए
docker-compose down
# Containers + Database data delete करने के लिए
docker-compose down -v




## 🚀 First Time Setup

```bash
# 1. Install Docker (Ubuntu/Debian)
sudo apt update
sudo apt install docker.io docker-compose

# 2. Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# 3. Add your user to docker group (avoid using sudo)
sudo usermod -aG docker $USER
# ⚠️ Log out and log back in after this

# 4. Navigate to your project
cd /home/mukesh/Downloads/Mukks/Practise/Flask/flask-production-app

# 5. Start your application
docker-compose up --build
```

---

## 📝 Most Used Commands

### Start Your Application
```bash
# First time or after changes to Dockerfile/requirements.txt
docker-compose up --build

# Regular start (after first time)
docker-compose up

# Start in background
docker-compose up -d
```

### Stop Your Application
```bash
# Stop (keeps data)
docker-compose down

# Stop and delete all data (fresh start)
docker-compose down -v
```

### View Logs
```bash
# Show all logs
docker-compose logs

# Show logs and follow (live updates)
docker-compose logs -f

# Show only Flask app logs
docker-compose logs -f web

# Show only database logs
docker-compose logs -f db
```

### Check Status
```bash
# See if containers are running
docker-compose ps

# See all Docker containers
docker ps

# See all Docker images
docker images
```

---

## 🗄️ Database Commands

### Access Database
```bash
# Connect to PostgreSQL
docker-compose exec db psql -U flaskuser -d flaskdb

# Inside psql:
\dt                    # List all tables
\d table_name          # Show table structure
SELECT * FROM users;   # Run SQL query
\q                     # Exit psql
```

### Run Migrations
```bash
# Create new migration
docker-compose exec web flask db migrate -m "your message"

# Apply migrations
docker-compose exec web flask db upgrade

# Rollback migration
docker-compose exec web flask db downgrade
```

---

## 🔧 Other Useful Commands

### Execute Commands in Container
```bash
# Open shell in Flask container
docker-compose exec web bash

# Run Python commands
docker-compose exec web python
docker-compose exec web flask shell

# Run Flask commands
docker-compose exec web flask --help
```

### Rebuild
```bash
# Rebuild images
docker-compose build

# Rebuild from scratch (no cache)
docker-compose build --no-cache

# Rebuild and start
docker-compose up --build
```

### Clean Up
```bash
# Remove unused containers and images
docker system prune

# Remove everything (including volumes)
docker system prune -a --volumes
```

---

## 🎯 Common Workflows

### Daily Development
```bash
# Start
docker-compose up

# Work on your code...
# Changes auto-reload!

# Stop (Ctrl+C, then:)
docker-compose down
```

### Add New Python Package
```bash
# 1. Add to requirements.txt
# 2. Rebuild:
docker-compose down
docker-compose up --build
```

### Fresh Start (Reset Everything)
```bash
docker-compose down -v
docker-compose up --build
```

### Check Why Container Failed
```bash
docker-compose ps
docker-compose logs web
docker-compose logs db
```

---

## 🌐 Access Your App

- **Flask App**: http://localhost:5000
- **Database**: localhost:5432

---

## ⚠️ Troubleshooting

### Port Already in Use
```bash
# Find what's using port 5000
sudo lsof -i :5000

# Kill it
sudo kill -9 <PID>
```

### Permission Denied
```bash
# Make sure you're in docker group
sudo usermod -aG docker $USER
# Log out and log back in
```

### Container Won't Start
```bash
# Check logs
docker-compose logs

# Try fresh rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up
```

---

## 💡 Pro Tips

1. **Use background mode**: `docker-compose up -d` frees your terminal
2. **Monitor logs**: Open another terminal and run `docker-compose logs -f`
3. **Your data is safe**: Database data persists in volumes
4. **Hot reload works**: Just edit your .py files, changes apply instantly!

---

**Quick Start**: `docker-compose up --build` → Visit http://localhost:5000
