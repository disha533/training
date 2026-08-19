from fastmcp import FastMCP

from expense_manager_mcp.services import ExpenseService


def register(mcp: FastMCP, service: ExpenseService) -> None:
    @mcp.tool
    def get_expense(expense_id: int) -> dict:
        """Fetch a single expense by its id.

        Use this when you already know the specific expense id - usually
        because a previous list_expenses call returned it.
        """
        result = service.get_expense(expense_id)
        return result.model_dump(mode="json") if result else {}


    @mcp.tool
    def get_monthly_summary(month: int, year: int) -> dict:
        """Get total spending per category for a given month and year.

        Use this for requests like "how much did I spend this month" or
        "break down my July spending by category".
        """
        results = service.get_monthly_summary(month, year)
        return {"summary": [r.model_dump(mode="json") for r in results]}


