"""Init module."""
from sqlalchemy.orm import declarative_base

from database.db_engine import DBSessionManager, get_async_db, get_db

# Define a declarative base for use in the models
Base = declarative_base()
# WATCHOUT for this - https://stackoverflow.com/questions/54118182/sqlalchemy-not-creating-tables


__all__ = ["Base", "get_db", "DBSessionManager", "get_async_db"]
