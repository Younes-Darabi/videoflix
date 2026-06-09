from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator

from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer
from .services import account_activation_token, send_activation_email, send_password_reset_email
from ..models import CustomUser


class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = serializer.save()
                send_activation_email(user, request)
            except Exception as e:
                return Response({"detail": "Registration failed. Please try again."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({
                "user": {
                    "id": user.pk,
                    "email": user.email
                },
                "token": account_activation_token.make_token(user)
            },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateAccountView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, CustomUser.DoesNotExist):
            return Response({"detail": "Activation link is invalid."}, status=status.HTTP_400_BAD_REQUEST)

        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Account successfully activated."}, status=status.HTTP_200_OK)

        return Response({"detail": "Activation link is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email')

        try:
            user = CustomUser.objects.get(email=email)
            send_password_reset_email(user, request)
        except CustomUser.DoesNotExist:
            pass

        return Response(
            {"detail": "An email has been sent to reset your password."},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, CustomUser.DoesNotExist):
            return Response({"detail": "Invalid link."}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Invalid or expired link."}, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if new_password != confirm_password:
            return Response({"detail": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Your Password has been successfully reset."}, status=status.HTTP_200_OK)


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = serializer.validated_data["refresh"]
        access = serializer.validated_data["access"]

        response = Response({"detail": "Login successful"})

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite='Lax'
        )

        response.set_cookie(
            key="access_token",
            value=str(access),
            httponly=True,
            secure=True,
            samesite='Lax'
        )

        email = request.data.get('email')
        user = CustomUser.objects.get(email=email)

        response.data = {
            "detail": "Login successful",
            "user": {
                "id": user.pk,
                "username": user.email
            }
        }
        return response


class LogoutView(APIView):

    def post(self, request):
        response = Response(
            {"detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."},
            status=status.HTTP_200_OK
        )
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


class CustomTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token is None:
            return Response(
                {'Detail': 'Refresh token not found!'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.get_serializer(data={'refresh': refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response(
                {'Detail': 'Refresh token invalid!'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        access_token = serializer.validated_data.get('access')

        response = Response({
            "detail": "access Token refreshed",
            "access": access_token
            })

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite='Lax'
        )

        return response
