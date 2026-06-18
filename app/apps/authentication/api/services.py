import os
from django.contrib.auth.tokens import (
    PasswordResetTokenGenerator,
    default_token_generator,
)
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.conf import settings
from email.mime.image import MIMEImage


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """Generates tokens for email account activation."""

    def _make_hash_value(self, user, timestamp):
        """Builds hash from user pk, timestamp, and is_active to invalidate token after activation."""
        return str(user.pk) + str(timestamp) + str(user.is_active)


account_activation_token = AccountActivationTokenGenerator()

LOGO_PATH = os.path.join(os.path.dirname(
    __file__), "../templates/authentication/emails/logo.png")


def _attach_logo(email):
    """Attaches the Videoflix logo as an inline image with Content-ID 'logo'."""
    with open(LOGO_PATH, "rb") as f:
        img = MIMEImage(f.read())
        img.add_header("Content-ID", "<logo>")
        img.add_header("Content-Disposition", "inline", filename="logo.png")
        email.attach(img)


def send_activation_email(user, request):
    """Sends an account activation email with a unique token link."""
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    frontend_url = settings.FRONTEND_URL
    link = f"{frontend_url}/pages/auth/activate.html?uid={uid}&token={token}"

    html_content = render_to_string(
        "authentication/emails/activation_email.html",
        {
            "user": user,
            "link": link,
        },
    )

    email = EmailMultiAlternatives(
        subject="Activate your account",
        body=f"Click the link to activate your account:\n{link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.attach_alternative(html_content, "text/html")
    _attach_logo(email)
    email.send(fail_silently=False)


def send_password_reset_email(user, request):
    """Sends a password reset email with a unique token link."""
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    frontend_url = settings.FRONTEND_URL
    link = f"{frontend_url}/pages/auth/confirm_password.html?uid={uid}&token={token}"

    html_content = render_to_string(
        "authentication/emails/password_reset_email.html",
        {
            "user": user,
            "link": link,
        },
    )

    email = EmailMultiAlternatives(
        subject="Reset your password",
        body=f"Click the link to reset your password:\n{link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.attach_alternative(html_content, "text/html")
    _attach_logo(email)
    email.send(fail_silently=False)
