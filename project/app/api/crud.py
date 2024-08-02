"""
Handles POST requests to create summaries
"""

from typing import List, Union

from app.models.pydantic import SummaryPayloadSchema
from app.models.tortoise import TextSummary


async def post(payload: SummaryPayloadSchema) -> TextSummary:
    """Utility for creating a summary"""

    summary = TextSummary(
        url=payload.url,
        summary="",
    )
    await summary.save()

    return summary.id


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


async def delete(id: int) -> int:
    """Utility for deleting a summary"""

    summary = await TextSummary.filter(id=id).delete()

    return summary


async def put(id: int, payload: SummaryPayloadSchema) -> Union[dict, None]:
    """Utiliy to update a summary"""

    summary = await TextSummary.filter(id=id).update(
        url=payload.url, summary=payload.summary
    )
    if summary:
        updated_summary = await TextSummary.filter(id=id).first().values()
        return updated_summary
    return None
