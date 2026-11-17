import functools

from src.utils.exceptions import UnauthorizedError, ForbiddenError


# 登录校验
def login_required(func):
    @functools.wraps(func)
    async def wrapper(request, *args, **kwargs):
        user = request.state.user
        if user is None:
            auth_error = request.state.auth_error
            if not auth_error:
                auth_error = 'please login first'
            raise UnauthorizedError(auth_error)
        return await func(request, *args, **kwargs)

    return wrapper


# 权鉴
def permission_required(scope):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(request, *args, **kwargs):
            user = request.state.user
            if user is None:
                auth_error = request.state.auth_error
                if not auth_error:
                    auth_error = 'please login first'
                raise UnauthorizedError(auth_error)
            if scope not in user['roles']:
                raise ForbiddenError(f'permission denied: requires scope [{scope}]')
            return await func(request, *args, **kwargs)

        return wrapper

    return decorator
