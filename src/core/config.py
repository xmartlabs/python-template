from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    database_url: PostgresDsn
    server_url: str

    # Auth
    access_token_expire_minutes: int
    jwt_signing_key: str
    accept_cookie: bool = True
    accept_token: bool = True


settings = Settings()
