"""Pydantic schemas for the push/pull sync payload."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ExpenseSchema(BaseModel):
    """A single expense record as exchanged during sync."""

    id: int
    title: str
    amount: float
    date: datetime
    description: Optional[str] = None


class ExpenseCategorySchema(BaseModel):
    """
    An expense category together with all its expense entries.

    ``sum`` is the aggregated total maintained by the mobile app and is
    round-tripped unchanged so the mobile can restore it without recalculating.
    """

    id: int
    name: str
    sum: float = 0.0
    expenses: List[ExpenseSchema] = []


class SavingSchema(BaseModel):
    """A single saving deposit record as exchanged during sync."""

    id: int
    title: str
    amount: float
    date: datetime


class SavingCategorySchema(BaseModel):
    """
    A saving goal category together with all its deposit entries.

    ``sum`` and ``is_goal_achieved`` are maintained by the mobile app and
    stored as-is so full category state can be restored after a pull.
    """

    id: int
    name: str
    goal: float
    sum: float = 0.0
    is_goal_achieved: bool = False
    savings: List[SavingSchema] = []


class SyncPayload(BaseModel):
    """
    Top-level envelope for both push and pull sync operations.

    Contains the complete financial dataset for one user: all expense
    categories (with their expenses) and all saving categories (with their
    deposits).
    """

    expense_categories: List[ExpenseCategorySchema] = []
    saving_categories: List[SavingCategorySchema] = []
