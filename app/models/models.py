"""SQLAlchemy ORM models for the MoneyTracker database."""

import uuid
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    """
    Registered user account.

    Stores the credentials needed for authentication. All financial data is
    linked to a user via foreign keys so each user's records stay isolated.
    """

    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ExpenseCategory(Base):
    """
    A user-defined category that groups related expenses (e.g. "Food", "Rent").

    ``sum`` mirrors the aggregated total maintained by the mobile app and is
    stored as-is during push so it can be restored on pull without recalculating.
    """

    __tablename__ = 'expense_category'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    name = Column(String(100), nullable=False)
    sum = Column(Float, nullable=False, default=0.0)


class Expense(Base):
    """
    A single expense entry belonging to an ExpenseCategory.

    Amounts are negative (as stored by the mobile app). The optional
    ``description`` field may carry additional notes from the user.
    """

    __tablename__ = 'expense'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    category_id = Column(BigInteger, ForeignKey('expense_category.id'), nullable=False)

    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)


class SavingCategory(Base):
    """
    A user-defined savings goal category (e.g. "Vacation", "Emergency fund").

    ``goal`` is the target amount, ``sum`` is the current total deposited.
    ``is_goal_achieved`` is set by the mobile app once the goal is reached.
    Both aggregates are stored as-is to allow full state restoration on pull.
    """

    __tablename__ = 'saving_category'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    name = Column(String(100), nullable=False)
    goal = Column(Float, nullable=False)
    sum = Column(Float, nullable=False, default=0.0)
    is_goal_achieved = Column(Boolean, default=False)


class Saving(Base):
    """A single saving deposit entry belonging to a SavingCategory."""

    __tablename__ = 'saving'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    category_id = Column(BigInteger, ForeignKey('saving_category.id'), nullable=False)

    title = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
