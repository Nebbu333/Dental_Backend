"""
Utilities for safe user management in multi-tenant environment
"""
from django_tenants.utils import schema_context
from tenants.models import Clinic
from accounts.models import User


def create_tenant_user(schema_name, username, email, password, role='dentist', is_staff=False, is_superuser=False):
    """
    Create a user in a specific tenant schema safely
    """
    try:
        tenant = Clinic.objects.get(schema_name=schema_name)
        with schema_context(tenant.schema_name):
            if User.objects.filter(username=username).exists():
                raise ValueError(f"User {username} already exists in tenant {schema_name}")
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role,
                is_staff=is_staff,
                is_superuser=is_superuser
            )
            return user
    except Clinic.DoesNotExist:
        raise ValueError(f"Tenant {schema_name} does not exist")


def get_tenant_users(schema_name):
    """
    Get all users in a specific tenant schema
    """
    try:
        tenant = Clinic.objects.get(schema_name=schema_name)
        with schema_context(tenant.schema_name):
            return User.objects.all()
    except Clinic.DoesNotExist:
        raise ValueError(f"Tenant {schema_name} does not exist")


def create_tenant_admin(schema_name, username='admin', email=None, password='admin123'):
    """
    Create a tenant admin user with proper privileges
    """
    if email is None:
        email = f'{username}@{schema_name}.com'
    
    return create_tenant_user(
        schema_name=schema_name,
        username=username,
        email=email,
        password=password,
        role='admin',
        is_staff=True,
        is_superuser=True
    )


def create_public_admin(username='saas_admin', email='admin@dentacore.com', password='saas123'):
    """
    Create the SaaS admin in public schema
    """
    if User.objects.filter(username=username).exists():
        return User.objects.get(username=username)
    
    return User.objects.create_user(
        username=username,
        email=email,
        password=password,
        role='admin',
        is_staff=True,
        is_superuser=True
    )


def user_exists_in_tenant(schema_name, username):
    """
    Check if a user exists in a specific tenant schema
    """
    try:
        tenant = Clinic.objects.get(schema_name=schema_name)
        with schema_context(tenant.schema_name):
            return User.objects.filter(username=username).exists()
    except Clinic.DoesNotExist:
        return False
