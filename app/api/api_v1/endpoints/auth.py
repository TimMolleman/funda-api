from fastapi import APIRouter, HTTPException
from sqlalchemy import exc

from api.api_v1.util.auth_logic import Auth
from api.api_v1.schemas.api_schemas import AuthDetails
from connections.funda_db import FundaDB

router = APIRouter()


@router.post('/register', status_code=201)
def register(auth_details: AuthDetails):
    """Endpoint for registering user. On double username return status code 409. On success code 201."""
    hashed_password = Auth().get_password_hash(auth_details.password)

    try:
        FundaDB().insert_new_user(auth_details.username, hashed_password)
    except exc.IntegrityError:
        raise HTTPException(status_code=409, detail='Username is already taken')

    return {'username': auth_details.username}


@router.post('/login', status_code=201)
def login(auth_details: AuthDetails):
    """Endpoint for login of user. Return 401 if username not available or password wrong. On success code 201."""
    user_info = FundaDB().get_user_info(auth_details.username)

    if not user_info:
        raise HTTPException(status_code=401, detail='Username does not exist')
    if not Auth().verify_password(auth_details.password, user_info['password']):
        raise HTTPException(status_code=401, detail=f'Password is incorrect for user {user_info["username"]}')

    # Encode JWT token and return to user
    token = Auth().encode_jwt_token(user_info['username'])
    return {'token': token}
