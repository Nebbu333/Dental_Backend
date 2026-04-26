from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Appointment
from .serializers import AppointmentSerializer
from accounts.permissions import RolePermission
from audit.utils import log_action

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
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
        appointment = serializer.save()
        log_action(self.request.user, 'Appointment created', f'Appointment {appointment.id} created for {appointment.patient.full_name}.')
