from typing import Optional

import requests
from dotenv import dotenv_values
from pydantic import BaseModel, EmailStr, ValidationError, validator

TIMEOUT = (1, 5)
URL = "http://localhost:8000/api"


class RegisterInput(BaseModel):
    email: EmailStr
    name: str
    password: str
    passwordConfirm: str
    photo: Optional[str]


class RegisterResponse(BaseModel):
    email: EmailStr
    name: str
    photo: Optional[str]
    status: str


def health_check_handler():
    resp = requests.get(f"{URL}/healthchecker", timeout=TIMEOUT)
    expected = {
        "message": "JWT Authentication in Rust using Actix-web",
        "status": "success",
    }

    assert resp.status_code == requests.codes.ok
    assert resp.json() == expected


def register():
    req = RegisterInput(
        email="test8@test.com",
        name="test",
        password="password123",
        passwordConfirm="password123",
    )

    expected_response = RegisterResponse(
        email="test8@test.com", name="test", photo="test.png", status="success"
    )

    resp = requests.post(f"{URL}/auth/register", json=req.dict(), timeout=TIMEOUT)

    output_dict = resp.json()
    output_response = RegisterResponse(
        email=output_dict["data"]["user"]["email"],
        name=output_dict["data"]["user"]["name"],
        status=output_dict["status"],
    )

    # print(f"{output_response.dict()=}")
    # print(f"{expected_response.dict()=}")
    # print(f"{output_response.dict() == expected_response.dict()}")

    assert resp.status_code == requests.codes.created
    assert output_response.dict() == expected_response.dict()


if __name__ == "__main__":
    try:
        health_check_handler()
        register()
    except requests.exceptions.Timeout:
        print("the request timed out")
    except ValidationError as err:
        print(f"validation error: {str(err)}")
    except AssertionError as err:
        print(f"assertion error: {err}")
    except Exception as err:
        print(f"an error occurred: {err}")
