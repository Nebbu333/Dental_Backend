from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer
from accounts.permissions import RolePermission
from audit.utils import log_action

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, RolePermission]
    role_permissions = {
        'list': ['admin', 'dentist', 'receptionist', 'pharmacist'],
        'retrieve': ['admin', 'dentist', 'receptionist', 'pharmacist'],
        'create': ['admin', 'dentist', 'receptionist', 'pharmacist'],
        'update': ['admin'],
        'partial_update': ['admin'],
        'destroy': ['admin'],
    }

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Message.objects.all()
        return Message.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user))

    def perform_create(self, serializer):
        message = serializer.save()
        log_action(self.request.user, 'Message sent', f'Message to {message.receiver.username} sent.')
        if self.request.user.role == 'admin':
            return Message.objects.all()
        return Message.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user))

    def perform_create(self, serializer):
        message = serializer.save()
        log_action(self.request.user, 'Message sent', f'Message to {message.receiver.username} sent.')
