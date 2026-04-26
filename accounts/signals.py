from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from audit.utils import log_action


@receiver(user_logged_in)
def log_user_login(sender, user, request, **kwargs):
    log_action(user, 'User login', f'{user.username} logged in.')
