import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from tenants.models import Clinic

schemas = list(Clinic.objects.values_list('schema_name', flat=True))

for schema in schemas:
    with connection.cursor() as cursor:
        cursor.execute(f"SET search_path TO {schema}")
        cursor.execute("DELETE FROM django_migrations")
        print(f"Deleted all migrations from schema {schema}!")