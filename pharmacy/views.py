from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Medicine, Prescription, PrescriptionItem
from .serializers import MedicineSerializer, PrescriptionSerializer, PrescriptionItemSerializer
from billing.models import Invoice

class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

    @action(detail=True, methods=['post'])
    def dispense(self, request, pk=None):
        prescription = self.get_object()
        
        # Check if there's an invoice and if it's paid
        invoice = Invoice.objects.filter(prescription=prescription).first()
        
        if invoice and invoice.payment_status != 'paid':
            return Response(
                {"detail": "NOT PAID - DO NOT DISPENSE"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        items = prescription.items.filter(availability_status='available')
        
        # Process dispensing and reduce stock
        dispensed_count = 0
        for item in items:
            medicine = item.medicine
            if medicine.stock_quantity >= item.quantity:
                medicine.stock_quantity -= item.quantity
                medicine.save()
                item.availability_status = 'dispensed'
                item.save()
                dispensed_count += 1
                
        return Response({
            "detail": f"Successfully dispensed {dispensed_count} items.",
        })
