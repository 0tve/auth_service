import uuid

import fastapi
from fastapi import status

from auth_service.entities import schemas

products = {}


def create_product(request: schemas.ProductCreate) -> schemas.Product:
    id = uuid.uuid4()
    product = schemas.Product(
        id=id, name=request.name, description=request.description)
    products.update({id: product})
    return product


def delete_product(id: uuid.UUID) -> None:
    product = products.pop(id, None)
    if product is None:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Товар не найден')


def update_product(id: uuid.UUID, request: schemas.ProductUpdate) -> schemas.Product:
    product = products.get(id)
    if product is None:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Товар не найден')
    update_data = request.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    return product


def get_products() -> list[schemas.Product]:
    return list(products.values())


def get_product(id: uuid.UUID) -> schemas.Product:
    product = products.get(id)
    if product is None:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Товар не найден')
    return product
