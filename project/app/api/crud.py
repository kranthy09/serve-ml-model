"""
Handles POST requests to create summaries
"""

from typing import List


from typing import Union

from app.models.pydantic import SummaryPayloadSchema
from app.models.tortoise import TextSummary


async def post(payload: SummaryPayloadSchema) -> TextSummary:
    """Utility for creating a summary"""

    summary = TextSummary(
        url=payload.url,
        summary="dummy summary",
    )
    await summary.save()

    return summary


async def get(id: int) -> Union[dict, None]:
    """Utility for getting a summary"""

    summary = await TextSummary.filter(id=id).first().values()
    if summary:
        return summary
    return None


async def get_all() -> List:
    """Utility for getting all summaries"""

    summaries = await TextSummary.all().values()
    return summaries
