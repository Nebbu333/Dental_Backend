from .models import AuditLog


def log_action(user, action, details=None):
    AuditLog.objects.create(user=user, action=action, details=details)
