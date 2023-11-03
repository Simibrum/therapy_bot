"""Init module."""
from sqlalchemy.orm import declarative_base
from database.db_engine import get_db

# Define a declarative base for use in the models
Base = declarative_base()
# WATCHOUT for this - https://stackoverflow.com/questions/54118182/sqlalchemy-not-creating-tables
