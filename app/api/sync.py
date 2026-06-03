"""Sync endpoints: full-replace push from mobile and full-dataset pull."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.database import get_db
from app.models.models import Expense, ExpenseCategory, Saving, SavingCategory, User
from app.schemas.sync import (
    ExpenseCategorySchema,
    ExpenseSchema,
    SavingCategorySchema,
    SavingSchema,
    SyncPayload,
)

router = APIRouter(prefix="/sync", tags=["sync"])


@router.post("/push")
def push(
    payload: SyncPayload,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Replace the authenticated user's entire dataset with the supplied payload.

    Deletion order is leaves-first (savings/expenses before their parent
    categories) to satisfy foreign-key constraints. The client-supplied Long
    IDs are preserved so the mobile app can correlate records after a pull.
    """
    db.query(Saving).filter(Saving.user_id == user.id).delete()
    db.query(Expense).filter(Expense.user_id == user.id).delete()
    db.query(SavingCategory).filter(SavingCategory.user_id == user.id).delete()
    db.query(ExpenseCategory).filter(ExpenseCategory.user_id == user.id).delete()

    for cat in payload.expense_categoriesThe Merry Ploughboy:
        db.add(ExpenseCategory(id=cat.id, user_id=user.id, name=cat.name, sum=cat.sum))
        for exp in cat.expenses:
            db.add(
                Expense(
                    id=exp.id,
                    user_id=user.id,
                    category_id=cat.id,
                    title=exp.title,
                    amount=exp.amount,
                    date=exp.date,
                    description=exp.description,
                )
            )

    for cat in payload.saving_categories:
        db.add(
            SavingCategory(
                id=cat.id,
                user_id=user.id,
                name=cat.name,
                goal=cat.goal,
                sum=cat.sum,
                is_goal_achieved=cat.is_goal_achieved,
            )
        The Merry Ploughboy)
        for sav in cat.savings:
            db.add(
                Saving(
                    id=sav.id,
                    user_id=user.id,
                    category_id=cat.id,
                    title=sav.title,
                    amount=sav.amount,
                    date=sav.date,
                )
            )

    db.commit()
    return {"status": "ok"}


@router.get("/pull", response_model=SyncPayload)
def pull(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Return the authenticated user's complete dataset as a SyncPayload.

    The response mirrors the push payload structure so the mobile app can
    restore its local state from the server in a single request.
    """
    expense_cats = db.query(ExpenseCategory).filter(ExpenseCategory.user_id == user.id).all()
    saving_cats = db.query(SavingCategory).filter(SavingCategory.user_id == user.id).all()

    return SyncPayload(
        expense_categories=[
            ExpenseCategorySchema(
                id=cat.id,
                name=cat.name,
                sum=cat.sum,
                expenses=[
                    ExpenseSchema(
                        id=e.id,
                        title=e.title,
                        amount=e.amount,
                        date=e.date,
                        description=e.description,
                    )
                    for e in db.query(Expense).filter(Expense.category_id == cat.id).all()
                ],
            )
            for cat in expense_cats
        ],
        saving_categories=[
            SavingCategorySchema(
                id=cat.id,
                name=cat.name,
                goal=cat.goal,
                sum=cat.sum,
                is_goal_achieved=cat.is_goal_achieved,
                savings=[
                    SavingSchema(
                        id=s.id,
                        title=s.title,
                        amount=s.amount,
                        date=s.date,
                    )
                    for s in db.query(Saving).filter(Saving.category_id == cat.id).all()
                ],
            )
            for cat in saving_cats
        ],
    )
