import pydantic

from fastapi import (
    Request,
    status,
)
from fastapi.responses import JSONResponse

# fastapi docs on error handlers: https://fastapi.tiangolo.com/tutorial/handling-errors/?h=error#install-custom-exception-handlers
async def handle_pydantic_validation_errors(request: Request, exc: pydantic.ValidationError):
    errors = exc.errors()

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": [
                {
                "msg": error["msg"],
                "input": error["input"],
                }
                for error in errors
            ]
        },
    )