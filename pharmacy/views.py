from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Medicine, Prescription, PrescriptionItem
from .serializers import MedicineSerializer, PrescriptionSerializer
from billing.models import Invoice
from accounts.permissions import RolePermission
from audit.utils import log_action

class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsAuthenticated, RolePermission]
    role_permissions = {
        'list': ['admin', 'dentist', 'receptionist', 'pharmacist'],
        'retrieve': ['admin', 'dentist', 'receptionist', 'pharmacist'],
        'create': ['admin', 'pharmacist'],
        'update': ['admin', 'pharmacist'],
        'partial_update': ['admin', 'pharmacist'],
        'destroy': ['admin'],
    }

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, RolePermission]
    role_permissions = {
        'list': ['admin', 'dentist', 'receptionist', 'pharmacist'],
        'retrieve': ['admin', 'dentist', 'receptionist', 'pharmacist'],
        'create': ['admin', 'dentist'],
        'update': ['admin', 'dentist'],
        'partial_update': ['admin', 'dentist'],
        'destroy': ['admin'],
        'dispense': ['admin', 'pharmacist'],
    }

    def perform_create(self, serializer):
        prescription = serializer.save(dentist=self.request.user if self.request.user.role == 'dentist' else serializer.validated_data.get('dentist'))
        log_action(self.request.user, 'Prescription created', f'Prescription #{prescription.id} created for {prescription.patient.full_name}.')

    @action(detail=True, methods=['post'])
    def dispense(self, request, pk=None):
        prescription = self.get_object()
        invoice = Invoice.objects.filter(prescription=prescription).first()

        if not invoice:
            return Response(
                {"detail": "NO INVOICE - CANNOT DISPENSE"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if invoice.payment_status != 'paid':
            return Response(
                {"detail": "NOT PAID - DO NOT DISPENSE"},
                status=status.HTTP_400_BAD_REQUEST
            )

        items = prescription.items.filter(availability_status='available')
        dispensed_count = 0
        for item in items:
            medicine = item.medicine
            if medicine.stock_quantity >= item.quantity:
                medicine.stock_quantity -= item.quantity
                medicine.save()
                item.availability_status = 'dispensed'
                item.save()
                dispensed_count += 1

        log_action(request.user, 'Medicine dispensed', f'Dispensed {dispensed_count} items for prescription #{prescription.id}.')
        return Response({
            "detail": f"Successfully dispensed {dispensed_count} items.",
        })
