import fastapi
from fastapi import responses, status
from sqlalchemy import exc


def handle_integrity_error(request: fastapi.Request, exc: exc.IntegrityError):
    return responses.JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={'detail': str(exc)}
    )
