import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
import datetime as dt
from singleton_decorator import singleton
from typing import Optional


@singleton
class Auth:
    """Auth class for handling login, registering and retrieving jwt token. Passwords are hashed with the bcrypt
    function."""
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    secret = 'SECRET'

    def get_password_hash(self, password: str) -> str:
        """Get password hash using CryptoContext bcrypt."""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str):
        """Verify password given by user against the hashed password"""
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_jwt_token(self, user_id: str) -> str:
        """Encode a JWT token during user login."""
        payload = {
            'exp': dt.datetime.utcnow() + dt.timedelta(days=0, minutes=60),
            'iat': dt.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_jwt_token(self, token: str) -> Optional[str]:
        """Decode a user token and check if (still) valid for a user before making request."""
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='JWT signature token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid JWT token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)) -> str:
        """Wrapper to use for authentication in requests to server."""
        username = self.decode_jwt_token(auth.credentials)
        return username
