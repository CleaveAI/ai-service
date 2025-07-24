from workos import WorkOSClient

from src.config import settings

from .schemas import AuthenticateResponse


class AuthService:
    def __init__(self):
        self.workos_client = WorkOSClient(
            api_key=settings.WORKOS_API_KEY,
            client_id=settings.WORKOS_CLIENT_ID,
        )

    def get_jwt_token(self) -> AuthenticateResponse:
        user_details = self.workos_client.user_management.authenticate_with_password(
            email=settings.WORKOS_TESTUSER_EMAIL,
            password=settings.WORKOS_TESTUSER_PASSWORD,
        )

        return AuthenticateResponse(
            token=user_details.access_token,
        )
