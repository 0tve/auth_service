import pathlib

from auth_service.entities import constants, schemas, enums

db_default_credentials = schemas.DBCredentials.get_from_env_file(
    pathlib.Path(constants.SETTINGS_FILE), enums.DBDefaultCredentialsEnvFields)
db_credentials = schemas.DBCredentials.get_from_env_file(
    pathlib.Path(constants.SETTINGS_FILE), enums.DBCredentialsEnvFields)
