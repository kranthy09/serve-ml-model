"""
Pydantic Models for app/models.
"""

from pydantic import BaseModel


class SummaryPayloadSchema(BaseModel):
    """Schema for summary payload"""

    url: str


class SummaryResponseSchema(SummaryPayloadSchema):
    """Schema for summary response"""

    id: int
