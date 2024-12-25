# Expense Tracker API

This is a Django REST Framework (DRF) application for managing expenses and categories. It provides endpoints for creating, retrieving, updating, and deleting expenses, as well as managing categories.

## Features
**Expense Management**:
- Create, retrieve, update, and delete expenses.
- Filter expenses by category or date.

**Category Management**:
- Automatically create categories if they don't exist when adding or updating expenses.

**Authentication**:
- Uses JWT (JSON Web Tokens) for secure authentication.

## Installation

*Prerequisites:*
- Python 3.6 or higher
- PostgreSQL

1. Clone the Repository

```
git clone https://github.com/Anguilla-anguilla/expense_tracker_API.git
cd expense_tracker_API
```

2. Set Up a Virtual Environment

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Dependencies

```
pip install -r requirements.txt
```

4. Set Up the Database
Create a PostgreSQL database for the project. Update the database settings in settings.py:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
Apply migrations:

```
python manage.py migrate
```

5. Create a superuser:
```
python manage.py createsuperuser
```

6. Run the Development Server

```
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/schema/swagger`.

[Project URL](https://roadmap.sh/projects/expense-tracker-api)
