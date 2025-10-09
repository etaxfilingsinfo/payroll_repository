from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # --- Pydantic V2/V3 Configuration ---
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    
    # Database connection details
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    # JWT secret key and token expiration time
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # Default 60 minutes

    # Google OAuth credentials
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/google/callback"

    @property
    def DATABASE_URL(self) -> str:
        """
        Assembles the full database connection URL using the base 'postgresql' dialect.
        This setup works with both the synchronous Alembic tool and the asynchronous
        database engine in the application.
        """
        driver_dialect = "postgresql"  # Base dialect
        return f"{driver_dialect}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

# Instantiate the settings object to be used throughout the application
settings = Settings()
