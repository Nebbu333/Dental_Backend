from django.db import models
from django.conf import settings
from patients.models import Patient

class Treatment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='treatments')
    dentist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='treatments_provided')
    diagnosis = models.TextField()
    treatment_notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Treatment for {self.patient.full_name} on {self.created_at.date()}"
