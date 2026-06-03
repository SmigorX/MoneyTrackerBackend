"""SQLAlchemy ORM models for the MoneyTracker database."""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

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
    """

    __tablename__ = 'expense_category'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    name = Column(String(100), nullable=False)


class Expense(Base):
    """
    A single expense entry belonging to an ExpenseCategory.

    The ``description`` field is optional and may be used by the mobile app
    for additional notes.
    """

    __tablename__ = 'expense'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey('expense_category.id'), nullable=False)

    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)


class SavingCategory(Base):
    """
    A user-defined savings goal category (e.g. "Vacation", "Emergency fund").

    ``goal`` is the target amount. ``is_goal_achieved`` is set by the mobile
    app once the accumulated savings reach that target.
    """

    __tablename__ = 'saving_category'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    name = Column(String(100), nullable=False)
    goal = Column(Float, nullable=False)
    is_goal_achieved = Column(Boolean, default=False)


class Saving(Base):
    """A single saving entry (deposit) belonging to a SavingCategory."""

    __tablename__ = 'saving'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey('saving_category.id'), nullable=False)

    title = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
