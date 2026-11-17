from starlette.middleware.base import BaseHTTPMiddleware

from src.core import jwt_token
from src.utils.exceptions import UnauthorizedError


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        request.state.user = None
        request.state.auth_error = None

        auth = request.headers.get('Authorization')
        if auth:
            parts = auth.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                request.state.auth_error = 'invalid authorization header'
            else:
                try:
                    request.state.user = jwt_token.verify_access_token(parts[1])
                except UnauthorizedError as exc:
                    request.state.auth_error = exc.msg

        return await call_next(request)
