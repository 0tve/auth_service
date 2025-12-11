import uuid

import fastapi
from fastapi import security
from sqlalchemy.ext import asyncio as sa_asyncio

from auth_service.components import authentication, db
from auth_service.entities import schemas

router = fastapi.APIRouter()


@router.post('/login')
async def login(
    request: schemas.AuthenticationUserLogin = fastapi.Depends(),
    session: sa_asyncio.AsyncSession = fastapi.Depends(db.get_session)
) -> schemas.AuthenticationAccessToken:
    return await authentication.login(request=request, session=session)


@router.post('/logout')
async def logout(
    credentials: security.HTTPAuthorizationCredentials = fastapi.Depends(
        authentication.http_bearer),
    session: sa_asyncio.AsyncSession = fastapi.Depends(db.get_session),
) -> None:
    return await authentication.logout(credentials=credentials, session=session)


# Для удобства тестирования
@router.get('/check_authentication')
async def check_authentication(
    user_id: uuid.UUID = fastapi.Depends(
        authentication.get_authenticated_user_id)
):
    return {'message': f'Вы прошли аутентификацию! Ваш id: {user_id}'}
