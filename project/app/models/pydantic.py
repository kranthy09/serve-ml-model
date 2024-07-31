"""
Pydantic Models for app/models.
"""

from pydantic import AnyHttpUrl, BaseModel


class SummaryPayloadSchema(BaseModel):
    """Schema for summary payload"""

    url: AnyHttpUrl


class SummaryResponseSchema(SummaryPayloadSchema):
    """Schema for summary response"""

    id: int


class SummaryUpdatePayloadSchema(SummaryPayloadSchema):
    """Schema for summary update payload"""

    summary: str
