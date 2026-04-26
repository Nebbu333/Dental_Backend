from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Patient
from .serializers import PatientSerializer
from accounts.permissions import RolePermission
from audit.utils import log_action

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, RolePermission]
    role_permissions = {
        'list': ['admin', 'dentist', 'receptionist'],
        'retrieve': ['admin', 'dentist', 'receptionist'],
        'create': ['admin', 'receptionist'],
        'update': ['admin', 'receptionist'],
        'partial_update': ['admin', 'receptionist'],
        'destroy': ['admin'],
    }

    def perform_create(self, serializer):
        patient = serializer.save(created_by=self.request.user)
        log_action(self.request.user, 'Patient created', f'Patient {patient.full_name} created.')
