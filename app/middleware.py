import logging

from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.database import SessionLocal
from app.models import RequestResponseLog

logger = logging.getLogger(__name__)


class RequestResponseLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_body = await request.body()

        response = await call_next(request)

        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        try:
            async with SessionLocal() as session:
                session.add(
                    RequestResponseLog(
                        method=request.method,
                        path=request.url.path,
                        query_params=str(request.query_params) or None,
                        request_body=request_body.decode("utf-8", errors="replace")
                        or None,
                        response_status=response.status_code,
                        response_body=response_body.decode("utf-8", errors="replace")
                        or None,
                    )
                )
                await session.commit()
        except SQLAlchemyError:
            logger.exception("Failed to persist request/response log")

        headers = {
            key: value
            for key, value in response.headers.items()
            if key.lower() != "content-length"
        }
        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=headers,
            media_type=response.media_type,
        )
