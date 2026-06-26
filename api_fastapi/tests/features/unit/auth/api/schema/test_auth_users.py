import pytest
from pydantic import ValidationError

from app.features.auth.api.schemas.auth_schema import LoginRequest, RegisterRequest

def test_register_request_accepts_vlid_payload() -> None:
    payload = RegisterRequest(
        name="Victor Ramos",
        email="victor@email.com",
        password="12345678",
    )

    assert payload.name == "Victor Ramos"
    assert payload.email == "victor@email.com"
    assert payload.password == "12345678"
    
    
def test_register_request_rejects_invalid_email() -> None:
    with pytest.raises(ValidationError):
        RegisterRequest(
            name="Victor Ramos",
            email="email-invalido",
            password="12345678",
        )


def test_register_request_rejects_short_password() -> None:
    with pytest.raises(ValidationError):
        RegisterRequest(
            name="Victor Ramos",
            email="victor@email.com",
            password="123",
        )


def test_login_request_accepts_valid_payload() -> None:
    payload = LoginRequest(
        email="victor@email.com",
        password="12345678",
    )

    assert payload.email == "victor@email.com"
    assert payload.password == "12345678"