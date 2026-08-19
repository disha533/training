from datetime import date

from pydantic import BaseModel, Field


class ExpenseIn(BaseModel):
    """Everything needed to record  an expense.
    """

    amount: float = Field(..., gt=0, description="Must be a positive number")
    category: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    expense_date: date


class ExpenseOut(BaseModel):
    """What we return for a single expense."""

    id: int
    amount: float
    category: str
    description: str
    expense_date: date




class MonthlySummaryEntry(BaseModel):
    """One row of a monthly spending-by-category summary."""

    category: str
    total: float