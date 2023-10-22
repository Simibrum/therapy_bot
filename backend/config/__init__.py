"""Configuration for the backend."""
import os
import tempfile
from config.init_logger import logger

# Load API Key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")


class ProductionConfig:
    """Production configuration - e.g. for remote deployment."""
    name = "production"
    # Database setup
    # Use an SQLite database for now - in database folder
    DATABASE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database", "database.db")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_FILE}"
    SQLALCHEMY_ENGINE_OPTIONS = {'connect_args': {'check_same_thread': False}}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 12


class TestConfig:
    """Test configuration - e.g. for local dev."""
    name = "local_test"
    # Switch to temporary file-based DB to avoid issues with DB data being reset between tests
    DATABASE_FILE = None
    SQLALCHEMY_DATABASE_URI = None
    # SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ENGINE_OPTIONS = {'connect_args': {'check_same_thread': False}}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4  # Use a low value for faster tests; the default is 12
    DEBUG = True

    @classmethod
    def generate_temp_file(cls):
        """Generate a temporary database file and update the configuration."""
        cls.DATABASE_FILE = tempfile.mkstemp()[1]
        cls.SQLALCHEMY_DATABASE_URI = f"sqlite:///{cls.DATABASE_FILE}"

    @staticmethod
    def remove_temp_file():
        os.remove(TestConfig.DATABASE_FILE)


def get_config():
    """Set the working environment."""
    logger.debug("Getting config")
    # Config to use
    config_env = os.environ.get('CONFIG_ENV', 'development')

    if config_env == "production":
        logger.debug("Using production config")
        config = ProductionConfig
    elif config_env == "testing":
        logger.debug("Using test config")
        config = TestConfig
    else:
        logger.debug("Using testing config as default")
        config = TestConfig
    return config
