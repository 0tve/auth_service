import uuid
import fastapi
from fastapi import status
from sqlalchemy.ext import asyncio as sa_asyncio

from auth_service.components import permissions, users
from auth_service.entities import schemas


async def create_user_permission(request: schemas.UserPermission, session: sa_asyncio.AsyncSession) -> schemas.UserPermission:
    user = await users.fetch_user(session=session, id=request.user_id)
    permission = await permissions.fetch_permission(session=session, id=request.permission_id)
    for user_permission in user.permissions:
        if user_permission.business_entity == permission.business_entity:
            raise fastapi.HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    'У пользователя уже есть правило для данной бизнес-сущности. Вы должны изменить это правило вместо добавления нового.')
            )
    user.permissions.append(permission)
    await session.commit()
    await session.refresh(user)
    return schemas.UserPermission(user_id=request.user_id, permission_id=request.permission_id)


async def delete_user_permission(request: schemas.UserPermission, session: sa_asyncio.AsyncSession) -> None:
    user = await users.fetch_user(session=session, id=request.user_id)
    permission = await permissions.fetch_permission(session=session, id=request.permission_id)
    user.permissions.remove(permission)
    await session.commit()
    await session.refresh(user)


async def get_user_permissions(user_id: uuid.UUID, session: sa_asyncio.AsyncSession) -> schemas.UserPermissions:
    user = await users.fetch_user(session=session, id=user_id)
    return schemas.UserPermissions(user_id=user_id, permissions=user.permissions)


async def get_permission_users(permission_id: uuid.UUID, session: sa_asyncio.AsyncSession) -> schemas.PermissionUsers:
    permission = await permissions.fetch_permission(session=session, id=permission_id)
    return schemas.PermissionUsers(permission_id=permission_id, users=permission.users)
