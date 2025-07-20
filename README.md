# devbox_backend

This project provides a backend service for the **Devbox Platform**, including user authentication and API usage tracking with Kafka integration.

## 📦 Tech Stack

- Python 3.12
- Django + Django REST Framework
- Pytest
- Swagger (drf-yasg)

# Create & activate virtual environment

python3 -m venv v_env
source v_env/bin/activate
#  Install dependencies(packages)
pip install -r requirements.txt

# Run Django server
python manage.py migrate  # No DB used, but required to set up auth
python manage.py runserver

# API Endpoints

Method	Endpoint	        Description
POST	/login/	            Login and get JWT token
GET	    /profile/	        View mock profile
GET	    /api-usage/	        List API usage
POST	/api-usage/add/	    Add API usage 
GET	    /swagger/	        Swagger UI Docs
GET	    /redoc/	            ReDoc API Docs
# Login Credentials

# Authentication
Use Authorization: Bearer <access_token> pass in the request header for /profile/ and /api-usage/* endpoints.

# Run Tests (Pytest + Django)
1.Create pytest.ini in project root:
    [pytest]
    DJANGO_SETTINGS_MODULE = devbox_platform.settings
    python_files = tests.py test_*.py *_tests.py

Run tests:
pytest 

# Future Improvements
1.persistent DB (e.g., PostgreSQL)
2.Use Kafka with Kafka Connect or Kafka Streams
3.Add Kafka consumers in Django
4.Dockerize Django app itself