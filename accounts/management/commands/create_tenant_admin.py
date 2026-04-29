from django.core.management.base import BaseCommand
from django_tenants.utils import schema_context
from tenants.models import Clinic
from accounts.models import User


class Command(BaseCommand):
    help = 'Create a tenant admin user for a specific tenant schema'

    def add_arguments(self, parser):
        parser.add_argument('schema_name', type=str, help='Tenant schema name')
        parser.add_argument('--username', type=str, default='admin', help='Admin username')
        parser.add_argument('--email', type=str, help='Admin email')
        parser.add_argument('--password', type=str, default='admin123', help='Admin password')

    def handle(self, *args, **options):
        schema_name = options['schema_name']
        username = options['username']
        email = options.get('email') or f'{username}@{schema_name}.com'
        password = options['password']

        try:
            tenant = Clinic.objects.get(schema_name=schema_name)
            self.stdout.write(f'Found tenant: {tenant.name}')
            
            with schema_context(tenant.schema_name):
                # Check if admin user already exists
                if User.objects.filter(username=username).exists():
                    user = User.objects.get(username=username)
                    self.stdout.write(
                        self.style.WARNING(f'Admin user {username} already exists in tenant {schema_name}')
                    )
                    # Ensure user has admin privileges
                    user.is_staff = True
                    user.is_superuser = True
                    user.role = 'admin'
                    user.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'Updated admin privileges for {username}')
                    )
                else:
                    # Create new admin user
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        is_staff=True,
                        is_superuser=True,
                        role='admin'
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f'Created admin user {username} in tenant {schema_name}')
                    )
                
                # Display user info
                self.stdout.write(f'User details:')
                self.stdout.write(f'  Username: {user.username}')
                self.stdout.write(f'  Email: {user.email}')
                self.stdout.write(f'  Role: {user.role}')
                self.stdout.write(f'  Is Staff: {user.is_staff}')
                self.stdout.write(f'  Is Superuser: {user.is_superuser}')
                
        except Clinic.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Tenant with schema_name {schema_name} does not exist')
            )
