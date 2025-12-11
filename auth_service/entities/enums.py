import enum


class BusinessEntity(enum.Enum):
    user = 'Пользователь'
    permission = 'Право доступа'
    product = 'Товар'


class Operation(enum.Enum):
    create = 'Запись'
    read = 'Чтение'
    update = 'Изменение'
    delete = 'Удаление'


class AuthenticationSettingsFields(enum.Enum):
    secret_key = 'SECRET_KEY'
    algorithm = 'ALGORITHM'
    access_token_ttl_minutes = 'ACCESS_TOKEN_TTL_MINUTES'


class DBCredentialsEnvFields(enum.Enum):
    user = 'DB_USER'
    password = 'DB_PASSWORD'
    host = 'DB_HOST'
    port = 'DB_PORT'
    name_ = 'DB_NAME'

    @classmethod
    def get_name_field(cls) -> str:
        return cls.name_.name[:-1]


class DBDefaultCredentialsEnvFields(enum.Enum):
    user = 'DB_DEFAULT_USER'
    password = 'DB_DEFAULT_PASSWORD'
    host = 'DB_DEFAULT_HOST'
    port = 'DB_DEFAULT_PORT'
    name_ = 'DB_DEFAULT_NAME'

    @classmethod
    def get_name_field(cls) -> str:
        return cls.name_.name[:-1]
