import uuid

import fastapi
from fastapi import status
from sqlalchemy.ext import asyncio as sa_asyncio

from auth_service.components import authentication, db, user_permissions
from auth_service.entities import enums, schemas


async def get_user_entity_permissions(business_entity: enums.BusinessEntity, user_id: uuid.UUID = fastapi.Depends(authentication.get_authenticated_user_id), session: sa_asyncio.AsyncSession = fastapi.Depends(db.get_session)):
    user_permission_list = (await user_permissions.get_user_permissions(user_id=user_id, session=session)).permissions
    user_entity_permissions = None
    for user_permission in user_permission_list:
        if user_permission.business_entity == business_entity:
            user_entity_permissions = user_permission
    if user_entity_permissions is None:
        raise fastapi.HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,
                                    detail='У пользователя не заданы доступы для данной бизнес-сущности')
    return user_entity_permissions


def check_user_permissions(user_entity_permissions: schemas.Permission, required_permissions: schemas.Permission):
    missing_permissions = [] 
    if required_permissions.create and not user_entity_permissions.create:
        missing_permissions.append(enums.Operation.create.value)
    if required_permissions.read and not user_entity_permissions.read:
        missing_permissions.append(enums.Operation.read.value)
    if required_permissions.update and not user_entity_permissions.update:
        missing_permissions.append(enums.Operation.update.value)
    if required_permissions.delete and not user_entity_permissions.delete:
        missing_permissions.append(enums.Operation.delete.value)
    if missing_permissions:
        raise fastapi.HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail=f'У пользователя не хватает прав {', '.join(missing_permissions)} для бизнес-сущности {required_permissions.business_entity.value}')


def get_required_permissions(business_entity: enums.BusinessEntity, operations: list[enums.Operation]):
    return schemas.Permission(
        id=uuid.uuid4(),
        name='required_permission',
        create=enums.Operation.create in operations,
        read=enums.Operation.read in operations,
        update=enums.Operation.update in operations,
        delete=enums.Operation.delete in operations,
        business_entity=business_entity,
    )


def require_permissions(
    business_entities: list[enums.BusinessEntity],
    operations: list[enums.Operation],
) -> fastapi.Depends:
    async def permission_checker(
        user_id: uuid.UUID = fastapi.Depends(
            authentication.get_authenticated_user_id),
        session: sa_asyncio.AsyncSession = fastapi.Depends(db.get_session),
    ) -> None:
        for business_entity in business_entities:
            user_entity_permissions = await get_user_entity_permissions(
                business_entity=business_entity,
                user_id=user_id,
                session=session
            )
            required_permissions = get_required_permissions(
                business_entity=business_entity,
                operations=operations
            )
            check_user_permissions(user_entity_permissions=user_entity_permissions,
                                   required_permissions=required_permissions)

    return fastapi.Depends(permission_checker)
