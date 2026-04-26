from django.db import models
from patients.models import Patient
from pharmacy.models import Prescription

class Invoice(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ]
    INVOICE_TYPE_CHOICES = [
        ('dental', 'Dental'),
        ('pharmacy', 'Pharmacy'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='invoices')
    prescription = models.ForeignKey(Prescription, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    treatment = models.ForeignKey('edr.Treatment', on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    invoice_type = models.CharField(max_length=20, choices=INVOICE_TYPE_CHOICES, default='dental')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.invoice_type.title()} Invoice for {self.patient.full_name} - {self.total_amount}"


class DentalInvoiceManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(invoice_type='dental')


class PharmacyInvoiceManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(invoice_type='pharmacy')


class DentalInvoice(Invoice):
    objects = DentalInvoiceManager()

    class Meta:
        proxy = True
        verbose_name = 'Dental Invoice'
        verbose_name_plural = 'Dental Invoices'


class PharmacyInvoice(Invoice):
    objects = PharmacyInvoiceManager()

    class Meta:
        proxy = True
        verbose_name = 'Pharmacy Invoice'
        verbose_name_plural = 'Pharmacy Invoices'
