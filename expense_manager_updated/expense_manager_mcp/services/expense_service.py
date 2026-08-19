from typing import Optional

from sqlalchemy import extract, func, select
from sqlalchemy.orm import Session, sessionmaker

from expense_manager_mcp.models import (
    Expense,
    ExpenseIn,
    ExpenseOut,
    MonthlySummaryEntry,
)


class ExpenseService:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    # --------------------------------------------------------------- reads
    def get_expense(self, expense_id: int) -> Optional[ExpenseOut]:
        with self._session_factory() as session:
            expense = session.get(Expense, expense_id)
            return (
                ExpenseOut.model_validate(expense, from_attributes=True)
                if expense
                else None
            )

    def get_monthly_summary(self, month: int, year: int) -> list[MonthlySummaryEntry]:
        with self._session_factory() as session:
            stmt = (
                select(
                    Expense.category,
                    func.sum(Expense.amount).label("total"),
                )
                .where(
                    extract("MONTH", Expense.expense_date) == month,
                    extract("YEAR", Expense.expense_date) == year,
                )
                .group_by(Expense.category)
                .order_by(func.sum(Expense.amount).desc())
            )
            rows = session.execute(stmt).all()
            return [
                MonthlySummaryEntry(category=row.category, total=row.total)
                for row in rows
            ]

    # -------------------------------------------------------------- writes
    def add_expense(self, payload: ExpenseIn) -> ExpenseOut:
        with self._session_factory() as session:
            expense = Expense(**payload.model_dump())
            session.add(expense)
            session.commit()
            session.refresh(expense)
            return ExpenseOut.model_validate(expense, from_attributes=True)

    def delete_expense(self, expense_id: int) -> bool:
        with self._session_factory() as session:
            expense = session.get(Expense, expense_id)
            if expense is None:
                return False
            session.delete(expense)
            session.commit()
            return True
