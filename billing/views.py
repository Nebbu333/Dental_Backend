from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Invoice
from .serializers import InvoiceSerializer
from accounts.permissions import RolePermission
from audit.utils import log_action

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated, RolePermission]
    role_permissions = {
        'list': ['admin', 'receptionist'],
        'retrieve': ['admin', 'receptionist'],
        'create': ['admin', 'receptionist'],
        'update': ['admin', 'receptionist'],
        'partial_update': ['admin', 'receptionist'],
        'destroy': ['admin'],
        'pay': ['admin', 'receptionist'],
    }

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        invoice = self.get_object()
        if invoice.payment_status == 'paid':
            return Response({'detail': 'Invoice is already paid.'}, status=status.HTTP_200_OK)
        invoice.payment_status = 'paid'
        invoice.save()
        log_action(request.user, 'Payment made', f'Invoice #{invoice.id} marked paid.')
        return Response({'detail': 'Invoice marked paid.'}, status=status.HTTP_200_OK)
