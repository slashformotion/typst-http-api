from __future__ import annotations

import logging
import os
import tempfile
from pathlib import Path

import typst
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.responses import StreamingResponse
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.datastructures import UploadFile

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


@app.post("/project")
@limiter.limit(f"{REQUEST_PER_MINUTES}/minute")
async def build_project(request: Request, response: Response):
    form_data = await request.form()
    with tempfile.TemporaryDirectory(suffix="_typst") as td:
        for field_name, file_obj in form_data.items():
            if isinstance(file_obj, UploadFile):
                if ".." in field_name:
                    raise HTTPException(
                        status_code=400, detail="no field names can contain '..'"
                    )
                with open(Path(td) / field_name, "wb") as f:
                    f.write(await file_obj.read())

        try:
            res = typst.compile(Path(td) / "main.typ")
        except RuntimeError as e:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            logger.error(f"failed to build {1}")
            return CompilationError(reason="Compilation error", content=str(e))

        def iterfile(
            input_bytes: bytes,
            chunk_size: int = DEFAULT_CHUNK_SIZE,
        ):
            for i in range(0, len(input_bytes), chunk_size):
                yield input_bytes[i : i + chunk_size]

        return StreamingResponse(iterfile(res), media_type="application/pdf")
