from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.conf import settings


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active)


account_activation_token = AccountActivationTokenGenerator()


def send_activation_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    frontend_url = settings.FRONTEND_URL
    link = f"{frontend_url}/pages/auth/activate.html?uid={uid}&token={token}"

    html_content = render_to_string('authentication/emails/activation_email.html', {
        'user': user,
        'link': link,
    })

    email = EmailMultiAlternatives(
        subject="Activate your account",
        body=f"Click the link to activate your account:\n{link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)


def send_password_reset_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    frontend_url = settings.FRONTEND_URL
    link = f"{frontend_url}/pages/auth/confirm_password.html?uid={uid}&token={token}"

    html_content = render_to_string('authentication/emails/password_reset_email.html', {
        'user': user,
        'link': link,
    })

    email = EmailMultiAlternatives(
        subject="Reset your password",
        body=f"Click the link to reset your password:\n{link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
