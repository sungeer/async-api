from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from src import settings
from src.utils.exceptions import UnauthorizedError


# 生成 JWT Access Token
def create_access_token(user_id, username, roles=None, expires_minutes=None) -> str:
    if expires_minutes is None:
        expires_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES

    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)

    if roles is None:
        roles = []

    payload = {
        'user_id': user_id,
        'username': username,
        'roles': roles,
        'exp': expire,
        'type': 'access',
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


# 解析 JWT Payload 不做业务校验
def _decode_token(token: str):
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except ExpiredSignatureError:
        raise UnauthorizedError('JWT token expired')
    except InvalidTokenError:
        raise UnauthorizedError('JWT token invalid or malformed')


# 验证 Access Token 并返回 payload
def verify_access_token(token: str):
    payload = _decode_token(token)
    if payload.get('type') != 'access':
        raise UnauthorizedError('JWT token type mismatch')
    return payload
