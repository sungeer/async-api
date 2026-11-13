from starlette.middleware.base import BaseHTTPMiddleware

from src.utils.request_id import new_request_id


class RequestIDMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        request_id = new_request_id()

        request.state.request_id = request_id

        response = await call_next(request)

        response.headers['X-Request-ID'] = request_id
        return response
