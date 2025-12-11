import uuid

import fastapi
from sqlalchemy.ext import asyncio as sa_asyncio

from auth_service.components import authorization, db, permissions
from auth_service.entities import enums, schemas

router = fastapi.APIRouter()
business_entity = enums.BusinessEntity.permission


@router.post(
    '/permissions',
    dependencies=[
        authorization.require_permissions(
            business_entities=[business_entity], operations=[
                enums.Operation.create]
        )
    ],
)
async def create_permission(
    request: schemas.PermissionCreate = fastapi.Depends(),
    session: sa_asyncio.AsyncSession = fastapi.Depends(db.get_session),
) -> schemas.Permission:
    return await permissions.create_permission(request=request, session=session)


@router.get(
    '/permissions',
    dependencies=[
        authorization.require_permissions(
            business_entities=[business_entity], operations=[
                enums.Operation.read]
        )
    ],
)
async def get_permissions(
    limit: int = fastapi.Query(default=100, ge=1),
    session: sa_asyncio.AsyncSession = fastapi.Depends(db.get_session),
) -> list[schemas.Permission]:
    return await permissions.get_permissions(limit=limit, session=session)


@router.get(
    '/permissions/{id}',
    dependencies=[
        authorization.require_permissions(
            business_entities=[business_entity], operations=[
                enums.Operation.read]
        )
    ],
)
async def get_permission(
    id: uuid.UUID,
    session: sa_asyncio.AsyncSession = fastapi.Depends(db.get_session),
) -> schemas.Permission:
    return await permissions.get_permission(id=id, session=session)


@router.patch(
    '/permissions/{id}',
    dependencies=[
        authorization.require_permissions(
            business_entities=[business_entity], operations=[
                enums.Operation.update]
        )
    ],
)
async def update_permission(
    id: uuid.UUID,
    request: schemas.PermissionUpdate = fastapi.Depends(),
    session: sa_asyncio.AsyncSession = fastapi.Depends(db.get_session),
) -> schemas.Permission:
    return await permissions.update_permission(id=id, request=request, session=session)


@router.delete(
    '/permissions/{id}',
    status_code=204,
    dependencies=[
        authorization.require_permissions(
            business_entities=[business_entity], operations=[
                enums.Operation.delete]
        )
    ],
)
async def delete_permission(
    id: uuid.UUID,
    session: sa_asyncio.AsyncSession = fastapi.Depends(db.get_session),
) -> None:
    return await permissions.delete_permission(id=id, session=session)
