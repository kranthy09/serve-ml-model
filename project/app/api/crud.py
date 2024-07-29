"""
Handles POST requests to create summaries
"""

from app.models.pydantic import SummaryPayloadSchema
from app.models.tortoise import TextSummary


async def post(payload: SummaryPayloadSchema) -> int:
    """Utility for creating a summary"""

    summary = TextSummary(
        url=payload.url,
        summary="dummy summary",
    )
    await summary.save()

    return summary.id
