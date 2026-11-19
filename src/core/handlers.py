from loguru import logger
from starlette.requests import ClientDisconnect
from starlette.exceptions import HTTPException

from src.utils.exceptions import (
    BusinessError,
    ParamError,
    UpstreamUnavailableError,
    UnauthorizedError,
    ForbiddenError
)
from src.core.response import fail


# 业务失败
async def business_error(request, exc):
    logger.warning(
        'business error, method={}, path={}, msg={}',
        request.method, request.url.path, exc.msg,
    )
    # 前端通过 HTTP 状态 + success 判断
    # 业务拒绝是唯一允许 200 的失败场景
    return fail(exc.msg, http_status=200)


# 400 入参错误
async def param_error(request, exc):
    logger.warning(
        'param error, method={}, path={}, msg={}',
        request.method, request.url.path, exc.msg,
    )
    return fail(exc.msg, http_status=400)


# 503 上游依赖不可用
async def upstream_unavailable(request, exc):
    logger.exception(
        'upstream unavailable, path={}',
        request.url.path
    )
    return fail(exc.msg, http_status=503)


# 401 未登录
async def unauthorized_error(request, exc):
    logger.warning(
        'unauthorized, method={}, path={}, msg={}',
        request.method, request.url.path, exc.msg,
    )
    return fail(exc.msg, http_status=401)


# 403 无权限
async def forbidden_error(request, exc):
    return fail(exc.msg, http_status=403)


# 404 路由匹配不到
async def not_found(request, exc):
    return fail(exc.detail, http_status=404)


# 405 方法不对
async def method_not_allowed(request, exc):
    return fail(exc.detail, http_status=405)


# 客户端中途断开
async def client_disconnect(request, exc):
    return fail('client closed request', http_status=499)


# 所有未显式注册的 400 413 416 等
async def http_error(request, exc):
   logger.warning(
       'http error, method={}, path={}, status={}, msg={}',
       request.method, request.url.path, exc.status_code, exc.detail,
   )
   return fail(exc.detail, http_status=exc.status_code)


# 内部错误 500
async def server_error(request, exc):
    """兜底处理
    数据库崩了 依赖超时 等 系统级异常
    监控在这里感知
    """
    logger.exception(
        'unhandled server error path={}',
        request.url.path
    )
    return fail('internal server error', http_status=500)


exception_handlers = {
    HTTPException: http_error,  # 兜住 400/413/416 等所有未显式注册的
    404: not_found,
    405: method_not_allowed,
    BusinessError: business_error,  # 200
    ParamError: param_error,  # 400
    UpstreamUnavailableError: upstream_unavailable,  # 503
    UnauthorizedError: unauthorized_error,  # 401
    ForbiddenError: forbidden_error,  # 403
    ClientDisconnect: client_disconnect,  # 499
    Exception: server_error,
}
