"""
Write MCP tools: these are the only tools that change data. Kept apart
from read_tools.py so it's obvious at a glance which tools are safe to
call freely and which ones mutate the database.
"""


from datetime import date

from fastmcp import FastMCP

from expense_manager_mcp.models import  ExpenseIn
from expense_manager_mcp.services import ExpenseService


def register(mcp: FastMCP, service: ExpenseService) -> None:
    @mcp.tool
    def add_expense(
        amount: float,
        category: str,
        expense_date: date,
        description: str,
    ) -> dict:
        """Record a new expense.

        Use this whenever the user reports spending money, e.g. "I spent
        500 on groceries today" or "add a 1200 rupee expense for the
        electricity bill on Aug 5". If the user doesn't give a date,
        assume today. ALL fields are required, including description -
        if the user didn't give one, ask what the expense was for rather
        than guessing.
        """
        created = service.add_expense(
            ExpenseIn(
                amount=amount,
                category=category,
                description=description,
                expense_date=expense_date,
            )
        )
        return created.model_dump(mode="json")


    @mcp.tool
    def delete_expense(expense_id: int) -> dict:
        """Permanently delete an expense by id.

        Use this for requests like "delete that expense" or "remove
        entry 12" - after you've already found its id via list_expenses
        or get_expense. This cannot be undone. Returns
        {"deleted": true} on success, {"deleted": false} if no expense
        with that id existed.
        """
        deleted = service.delete_expense(expense_id)
        return {"deleted": deleted, "expense_id": expense_id}

