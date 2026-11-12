import json
from typing import Any

from starlette.responses import JSONResponse

from src.utils.serial import JSONExtendEncoder


class APIResponse(JSONResponse):

    def render(self, content: Any) -> bytes:
        return json.dumps(
            content,
            cls=JSONExtendEncoder,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(',', ':'),
        ).encode('utf-8')


def ok(data: Any = None) -> APIResponse:
    return APIResponse({'success': True, 'data': data})


def fail(error: str, http_status: int, headers: dict | None = None) -> APIResponse:
    return APIResponse(
        {'success': False, 'error': error},
        status_code=http_status,
        headers=headers,
    )
