3. App Folder (Application Logic)
    A Django project can have multiple apps, each handling a specific feature.
    Important Files Inside an App:

Models.py
    Defines database structure
    Each class one database table
    Uses Django ORM (no SQI required)

Views.py
    Contains business logic
    Processes user requests.
    Decides what data to send to templates

Urls.py (inside app):
    Maps app-specific URLs to views
    Keeps routing clean and modular