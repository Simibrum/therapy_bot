"""Configuration for the backend."""
import os
import tempfile
from pathlib import Path
from typing import ClassVar

from zoneinfo import ZoneInfo

from config.helper_functions import load_from_env_file
from config.init_logger import logger

# Load environment variables from .env file
load_from_env_file()

# Load API Key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

# Generate a secret key for the JWT
SECRET_KEY = os.getenv("SECRET_KEY", "dummy_secret_key")

# Get Frontend URL
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# Set the token time out value
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Set Timezone
TIMEZONE = os.getenv("TIMEZONE", "UTC")
TZ_INFO = ZoneInfo(TIMEZONE)

# GPU settings
USE_GPU = os.getenv("USE_GPU", "False").lower() == "true"

# SPACY Model
SPACY_MODEL = os.getenv("SPACY_MODEL", "en_core_web_sm")

# ASYNC - whether to use async database
ASYNC_DB = os.getenv("ASYNC_DB", "True").lower() == "true"


class ProductionConfig:
    """Production configuration - e.g. for remote deployment."""

    name = "production"
    # Database setup
    # Use an SQLite database for now - in database folder that is sibling of parent config folder
    DATABASE_FILE: ClassVar[Path] = Path(__file__).parent.parent / "database" / "database.db"
    SQLALCHEMY_DATABASE_URI: ClassVar[str] = f"sqlite:///{DATABASE_FILE}"
    SQLALCHEMY_ENGINE_OPTIONS: ClassVar[dict] = {"connect_args": {"check_same_thread": False}}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 12


class DevelopmentConfig:
    """Development configuration - e.g. for local dev."""

    name = "development"
    # Use an SQLite database for now - in database folder that is sibling of parent config folder
    DATABASE_FILE: ClassVar[Path] = Path(__file__).parent.parent / "database" / "dev_database.db"
    SQLALCHEMY_DATABASE_URI: ClassVar[str] = f"sqlite:///{DATABASE_FILE}"
    SQLALCHEMY_ENGINE_OPTIONS: ClassVar[dict] = {"connect_args": {"check_same_thread": False}}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4


class TestConfig:
    """Test configuration - e.g. for local dev."""

    name = "local_test"
    # Switch to temporary file-based DB to avoid issues with DB data being reset between tests
    DATABASE_FILE: ClassVar[Path] = None
    SQLALCHEMY_DATABASE_URI: ClassVar[str] = None
    if ASYNC_DB:
        SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///:memory:"
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ENGINE_OPTIONS: ClassVar[dict] = {"connect_args": {"check_same_thread": False}}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4  # Use a low value for faster tests; the default is 12
    DEBUG = True

    @classmethod
    def generate_temp_file(cls) -> None:
        """Generate a temporary database file and update the configuration."""
        cls.DATABASE_FILE = Path(tempfile.mkstemp()[1])
        if ASYNC_DB:
            cls.SQLALCHEMY_DATABASE_URI = f"sqlite+aiosqlite:///{cls.DATABASE_FILE}"
        else:
            cls.SQLALCHEMY_DATABASE_URI = f"sqlite:///{cls.DATABASE_FILE}"

    @staticmethod
    def remove_temp_file() -> None:
        """Remove the temporary database file."""
        TestConfig.DATABASE_FILE.unlink()


class AsyncConfig:
    """Asynchronous configuration - for async database operations."""

    name = "async"

    # Determine which async database to use
    ASYNC_DB_TYPE = os.getenv("ASYNC_DB_TYPE", "sqlite").lower()

    if ASYNC_DB_TYPE == "postgres":
        # PostgreSQL configuration
        DB_USER = os.getenv("POSTGRES_USER", "user")
        DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
        DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
        DB_PORT = os.getenv("POSTGRES_PORT", "5432")
        DB_NAME = os.getenv("POSTGRES_DB", "asyncdb")
        SQLALCHEMY_DATABASE_URI: ClassVar[
            str
        ] = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        # SQLite configuration (default)
        DB_FILE = os.getenv("SQLITE_DB_FILE", "async_sqlite.db")
        DB_PATH = Path(__file__).parent.parent / "database" / DB_FILE
        SQLALCHEMY_DATABASE_URI: ClassVar[str] = f"sqlite+aiosqlite:///{DB_PATH}"

    SQLALCHEMY_ENGINE_OPTIONS: ClassVar[dict] = {
        "echo": True,  # Set to False in production
        "pool_pre_ping": True,
    }
    if ASYNC_DB_TYPE == "postgres":
        SQLALCHEMY_ENGINE_OPTIONS.update(
            {
                "pool_size": 5,
                "max_overflow": 10,
            }
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    DEBUG = True  # Set to False in production
    BCRYPT_LOG_ROUNDS = 12


def get_config() -> object:
    """Set the working environment."""
    logger.debug("Getting config")
    # Config to use
    config_env = os.environ.get("CONFIG_ENV", "development")

    if config_env == "production":
        logger.debug("Using production config")
        config = ProductionConfig
    elif config_env == "development":
        logger.debug("Using development config")
        config = DevelopmentConfig
    elif config_env == "testing":
        logger.debug("Using test config")
        config = TestConfig
    elif config_env == "async":
        logger.debug(f"Using async config with {AsyncConfig.ASYNC_DB_TYPE}")
        config = AsyncConfig
    else:
        logger.debug("Using testing config as default")
        config = TestConfig
    return config
