
# Django + Celery Time Conversion System

A Django app that:
- Inserts dummy customers with PST timestamps using a management command
- Converts them to UTC every 5 minutes using Celery
- Toggles between PST ↔ UTC continuously

Built as part of a learning journey to understand:
- Django management commands
- Celery scheduling
- Timezone-aware datetime handling
- Redis as message broker



