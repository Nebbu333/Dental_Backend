import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

schemas = ['addis_smile_dental']

for schema in schemas:
    with connection.cursor() as cursor:
        cursor.execute(f"SET search_path TO {schema}")
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = %s", [schema])
        tables = cursor.fetchall()
        print(f"Tables in schema {schema}:")
        for table in tables:
            print(f"  {table[0]}")
        print()