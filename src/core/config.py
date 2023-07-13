from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    database_url: PostgresDsn

    # Auth
    access_token_expire_minutes: int
    jwt_signing_key: str
    accept_cookie = True
    accept_header = True


settings = Settings()
