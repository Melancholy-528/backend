from typing import List, Optional
from pydantic import BaseModel, Field, model_validator


class Scheme(BaseModel):
    name: str
    scheme_code: Optional[str] = None
    ministry: Optional[str] = None
    description: Optional[str] = None
    eligible_categories: List[str] = Field(default_factory=list)
    eligible_category: Optional[str] = None  # Backward compatibility
    income_limit: Optional[int] = None
    max_project_cost: Optional[int] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    subsidy_percentage: Optional[float] = None
    benefits: List[str] = Field(default_factory=list)
    source_url: Optional[str] = None

    @model_validator(mode="after")
    def sync_categories(self):
        if self.eligible_categories:
            if not self.eligible_category:
                self.eligible_category = ", ".join(self.eligible_categories)
        elif self.eligible_category:
            cats = [c.strip() for c in self.eligible_category.split(",") if c.strip()]
            self.eligible_categories = cats
        return self