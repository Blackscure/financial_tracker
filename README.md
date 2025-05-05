### Finacial tracker Backend

### Clone Project

```
  git clone https://github.com/Blackscure/financial_tracker.git

  cd financial_tracker

````


### Create Virtual Enviroment

```
   # Create virtual environment (you can name it venv or anything)
  python -m venv venv
  
  # Activate virtual environment
  # On Windows:
  venv\Scripts\activate
  # On macOS/Linux:
  source venv/bin/activate
```

### Step 3: Install Dependencies

```
    pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a .env file in the root directory (if applicable), and add your environment-specific settings:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/yourdbname
ALLOWED_HOSTS=127.0.0.1,localhost
```

### Step 5: Apply Migrations
```
    python manage.py makemigrations
    python manage.py migrate
```

### Step 7: Run the Development Server
```
  python manage.py runserver

```
