from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTAuthenticationFromCookie(JWTAuthentication):
    """Reads JWT access token from cookies instead of Authorization header."""

    def authenticate(self, request):
        """Reads JWT from cookie if Authorization header is absent."""
        header = self.get_header(request)
        if header is None:
            raw_token = request.COOKIES.get("access_token")
            if raw_token is None:
                return None
        else:
            raw_token = self.get_raw_token(header)

        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)
        return (user, validated_token)
