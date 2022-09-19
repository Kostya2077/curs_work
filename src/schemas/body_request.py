from pydantic import BaseModel
from src.schemas.request_model import RequestModel


class BodyRequestModel(BaseModel):
    method: str
    test_model: RequestModel = None


class BodyDatabaseModel(BaseModel):
    method: str
    database_name: str = None
    test_name: str = None


class BodyTestRequestModel(BaseModel):
    method: str
    result_success: bool = None
    db_name: str = None


















