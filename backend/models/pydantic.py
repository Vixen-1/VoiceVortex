from pydantic import BaseModel, Field
from enum import Enum

class QueryType(str, Enum):
    BUYER = "buyer"
    SUPPLIER = "supplier"

class QueryRequest(BaseModel):
    question: str = None
    type: QueryType = Field(..., description="Type of query, either 'buyer' or 'supplier'")