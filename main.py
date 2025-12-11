from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from sqlalchemy import exc

from auth_service.api import authentication, index, permissions, products, user_permissions
from auth_service.api import users as users_api
from auth_service.components import db, exceptions, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.ensure_db_exists()
    await db.create_tables()
    await users.create_admin()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(users_api.router)
app.include_router(permissions.router)
app.include_router(user_permissions.router)
app.include_router(authentication.router)
app.include_router(products.router)
app.include_router(index.router)
app.add_exception_handler(exc.IntegrityError,
                          exceptions.handle_integrity_error)

if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True)
