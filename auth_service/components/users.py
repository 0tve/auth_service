import uuid

import fastapi
import sqlalchemy as sa
from fastapi import status
from sqlalchemy.ext import asyncio as sa_asyncio
from sqlalchemy import exc

from auth_service.components import db, user_permissions, utils
from auth_service.entities import enums, models, schemas


async def fetch_user(session: sa_asyncio.AsyncSession, id: uuid.UUID | None = None, email: schemas.EmailStr255 | None = None) -> models.User:
    if id is None and email is None:
        raise fastapi.HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail='Нужно предоставить id или email')
    attr, value = ('id', id) if id is not None else ('email', email)
    user = await session.scalar(sa.select(models.User).where(getattr(models.User, attr) == value))
    if user is None or not user.is_active:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не существует')
    return user


async def create_user(request: schemas.UserCreate, session: sa_asyncio.AsyncSession) -> schemas.User:
    if request.password != request.password_repeated:
        raise fastapi.HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail='Пароли не совпадают')
    user = models.User(
        name=request.name,
        surname=request.surname,
        patronymic=request.patronymic,
        email=request.email,
        password=utils.hash_str(request.password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return schemas.User.model_validate(user)


async def get_users(
    limit: int,
    session: sa_asyncio.AsyncSession,
) -> list[schemas.User]:
    users = await session.scalars(sa.select(models.User).limit(limit))
    return [schemas.User.model_validate(user) for user in users.all()]


async def get_user(id: uuid.UUID, session: sa_asyncio.AsyncSession) -> schemas.User:
    user = await fetch_user(session, id)
    return schemas.User.model_validate(user)


async def update_user(id: uuid.UUID, request: schemas.UserUpdate, session: sa_asyncio.AsyncSession) -> schemas.User:
    user = await fetch_user(session, id)
    update_data = request.model_dump(exclude_none=True)
    if 'password' in update_data:
        update_data['password'] = utils.hash_str(update_data['password'])
    for field, value in update_data.items():
        setattr(user, field, value)
    await session.commit()
    await session.refresh(user)
    return schemas.User.model_validate(user)


async def delete_user(id: uuid.UUID, session: sa_asyncio.AsyncSession) -> None:
    user = await fetch_user(session, id)
    user.is_active = False
    await session.commit()


async def create_admin():
    async with db.async_sessionmaker() as session:
        admin_email = 'admin@admin.ru'
        try:
            if await fetch_user(session=session, email=admin_email):
                return
        except:
            pass

        user = models.User(
            name='admin',
            surname='admin',
            patronymic='admin',
            email=admin_email,
            password=utils.hash_str('admin'),
        )
        session.add(user)
        await session.flush()
        await session.refresh(user)

        admin_permissions: list[models.Permission] = []
        for business_entity in enums.BusinessEntity:
            permission = models.Permission(
                name=f'Права администратора на {business_entity.value}',
                create=True,
                read=True,
                update=True,
                delete=True,
                business_entity=business_entity.value,
            )
            session.add(permission)
            await session.flush()
            await session.refresh(permission)
            admin_permissions.append(permission)
        user.permissions = admin_permissions
        await session.commit()
        await session.refresh(user)
