# Database Connection and Data Management Guide

## ✅ Database Connection Verified!

Your PostgreSQL database is **connected and working** perfectly! Here's the proof:

### Database Info
- **Status**: ✅ Connected
- **Database**: flaskdb
- **User**: flaskuser
- **Tables**: 2 tables created
  - `users` (your data table)
  - `alembic_version` (migrations tracker)

### Users Table Schema
```sql
Column      | Type                        | Nullable | Default
------------|----------------------------|----------|------------------
id          | integer                     | NO       | Auto-increment (Primary Key)
username    | character varying(80)       | NO       | -
email       | character varying(120)      | NO       | -
password    | character varying(255)      | NO       | -
created_at  | timestamp without time zone | YES      | Current timestamp
updated_at  | timestamp without time zone | YES      | Current timestamp
```

**Current Records**: 0 (database is empty)

---

## 🔍 How to Check Database Connection

### Method 1: Check with Docker Command
```bash
# List all tables
docker-compose exec db psql -U flaskuser -d flaskdb -c "\dt"

# Check users table structure
docker-compose exec db psql -U flaskuser -d flaskdb -c "\d users"

# Count records
docker-compose exec db psql -U flaskuser -d flaskdb -c "SELECT COUNT(*) FROM users;"
```

### Method 2: Interactive Database Shell
```bash
# Enter PostgreSQL shell
./docker.sh db-shell
# or
docker-compose exec db psql -U flaskuser -d flaskdb

# Inside psql, try these commands:
\dt                    # List all tables
\d users              # Describe users table
SELECT * FROM users;  # View all users
\q                    # Exit
```

### Method 3: Use Flask Shell
```bash
# Open Flask shell
docker-compose exec web flask shell

# Inside Flask shell:
>>> from app.utils.database import db
>>> from app.models.user import User
>>> db.session.execute('SELECT 1').scalar()
1  # ✅ This means database is connected!
>>> User.query.count()
0  # Number of users in database
>>> exit()
```

### Method 4: Health Check Endpoint
```bash
# Your app has a health check endpoint
curl http://localhost:5000/health

# Should return:
# {"status":"healthy"}
```

---

## 📝 How to Add Data to Database

### Method 1: Using Flask Shell (Recommended for Testing)

**Step-by-step:**

1. **Open Flask shell**:
```bash
docker-compose exec web flask shell
```

2. **Import the model**:
```python
from app.models.user import User
from app.utils.database import db
from werkzeug.security import generate_password_hash
```

3. **Create a new user**:
```python
# Create user object
user = User(
    username='john_doe',
    email='john@example.com',
    password=generate_password_hash('secretpassword123')
)

# Add to session
db.session.add(user)

# Commit to database
db.session.commit()

print(f"User created with ID: {user.id}")
```

4. **Verify it was added**:
```python
# Query all users
users = User.query.all()
for u in users:
    print(u.to_dict())

# Query specific user
user = User.query.filter_by(username='john_doe').first()
print(user.to_dict())
```

5. **Exit**:
```python
exit()
```

### Method 2: Using API Endpoints

First, let me check your API routes:

```bash
# Check if you have a create user endpoint
curl -X GET http://localhost:5000/api/users/
```

**If you have a POST endpoint for creating users:**
```bash
curl -X POST http://localhost:5000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jane_doe",
    "email": "jane@example.com",
    "password": "securepass456"
  }'
```

### Method 3: Direct SQL (Not Recommended)

```bash
# Enter database shell
docker-compose exec db psql -U flaskuser -d flaskdb

# Insert data directly (DON'T DO THIS FOR PASSWORDS - use hashed passwords!)
INSERT INTO users (username, email, password, created_at, updated_at)
VALUES ('testuser', 'test@example.com', 'hashed_password_here', NOW(), NOW());

# Verify
SELECT * FROM users;

# Exit
\q
```

---

## 🚀 Complete Example: Adding Sample Data

### Create Sample Users Script

Let me create a Python script to add sample data:

```python
# Run this in Flask shell
from app.models.user import User
from app.utils.database import db
from werkzeug.security import generate_password_hash

# Create multiple users
sample_users = [
    {
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'password123'
    },
    {
        'username': 'bob',
        'email': 'bob@example.com',
        'password': 'password456'
    },
    {
        'username': 'charlie',
        'email': 'charlie@example.com',
        'password': 'password789'
    }
]

# Add all users
for user_data in sample_users:
    user = User(
        username=user_data['username'],
        email=user_data['email'],
        password=generate_password_hash(user_data['password'])
    )
    db.session.add(user)

# Save all at once
db.session.commit()

print(f"Added {User.query.count()} users!")

# Display all users
for user in User.query.all():
    print(user.to_dict())
```

---

## 📋 Common Database Operations

### Create (Add New Record)
```python
user = User(username='newuser', email='new@example.com', password='hashed_pwd')
db.session.add(user)
db.session.commit()
```

### Read (Query Records)
```python
# Get all users
all_users = User.query.all()

# Get specific user by ID
user = User.query.get(1)

# Filter by field
user = User.query.filter_by(username='alice').first()

# Get count
count = User.query.count()
```

### Update (Modify Record)
```python
# Find user
user = User.query.filter_by(username='alice').first()

# Update fields
user.email = 'newemail@example.com'

# Save changes
db.session.commit()
```

### Delete (Remove Record)
```python
# Find user
user = User.query.filter_by(username='bob').first()

# Delete
db.session.delete(user)
db.session.commit()
```

---

## 🛠️ Quick Commands Reference

### Check Database Status
```bash
# View all tables
docker-compose exec db psql -U flaskuser -d flaskdb -c "\dt"

# View users count
docker-compose exec db psql -U flaskuser -d flaskdb -c "SELECT COUNT(*) FROM users;"

# View all users
docker-compose exec db psql -U flaskuser -d flaskdb -c "SELECT id, username, email FROM users;"
```

### Add Data via Flask Shell
```bash
# 1. Open shell
docker-compose exec web flask shell

# 2. Run commands (paste this whole block):
from app.models.user import User
from app.utils.database import db
from werkzeug.security import generate_password_hash

user = User(
    username='testuser',
    email='test@example.com',
    password=generate_password_hash('password123')
)
db.session.add(user)
db.session.commit()
print(f"Created user: {user.to_dict()}")
exit()
```

### Verify Data Was Added
```bash
docker-compose exec db psql -U flaskuser -d flaskdb -c "SELECT * FROM users;"
```

---

## 🎯 Practical Example Walkthrough

Let's add a user and verify it works:

### Step 1: Check Current State
```bash
docker-compose exec db psql -U flaskuser -d flaskdb -c "SELECT COUNT(*) FROM users;"
# Should show: count = 0
```

### Step 2: Add a User
```bash
# Open Flask shell
docker-compose exec web flask shell
```

```python
# Inside Flask shell - copy and paste this:
from app.models.user import User
from app.utils.database import db
from werkzeug.security import generate_password_hash

# Create user
new_user = User(
    username='admin',
    email='admin@example.com',
    password=generate_password_hash('admin123')
)

# Save to database
db.session.add(new_user)
db.session.commit()

# Verify
print(f"✅ User created with ID: {new_user.id}")
print(new_user.to_dict())

# Exit
exit()
```

### Step 3: Verify in Database
```bash
# Check count again
docker-compose exec db psql -U flaskuser -d flaskdb -c "SELECT COUNT(*) FROM users;"
# Should show: count = 1

# View the user
docker-compose exec db psql -U flaskuser -d flaskdb -c "SELECT id, username, email FROM users;"
```

**Expected Output:**
```
 id | username |      email       
----+----------+------------------
  1 | admin    | admin@example.com
```

✅ **Success!** Your user has been added to the database!

---

## 🔍 Troubleshooting

### Database Connection Issues

**Problem**: Can't connect to database
```bash
# Check if database container is running
docker-compose ps

# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

**Problem**: Permission denied
```bash
# Check password in docker-compose.yml
# Should be: flaskuser / flaskpass
```

### Data Not Saving

**Problem**: Data disappears after container restart
- ✅ Don't worry! We use volumes, data persists
- Check: `docker volume ls` (should see `flask-production-app_postgres_data`)

**Problem**: Forgot to commit
```python
db.session.add(user)
# ❌ Forgot this line:
db.session.commit()  # Always commit!
```

---

## 📚 Additional Resources

### Your Database Models Location
- **Models**: `/app/models/user.py`
- **Database Utils**: `/app/utils/database.py`
- **Migrations**: `/migrations/`

### Useful Commands
```bash
# Create new migration (after changing models)
docker-compose exec web flask db migrate -m "description"

# Apply migrations
docker-compose exec web flask db upgrade

# Rollback migration
docker-compose exec web flask db downgrade
```

---

## 💡 Best Practices

1. **Always hash passwords**: Use `generate_password_hash()` for storing passwords
2. **Commit your changes**: Don't forget `db.session.commit()`
3. **Handle errors**: Wrap database operations in try-except blocks
4. **Use transactions**: Batch multiple operations before committing
5. **Validate data**: Check data before inserting into database

---

## 🎓 Summary

✅ **Database is connected** and working perfectly  
✅ **Users table is created** with proper schema  
✅ **You can add data** using Flask shell or API  
✅ **Data persists** in Docker volumes  
✅ **Multiple methods** available for database operations  

**Next Steps:**
1. Try adding a user using Flask shell (Method 1)
2. Verify it was added using the query commands
3. Build your API endpoints to create users programmatically

Your database is ready to use! 🚀
