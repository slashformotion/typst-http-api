from __future__ import annotations

import logging
import typst
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import StreamingResponse
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
import os

DEFAULT_CHUNK_SIZE = 1024
REQUEST_PER_MINUTES = os.getenv("TYPST_HTTP_API_REQUESTS_PER_MINUTES")


logger = logging.getLogger(__name__)

app = FastAPI(docs_url=None, redoc_url=None)

limiter = Limiter(key_func=get_remote_address)
if REQUEST_PER_MINUTES is not None:
    app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


Instrumentator().instrument(app).expose(app)


class CompilationError(BaseModel):
    reason: str
    content: str


@app.post("/")
@limiter.limit(f"{REQUEST_PER_MINUTES}/minute")
async def build(request: Request, response: Response):
    typst_bytes = await request.body()

    try:
        res = typst.compile(typst_bytes)
        logger.info(f"successfully build {len(typst_bytes)}")
    except RuntimeError as e:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        logger.error(f"failed to build {len(typst_bytes)}")
        return CompilationError(reason="Compilation error", content=str(e))

    def iterfile(
        input_bytes: bytes,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ):
        for i in range(0, len(input_bytes), chunk_size):
            yield input_bytes[i : i + chunk_size]

    return StreamingResponse(iterfile(res), media_type="application/pdf")
