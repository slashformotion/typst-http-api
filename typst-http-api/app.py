from __future__ import annotations

import typst
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import logging

from prometheus_fastapi_instrumentator import Instrumentator

DEFAULT_CHUNK_SIZE = 1024

app = FastAPI()

Instrumentator().instrument(app).expose(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CompilationError(BaseModel):
    reason: str
    content: str


@app.post("/")
async def build(req: Request, response: Response):
    typst_bytes = await req.body()

    try:
        res = typst.compile(typst_bytes)
    except RuntimeError as e:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return CompilationError(reason="Compilation error", content=str(e))

    def iterfile(
        input_bytes: bytes,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ):
        for i in range(0, len(input_bytes), chunk_size):
            yield input_bytes[i : i + chunk_size]

    return StreamingResponse(iterfile(res), media_type="application/pdf")
