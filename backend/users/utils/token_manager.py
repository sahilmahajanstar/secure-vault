from datetime import datetime
from functools import wraps

import jwt
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from common.error.authentication_error import (
    AuthenticationError,
    AuthenticationErrorCodes,
)
from vault import settings
from rest_framework import status
from django.utils import timezone


class TokenManager:
    def __init__(self, request):
        self.request = request

    def get_token(self):
        if self.request.headers.get("Authorization"):
            return self.request.headers.get("Authorization").split(" ")[1]
        return None

    def sign_token(self, user):
        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)
        payload = self.verify_token(access_token)
        OutstandingToken.objects.create(
            token=access_token,
            user_id=payload.get("user_id"),
            expires_at=timezone.datetime.fromtimestamp(payload.get("exp")),
            created_at=timezone.now(),
            jti=payload.get("jti"),
        )
        return {"refresh": refresh_token, "access": access_token}

    def refresh_token(self, token):
        try:
            refresh = RefreshToken(token)
            return {"refresh": str(refresh), "access": str(refresh.access_token)}
        except Exception as e:
            raise AuthenticationError(
                "Invalid or expired refresh token",
                AuthenticationErrorCodes.TOKEN_EXPIRED,
                status.HTTP_401_UNAUTHORIZED,
            )

    def verify_token(self, token):
        try:
            payload = AccessToken(token).payload
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationError(
                "Token has expired",
                AuthenticationErrorCodes.TOKEN_EXPIRED,
                status.HTTP_401_UNAUTHORIZED,
            )

    def add_to_blacklisted_token(self, token: OutstandingToken):
        BlacklistedToken.objects.create(token=token)

    def revoke_token(self):
        try:
            token = self.validate_token()
            jti = token.get("jti")
            outstanding_token = OutstandingToken.objects.get(jti=jti)
            self.add_to_blacklisted_token(outstanding_token)
            return True
        except Exception as e:
            return False

    def validate_token(self):
        return AccessToken(self.get_token())

    def is_token_blacklisted(self):
        try:
            token = self.validate_token()
            jti = token.get("jti")
            return BlacklistedToken.objects.filter(token__jti=jti).exists()
        except Exception:
            return True

    def is_token_valid(self):
        return not self.is_token_blacklisted()

    def revoke_all_tokens(self, user):
        tokens = OutstandingToken.objects.select_related("blacklistedtoken").filter(
            blacklistedtoken__isnull=True
        )
        for token in tokens:
            try:
                self.add_to_blacklisted_token(token)
            except Exception as e:
                print(e, flush=True)
