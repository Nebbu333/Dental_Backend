from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Treatment
from .serializers import TreatmentSerializer
from accounts.permissions import RolePermission
from billing.models import Invoice
from audit.utils import log_action

class TreatmentViewSet(viewsets.ModelViewSet):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer
    permission_classes = [IsAuthenticated, RolePermission]
    role_permissions = {
        'list': ['admin', 'dentist', 'receptionist'],
        'retrieve': ['admin', 'dentist', 'receptionist'],
        'create': ['admin', 'dentist'],
        'update': ['admin', 'dentist'],
        'partial_update': ['admin', 'dentist'],
        'destroy': ['admin'],
    }

    def _create_dental_invoice(self, treatment):
        if treatment.status == 'completed' and not Invoice.objects.filter(treatment=treatment, invoice_type='dental').exists():
            invoice = Invoice.objects.create(
                patient=treatment.patient,
                treatment=treatment,
                total_amount=treatment.treatment_cost,
                payment_status='pending',
                invoice_type='dental'
            )
            log_action(self.request.user, 'Dental invoice created', f'Dental invoice #{invoice.id} created for treatment #{treatment.id}.')

    def perform_create(self, serializer):
        dentist = self.request.user if self.request.user.role == 'dentist' else serializer.validated_data.get('dentist')
        treatment = serializer.save(dentist=dentist)
        log_action(self.request.user, 'Treatment created', f'Treatment #{treatment.id} created for {treatment.patient.full_name}.')
        self._create_dental_invoice(treatment)

    def perform_update(self, serializer):
        treatment = serializer.save()
        self._create_dental_invoice(treatment)
        log_action(self.request.user, 'Treatment updated', f'Treatment #{treatment.id} updated.')
