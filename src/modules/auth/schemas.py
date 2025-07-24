from pydantic import BaseModel


class AuthenticateResponse(BaseModel):
    token: str
