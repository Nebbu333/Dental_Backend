from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncDate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import RolePermission
from billing.models import Invoice
from pharmacy.models import Prescription, PrescriptionItem, Medicine


class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated, RolePermission]
    role_permissions = {
        'get': ['admin', 'receptionist'],
    }

    def get(self, request):
        total_revenue = Invoice.objects.filter(payment_status='paid').aggregate(total=Sum('total_amount'))['total'] or 0
        prescriptions_per_day = (
            Prescription.objects
            .annotate(day=TruncDate('created_at'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('-day')
        )
        stock_usage = PrescriptionItem.objects.filter(availability_status='dispensed').aggregate(total_dispensed=Sum('quantity'))['total_dispensed'] or 0
        unpaid_invoices = Invoice.objects.filter(Q(payment_status='pending') | Q(payment_status='unpaid')).count()
        current_stock = Medicine.objects.aggregate(total_stock=Sum('stock_quantity'))['total_stock'] or 0

        return Response({
            'total_revenue': total_revenue,
            'unpaid_invoices': unpaid_invoices,
            'stock_usage': stock_usage,
            'current_stock': current_stock,
            'prescriptions_per_day': [
                {'day': result['day'], 'count': result['count']} for result in prescriptions_per_day
            ],
        })
