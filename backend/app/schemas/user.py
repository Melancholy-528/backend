"""
Pydantic schemas for User Authentication and Profile Management.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class UserSignUp(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100, description="Full name of applicant/entrepreneur")
    email: str = Field(..., description="Unique email address")
    password: str = Field(..., min_length=6, description="Password (min 6 characters)")
    phone: Optional[str] = Field(default=None, description="10-digit mobile number")
    category: Optional[str] = Field(default="General", description="Category: SC, ST, OBC, Women, Minority, PwD, General")
    state: Optional[str] = Field(default=None, description="Resident State")
    district: Optional[str] = Field(default=None, description="Resident District")
    annual_income: Optional[int] = Field(default=None, description="Annual household income in INR")


class UserLogin(BaseModel):
    email: str = Field(..., description="Registered email address")
    password: str = Field(..., description="Account password")


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    category: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    annual_income: Optional[int] = None


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: Optional[str] = None
    category: Optional[str] = "General"
    state: Optional[str] = None
    district: Optional[str] = None
    annual_income: Optional[int] = None
    saved_schemes: List[str] = Field(default_factory=list)
    created_at: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
