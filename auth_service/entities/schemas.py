import pathlib
import typing
import uuid

import pydantic

from auth_service.components import utils
from auth_service.entities import enums

str255 = typing.Annotated[str, pydantic.StringConstraints(max_length=255)]
EmailStr255 = typing.Annotated[pydantic.EmailStr,
                               pydantic. StringConstraints(max_length=255)]


class BaseDB(pydantic.BaseModel):
    """Базовая схема базы данных"""


class DBCredentials(BaseDB):
    user: str
    password: str
    host: str
    port: str
    name: str

    @property
    def url(self) -> str:
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'

    @classmethod
    def get_from_env_file(cls, env_path: pathlib.Path, fields: enums.DBCredentialsEnvFields | enums.DBDefaultCredentialsEnvFields) -> 'DBCredentials':
        env_vars = utils.load_env(env_path)
        try:
            return cls(
                user=env_vars[fields.user.value],
                password=env_vars[fields.password.value],
                host=env_vars[fields.host.value],
                port=env_vars[fields.port.value],
                name=env_vars[fields.name_.value],
            )
        except KeyError as exc:
            missing = exc.args[0]
            raise KeyError(f'Отсутствует ключ {missing} в {env_path}')


class BaseUser(pydantic.BaseModel):
    """Базовая схема пользователя"""


class User(BaseUser):
    id: uuid.UUID
    name: str255
    surname: str255
    patronymic: str255
    email: EmailStr255

    model_config = pydantic.ConfigDict(from_attributes=True)


class UserCreate(BaseUser):
    name: str255
    surname: str255
    patronymic: str255
    email: EmailStr255
    password: str
    password_repeated: str


class UserUpdate(BaseUser):
    name: str255 | None = None
    surname: str255 | None = None
    patronymic: str255 | None = None
    email: EmailStr255 | None = None
    password: str | None = None


class BasePermission(pydantic.BaseModel):
    """Базовая схема прав доступа"""


class Permission(BasePermission):
    id: uuid.UUID
    name: str255
    description: str | None = None
    create: bool = False
    read: bool = False
    update: bool = False
    delete: bool = False
    business_entity: enums.BusinessEntity

    model_config = pydantic.ConfigDict(from_attributes=True)


class PermissionCreate(BasePermission):
    name: str255
    description: str | None = None
    create: bool = False
    read: bool = False
    update: bool = False
    delete: bool = False
    business_entity: enums.BusinessEntity


class PermissionUpdate(BasePermission):
    name: str255 | None = None
    description: str | None = None
    create: bool = False
    read: bool = False
    update: bool = False
    delete: bool = False
    business_entity: enums.BusinessEntity | None = None


class BaseAuthentication(pydantic.BaseModel):
    """Базовая схема аутентификации"""


class AuthenticationUserLogin(BaseAuthentication):
    email: EmailStr255
    password: str


class AuthenticationSettings(BaseAuthentication):
    secret_key: str
    algorithm: str
    access_token_ttl_minutes: str

    @classmethod
    def get_from_env_file(cls, env_path: pathlib.Path, fields: enums.AuthenticationSettingsFields) -> 'AuthenticationSettings':
        env_vars = utils.load_env(env_path)
        try:
            return cls(
                secret_key=env_vars[fields.secret_key.value],
                algorithm=env_vars[fields.algorithm.value],
                access_token_ttl_minutes=env_vars[fields.access_token_ttl_minutes.value],
            )
        except KeyError as exc:
            missing = exc.args[0]
            raise KeyError(f'Отсутствует ключ {missing} в {env_path}')


class AuthenticationAccessToken(BaseAuthentication):
    access_token: str
    token_type: str = 'bearer'


class BaseUserPermission(pydantic.BaseModel):
    """Базовая схема прав доступа пользователя"""


class UserPermission(BaseUserPermission):
    user_id: uuid.UUID
    permission_id: uuid.UUID


class UserPermissions(BaseUserPermission):
    user_id: uuid.UUID
    permissions: list[Permission]


class PermissionUsers(BaseUserPermission):
    permission_id: uuid.UUID
    users: list[User]


class BaseProduct(pydantic.BaseModel):
    """Базовая схема товара"""


class Product(BaseProduct):
    name: str255
    id: uuid.UUID = uuid.uuid4()
    description: str | None = None


class ProductCreate(BaseProduct):
    name: str255
    description: str | None = None


class ProductUpdate(BaseProduct):
    name: str255 | None = None
    description: str | None = None
