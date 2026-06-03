"""Pydantic schemas for the push/pull sync payload."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class ExpenseSchema(BaseModel):
    """A single expense record as exchanged during sync."""

    id: UUID
    title: str
    amount: float
    date: datetime
    description: Optional[str] = None


class ExpenseCategorySchema(BaseModel):
    """An expense category together with all its expense entries."""

    id: UUID
    name: str
    expenses: List[ExpenseSchema] = []


class SavingSchema(BaseModel):
    """A single saving deposit record as exchanged during sync."""

    id: UUID
    title: str
    amount: float
    date: datetime


class SavingCategorySchema(BaseModel):
    """A saving goal category together with all its deposit entries."""

    id: UUID
    name: str
    goal: float
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
