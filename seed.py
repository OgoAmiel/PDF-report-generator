"""Create and populate the local development orders database."""

import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path


DATABASE_PATH = Path(__file__).with_name("report.db")
PRODUCTS = [
    "Wireless Mouse",
    "Mechanical Keyboard",
    "USB-C Hub",
    "Laptop Stand",
    "Webcam",
    "Noise-Canceling Headphones",
]


def random_order_date() -> str:
    days_ago = random.randint(0, 29)
    return (date.today() - timedelta(days=days_ago)).isoformat()


def seed_orders(order_count: int = 200) -> None:
    orders = [
        (
            f"Customer {index:03d}",
            random.choice(PRODUCTS),
            random.randint(5, 200),
            random_order_date(),
        )
        for index in range(1, order_count + 1)
    ]

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                customer TEXT NOT NULL,
                product TEXT NOT NULL,
                amount INTEGER NOT NULL CHECK (amount BETWEEN 5 AND 200),
                created_at DATE NOT NULL
            )
            """
        )
        connection.execute("DELETE FROM orders")
        connection.executemany(
            """
            INSERT INTO orders (customer, product, amount, created_at)
            VALUES (?, ?, ?, ?)
            """,
            orders,
        )

    print(f"Seeded {order_count} orders in {DATABASE_PATH.name}")


if __name__ == "__main__":
    seed_orders()