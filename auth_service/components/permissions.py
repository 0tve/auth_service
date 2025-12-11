import uuid

import fastapi
import sqlalchemy as sa
from fastapi import status
from sqlalchemy.ext import asyncio as sa_asyncio

from auth_service.entities import models, schemas


async def fetch_permission(session: sa_asyncio.AsyncSession, id: uuid.UUID) -> models.Permission:
    permission = await session.scalar(sa.select(models.Permission).where(models.Permission.id == id))
    if permission is None:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Право доступа не существует')
    return permission


async def create_permission(request: schemas.PermissionCreate, session: sa_asyncio.AsyncSession) -> schemas.Permission:
    permission = models.Permission(
        name=request.name,
        description=request.description,
        create=request.create,
        read=request.read,
        update=request.update,
        delete=request.delete,
        business_entity=request.business_entity.value,
    )
    session.add(permission)
    await session.commit()
    await session.refresh(permission)
    return schemas.Permission.model_validate(permission)


async def get_permissions(
    limit: int,
    session: sa_asyncio.AsyncSession,
) -> list[schemas.Permission]:
    permissions = await session.scalars(sa.select(models.Permission).limit(limit))
    return [schemas.Permission.model_validate(permission) for permission in permissions.all()]


async def get_permission(id: uuid.UUID, session: sa_asyncio.AsyncSession) -> schemas.Permission:
    permission = await fetch_permission(session, id)
    return schemas.Permission.model_validate(permission)


async def update_permission(id: uuid.UUID, request: schemas.PermissionUpdate, session: sa_asyncio.AsyncSession) -> schemas.Permission:
    permission = await fetch_permission(session, id)
    update_data = request.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(permission, field, value)
    await session.commit()
    await session.refresh(permission)
    return schemas.Permission.model_validate(permission)


async def delete_permission(id: uuid.UUID, session: sa_asyncio.AsyncSession) -> None:
    permission = await fetch_permission(session, id)
    await session.delete(permission)
    await session.commit()
