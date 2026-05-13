from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Advanced Age Calculator"
    debug: bool = False
    secret_key: str = "your-secret-key-here"

    class Config:
        env_file = ".env"

settings = Settings()
