from typing import Optional
from pydantic import BaseModel


class Applicant(BaseModel):
    category: str
    annual_income: int
    project_cost: int
    age: Optional[int] = None
    gender: Optional[str] = None
    occupation: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None