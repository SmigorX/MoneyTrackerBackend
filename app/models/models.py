import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ExpenseCategory(Base):
    __tablename__ = 'expense_category'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    name = Column(String(100), nullable=False)

class Expense(Base):
    __tablename__ = 'expense'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey('expense_category.id'), nullable=False)
    
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

class SavingCategory(Base):
    __tablename__ = 'saving_category'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    name = Column(String(100), nullable=False)
    goal = Column(Float, nullable=False)
    is_goal_achieved = Column(Boolean, default=False)

class Saving(Base):
    __tablename__ = 'saving'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey('saving_category.id'), nullable=False)
    
    title = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)