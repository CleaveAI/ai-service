import base64
import os
from typing import Any, Dict

import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt


class JWKSClient:
    def __init__(self, jwks_url: str):
        self.jwks_url = jwks_url
        self._keys_cache = None

    def get_jwks(self) -> Dict[str, Any]:
        if self._keys_cache is None:
            response = requests.get(self.jwks_url)
            response.raise_for_status()
            self._keys_cache = response.json()
        return self._keys_cache

    def get_signing_key(self, kid: str) -> str:
        jwks = self.get_jwks()

        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                return self._construct_public_key(key)

        raise HTTPException(
            status_code=401, detail=f"Unable to find key with kid: {kid}"
        )

    def _construct_public_key(self, key_data: Dict[str, Any]) -> str:
        if key_data.get("kty") != "RSA":
            raise HTTPException(status_code=401, detail="Only RSA keys are supported")

        n = self._base64url_decode(key_data["n"])
        e = self._base64url_decode(key_data["e"])

        n_int = int.from_bytes(n, byteorder="big")
        e_int = int.from_bytes(e, byteorder="big")

        public_key = rsa.RSAPublicNumbers(e_int, n_int).public_key(default_backend())

        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        return pem.decode("utf-8")

    def _base64url_decode(self, data: str) -> bytes:
        missing_padding = len(data) % 4
        if missing_padding:
            data += "=" * (4 - missing_padding)

        return base64.urlsafe_b64decode(data)


class AuthDependencies:
    def __init__(self):
        self.JWKS_URL = os.environ.get("WORKOS_JWKS_URL")
        if not self.JWKS_URL:
            raise Exception("WORKOS_JWKS_URL not set in environment variables")

        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        self.jwks_client = JWKSClient(self.JWKS_URL)

    def get_public_key(self, token):
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")
        if not kid:
            raise HTTPException(status_code=401, detail="No 'kid' in token header")
        return self.jwks_client.get_signing_key(kid)

    def verify_token(self, token: str):
        try:
            public_key = self.get_public_key(token)
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                audience=None,
                options={"verify_aud": False},
            )
            if not payload:
                raise HTTPException(status_code=401, detail="Invalid token payload")
            return {
                "user_id": payload.get("sub"),
            }
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token validation error: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )


auth_dependencies = AuthDependencies()


def get_current_user(token: str = Depends(auth_dependencies.oauth2_scheme)):
    return auth_dependencies.verify_token(token)
