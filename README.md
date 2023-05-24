# Finor - Django Web App

### How to run Finor:
Make sure you got Python and Django correctly installed in your machine, additionally follow the next steps:

Finor requires the following modules:
- python -m pip install django-browser-reload
- python -m pip install requests
- python -m pip install python-dateutil
- python -m pip install Pillow
- python -m pip install matplotlib

Run the Migrate Command:
- python manage.py migrate

Run the Server:
- python manage.py runserver

Or in case you want to make it available in your Local LAN, use the following command instead:
- python manage.py runserver 0.0.0.0:8000