from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Clinic(TenantMixin):
    name = models.CharField(max_length=255)
    billing_email = models.EmailField()
    subscription_tier = models.CharField(max_length=50)

    auto_create_schema = True

    def __str__(self):
        return self.name


class Domain(DomainMixin):
    pass