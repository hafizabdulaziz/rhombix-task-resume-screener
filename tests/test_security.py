from src.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
)


def test_password_hashing():
    password = "secretpassword"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False

def test_jwt_tokens():
    data = {"sub": "recruiter@rhombix.com", "role": "Admin"}
    access_token = create_access_token(data)
    refresh_token = create_refresh_token(data)
    
    decoded_access = decode_token(access_token)
    assert decoded_access["sub"] == "recruiter@rhombix.com"
    assert decoded_access["role"] == "Admin"
    assert decoded_access["type"] == "access"

    decoded_refresh = decode_token(refresh_token)
    assert decoded_refresh["sub"] == "recruiter@rhombix.com"
    assert decoded_refresh["type"] == "refresh"
