from jose import JWTError, jwt

from core.config import config
from utils.time import get_utc_timestamp

JWT_SECRET = config.JWT_SECRET
JWT_EXPIRE = config.JWT_EXPIRE


class JWTService:
    @staticmethod
    def create_token(_id: int, _type: str) -> str:
        data = {
            'id': _id,
            'type': str(_type),
            'exp': get_utc_timestamp() + JWT_EXPIRE.total_seconds(),
            'iat': get_utc_timestamp()
        }
        encoded_jwt = jwt.encode(data, JWT_SECRET, algorithm="HS256")  # type: ignore
        return encoded_jwt

    @staticmethod
    def get_token_data(token: str) -> dict | None:
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms="HS256")  # type: ignore
            return payload
        except JWTError as e:
            print(e)
            return None
