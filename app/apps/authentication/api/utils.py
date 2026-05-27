from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token

def send_activation_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    domain = request.get_host()
    link = f"http://{domain}/api/activate/{uid}/{token}/"
    
    send_mail(
        subject="Activate your account",
        message=f"Click the link to activate your account: {link}",
        from_email=None,  # settings.py DEFAULT_FROM_EMAIL
        recipient_list=[user.email],
    )