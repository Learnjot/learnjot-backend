from typing import Annotated
from db.base import database
from pydantic import BeforeValidator


def get_database():
    return database

PyObjectId = Annotated[str, BeforeValidator(str)]