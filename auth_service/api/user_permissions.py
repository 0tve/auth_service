import uuid

import fastapi
from sqlalchemy.ext import asyncio as sa_asyncio

from auth_service.components import authorization, db, user_permissions
from auth_service.entities import enums, schemas

router = fastapi.APIRouter()
business_entities = [enums.BusinessEntity.user,
                     enums.BusinessEntity.permission]


@router.post(
    '/user_permissions',
    dependencies=[
        authorization.require_permissions(
            business_entities=business_entities, operations=[
                enums.Operation.create]
        )
    ],
)
async def create_user_permission(
    request: schemas.UserPermission = fastapi.Depends(),
    session: sa_asyncio.AsyncSession = fastapi.Depends(db.get_session)
) -> schemas.UserPermission:
    return await user_permissions.create_user_permission(request=request, session=session)


@router.delete(
    '/user_permissions',
    dependencies=[
        authorization.require_permissions(
            business_entities=business_entities, operations=[
                enums.Operation.delete]
        )
    ],
)
async def delete_user_permission(
    request: schemas.UserPermission = fastapi.Depends(),
    session: sa_asyncio.AsyncSession = fastapi.Depends(db.get_session)
) -> None:
    return await user_permissions.delete_user_permission(request=request, session=session)


@router.get(
    '/user_permissions/{user_id}',
    dependencies=[
        authorization.require_permissions(
            business_entities=business_entities, operations=[
                enums.Operation.read]
        )
    ],
)
async def get_user_permissions(
    user_id: uuid.UUID,
    session: sa_asyncio.AsyncSession = fastapi.Depends(db.get_session)
) -> schemas.UserPermissions:
    return await user_permissions.get_user_permissions(user_id=user_id, session=session)


@router.get(
    '/permission_users/{permission_id}',
    dependencies=[
        authorization.require_permissions(
            business_entities=business_entities, operations=[
                enums.Operation.read]
        )
    ],
)
async def get_permission_users(
    permission_id: uuid.UUID,
    session: sa_asyncio.AsyncSession = fastapi.Depends(db.get_session)
) -> schemas.PermissionUsers:
    return await user_permissions.get_permission_users(permission_id=permission_id, session=session)
