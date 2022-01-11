import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
import datetime as dt
from singleton_decorator import singleton


@singleton
class Auth:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    secret = 'SECRET'

    def get_password_hash(self, password: str) -> str:
        """Get password hash using CryptoContext bcrypt."""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_jwt_token(self, user_id):
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

    def decode_jwt_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='JWT signature token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid JWT token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        username = self.decode_jwt_token(auth.credentials)
        return username
