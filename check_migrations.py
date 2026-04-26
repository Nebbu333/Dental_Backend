import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from tenants.models import Clinic

schemas = ['public'] + list(Clinic.objects.values_list('schema_name', flat=True))

for schema in schemas:
    with connection.cursor() as cursor:
        cursor.execute(f"SET search_path TO {schema}")
        cursor.execute("SELECT app, name, applied FROM django_migrations ORDER BY app, name")
        rows = cursor.fetchall()
        print(f"Schema {schema}:")
        for row in rows:
            print(f"  {row[0]} {row[1]} {row[2]}")
        print()