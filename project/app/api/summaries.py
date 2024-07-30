"""
API to add a summary
"""

from typing import List


from fastapi import APIRouter, HTTPException

from app.api import crud
from app.models.pydantic import SummaryPayloadSchema, SummaryResponseSchema
from app.models.tortoise import SummarySchema

router = APIRouter()


@router.post("/", response_model=SummaryResponseSchema, status_code=201)
async def create_summary(
    payload: SummaryPayloadSchema,
) -> SummaryResponseSchema:
    """Creates summary"""

    summary = await crud.post(payload)

    response_object = {
        "id": summary.id,
        "url": payload.url,
    }
    return response_object


@router.get("/{id}/", response_model=SummarySchema)
async def read_summary(id: int) -> SummarySchema:
    """Reads summary"""

    summary = await crud.get(id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summmary not found")

    return summary


@router.get("/", response_model=List[SummarySchema])
async def read_all_summaries() -> List[SummarySchema]:
    """Reads all summaries"""

    summaries = await crud.get_all()
    return summaries
