import uuid

import fastapi
from fastapi import security, status
from sqlalchemy.ext import asyncio as sa_asyncio

from auth_service.components import authentication, authorization, db, users
from auth_service.entities import enums, schemas

router = fastapi.APIRouter()
business_entity = enums.BusinessEntity.user


@router.post('/users')
async def create_user(
    request: schemas.UserCreate = fastapi.Depends(),
    session: sa_asyncio.AsyncSession = fastapi.Depends(db.get_session),
) -> schemas.User:
    return await users.create_user(request=request, session=session)


@router.get(
    '/users',
    dependencies=[
        authorization.require_permissions(
            business_entities=[business_entity], operations=[
                enums.Operation.read]
        )
    ],
)
async def get_users(
    limit: int = fastapi.Query(default=100, ge=1),
    session: sa_asyncio.AsyncSession = fastapi.Depends(db.get_session),
) -> list[schemas.User]:
    return await users.get_users(limit=limit, session=session)


@router.get(
    '/users/{id}',
    dependencies=[
        authorization.require_permissions(
            business_entities=[business_entity], operations=[
                enums.Operation.read]
        )
    ],
)
async def get_user(
    id: uuid.UUID,
    session: sa_asyncio.AsyncSession = fastapi.Depends(db.get_session),
) -> schemas.User:
    return await users.get_user(id=id, session=session)


@router.patch(
    '/users/{id}',
    dependencies=[
        authorization.require_permissions(
            business_entities=[business_entity], operations=[
                enums.Operation.update]
        )
    ],
)
async def update_user(
    id: uuid.UUID,
    request: schemas.UserUpdate = fastapi.Depends(),
    session: sa_asyncio.AsyncSession = fastapi.Depends(db.get_session),
) -> schemas.User:
    return await users.update_user(id=id, request=request, session=session)


@router.delete(
    '/users/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        authorization.require_permissions(
            business_entities=[business_entity], operations=[
                enums.Operation.delete]
        )
    ],
)
async def delete_user(
    id: uuid.UUID,
    credentials: security.HTTPAuthorizationCredentials = fastapi.Depends(
        authentication.http_bearer),
    session: sa_asyncio.AsyncSession = fastapi.Depends(db.get_session),
) -> None:
    await users.delete_user(id=id, session=session)
    # await authentication.logout(credentials=credentials, session=session)
