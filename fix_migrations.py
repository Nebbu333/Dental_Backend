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
        try:
            cursor.execute(
                "INSERT INTO django_migrations (app, name, applied) "
                "VALUES ('accounts', '0001_initial', CURRENT_TIMESTAMP)"
            )
            print(f"Fixed migration history for schema {schema}!")
        except Exception as e:
            print(f"Schema {schema} already fixed or error: {e}")

