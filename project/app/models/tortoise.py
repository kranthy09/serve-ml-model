"""
Model classes for App.
"""

from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class TextSummary(models.Model):
    """Text summary model"""

    url = fields.TextField()
    summary = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        """String Representation"""

        return self.url


SummarySchema = pydantic_model_creator(TextSummary)
