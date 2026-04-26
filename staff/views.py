from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import StaffProfile
from .serializers import StaffProfileSerializer
from accounts.permissions import RolePermission


class StaffProfileViewSet(viewsets.ModelViewSet):
    queryset = StaffProfile.objects.all()
    serializer_class = StaffProfileSerializer
    permission_classes = [IsAuthenticated, RolePermission]
    role_permissions = {
        'list': ['admin'],
        'retrieve': ['admin'],
        'create': ['admin'],
        'update': ['admin'],
        'partial_update': ['admin'],
        'destroy': ['admin'],
    }
