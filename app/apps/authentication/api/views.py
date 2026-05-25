from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView, Response, status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User

from .serializers import RegisterSerializer
    

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'User created successfully!'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):

    def post(self, request):
        response = Response(
            {"detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."},
            status=status.HTTP_200_OK
        )
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


class LoginView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):

        response = super().post(request, *args, **kwargs)
        refresh = response.data.get('refresh')
        access = response.data.get('access')

        response.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=True,
            secure=True,
            samesite='Lax'
        )

        response.set_cookie(
            key="access_token",
            value=access,
            httponly=True,
            secure=True,
            samesite='Lax'
        )

        username = request.data.get('username')
        user = User.objects.get(username=username)

        response.data = {
            "detail": "Login successfully!",
            "user": {
                "id": user.pk,
                "username": user.username,
                "email": user.email
            }
        }
        return response


class TokenRefreshView(TokenRefreshView):

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

        response = Response(
            {"detail": "Token refreshed"}
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite='Lax'
        )

        return response
