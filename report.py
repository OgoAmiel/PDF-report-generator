"""Aggregate local order data for the PDF report."""

import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).with_name("report.db")


def getReportData() -> dict[str, object]:
    """Return the order aggregates used by the report."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.row_factory = sqlite3.Row

        total_orders = connection.execute(
            "SELECT COUNT(*) AS total_orders FROM orders"
        ).fetchone()["total_orders"]
        total_revenue = connection.execute(
            "SELECT COALESCE(SUM(amount), 0) AS total_revenue FROM orders"
        ).fetchone()["total_revenue"]
        top_products = connection.execute(
            """
            SELECT product, SUM(amount) AS revenue
            FROM orders
            GROUP BY product
            ORDER BY revenue DESC
            LIMIT 5
            """
        ).fetchall()
        orders_per_day = connection.execute(
            """
            SELECT created_at, COUNT(*) AS order_count
            FROM orders
            WHERE created_at >= date('now', '-6 days')
            GROUP BY created_at
            ORDER BY created_at
            """
        ).fetchall()
        all_orders = connection.execute(
            """
            SELECT id, customer, product, amount, created_at
            FROM orders
            ORDER BY created_at DESC, id DESC
            """
        ).fetchall()

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "top_products_by_revenue": [dict(row) for row in top_products],
        "orders_per_day_last_7_days": [dict(row) for row in orders_per_day],
        "all_orders": [dict(row) for row in all_orders],
    }