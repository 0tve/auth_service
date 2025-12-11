import datetime as dt
import pathlib
import uuid

import fastapi
import jwt
import sqlalchemy as sa
from fastapi import security, status
from jwt import exceptions
from sqlalchemy.ext import asyncio as sa_asyncio

from auth_service.components import db, users, utils
from auth_service.entities import constants, models, schemas, enums

authentication_settings = schemas.AuthenticationSettings.get_from_env_file(
    pathlib.Path(constants.SETTINGS_FILE), enums.AuthenticationSettingsFields)
http_bearer = security.HTTPBearer()


async def login(request: schemas.AuthenticationUserLogin, session: sa_asyncio.AsyncSession) -> schemas.AuthenticationAccessToken:
    user = await users.fetch_user(session=session, email=request.email)
    if not (request.email == user.email and utils.hash_str(request.password) == user.password):
        raise fastapi.HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверные данные пользователя')
    expiration_time = dt.datetime.now(dt.timezone.utc) + dt.timedelta(
        minutes=float(authentication_settings.access_token_ttl_minutes))
    payload = {'user_id': str(user.id),
               'exp': expiration_time.timestamp(),
               'jti': str(uuid.uuid4())}
    token = jwt.encode(payload=payload, key=authentication_settings.secret_key,
                       algorithm=authentication_settings.algorithm)
    return schemas.AuthenticationAccessToken(access_token=token, token_type='bearer')


async def logout(credentials: security.HTTPAuthorizationCredentials, session: sa_asyncio.AsyncSession) -> None:
    try:
        payload: dict = jwt.decode(jwt=credentials.credentials, key=authentication_settings.secret_key, algorithms=[
                                   authentication_settings.algorithm])
        jti: str = payload.get('jti')
        if jti is None:
            raise fastapi.HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Не удалось идентифицировать токен')
        revoked_token = models.RevokedToken(jti=uuid.UUID(jti))
        session.add(revoked_token)
        await session.commit()
    except exceptions.ExpiredSignatureError:
        raise fastapi.HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Срок действия токена истек')
    except (exceptions.InvalidTokenError):
        raise fastapi.HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверный токен')


async def get_authenticated_user_id(credentials: security.HTTPAuthorizationCredentials = fastapi.Depends(http_bearer), session: sa_asyncio.AsyncSession = fastapi.Depends(db.get_session)) -> uuid.UUID:
    try:
        payload: dict = jwt.decode(jwt=credentials.credentials,
                                   key=authentication_settings.secret_key,
                                   algorithms=[authentication_settings.algorithm])
        user_id = uuid.UUID(payload.get('user_id'))
        jti: str = payload.get('jti')
        if user_id is None:
            raise fastapi.HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='В токене переданы неверные данные')
        if jti is None:
            raise fastapi.HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Не удалось идентифицировать токен')
        revoked_token = await session.scalar(sa.select(models.RevokedToken).where(models.RevokedToken.jti == uuid.UUID(jti)))
        if revoked_token:
            raise fastapi.HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен отозван')
        return user_id
    except exceptions.ExpiredSignatureError:
        raise fastapi.HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Срок действия токена истек')
    except exceptions.InvalidTokenError:
        raise fastapi.HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверный токен')
