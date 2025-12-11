import uuid

import fastapi
from fastapi import status

from auth_service.components import authorization, products
from auth_service.entities import enums, schemas

router = fastapi.APIRouter()
business_entity = enums.BusinessEntity.product


@router.post(
    '/products',
    dependencies=[
        authorization.require_permissions(
            business_entities=[business_entity], operations=[
                enums.Operation.create]
        )
    ],
)
def create_product(
    request: schemas.ProductCreate = fastapi.Depends(),
) -> schemas.Product:
    return products.create_product(request=request)


@router.delete(
    '/products/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        authorization.require_permissions(
            business_entities=[business_entity], operations=[
                enums.Operation.delete]
        )
    ],
)
def delete_product(id: uuid.UUID) -> None:
    return products.delete_product(id=id)


@router.patch(
    '/products/{id}',
    dependencies=[
        authorization.require_permissions(
            business_entities=[business_entity], operations=[
                enums.Operation.update]
        )
    ],
)
def update_product(
    id: uuid.UUID, request: schemas.ProductUpdate = fastapi.Depends()
) -> schemas.Product:
    return products.update_product(id=id, request=request)


@router.get('/products',)
def get_products() -> list[schemas.Product]:
    return products.get_products()


@router.get('/products/{id}')
def get_product(id: uuid.UUID) -> schemas.Product:
    return products.get_product(id=id)
