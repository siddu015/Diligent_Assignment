#!/usr/bin/env python3
"""Deterministic ingestion of ecommerce dataset into SQLite."""

import csv
import sqlite3
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 28


def decimal_str(value):
    text = str(value).strip()
    return format(Decimal(text), "f")


def decimal_from_db(value):
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def ensure_directories(root_path):
    database_dir = root_path / "database"
    scripts_dir = root_path / "scripts"
    database_dir.mkdir(exist_ok=True)
    scripts_dir.mkdir(exist_ok=True)
    return database_dir


def enable_foreign_keys(connection):
    connection.execute("PRAGMA foreign_keys = ON;")
    result = connection.execute("PRAGMA foreign_keys;").fetchone()
    if not result or result[0] != 1:
        raise RuntimeError("Failed to enable SQLite foreign keys.")


def reset_schema(connection):
    drop_sql = """
    DROP TABLE IF EXISTS order_items;
    DROP TABLE IF EXISTS payments;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS products;
    DROP TABLE IF EXISTS customers;
    """
    connection.executescript(drop_sql)

    create_sql = """
    CREATE TABLE customers(
        customer_id TEXT PRIMARY KEY,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT UNIQUE NOT NULL,
        address TEXT NOT NULL,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        country TEXT NOT NULL,
        created_at TEXT NOT NULL
    );

    CREATE TABLE products(
        product_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        sub_category TEXT NOT NULL,
        price REAL NOT NULL,
        stock_quantity INTEGER NOT NULL,
        added_at TEXT NOT NULL
    );

    CREATE TABLE orders(
        order_id TEXT PRIMARY KEY,
        customer_id TEXT NOT NULL,
        order_date TEXT NOT NULL,
        total_amount REAL NOT NULL,
        status TEXT NOT NULL,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        country TEXT NOT NULL,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    );

    CREATE TABLE order_items(
        order_item_id TEXT PRIMARY KEY,
        order_id TEXT NOT NULL,
        product_id TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        item_price REAL NOT NULL,
        subtotal REAL NOT NULL,
        FOREIGN KEY(order_id) REFERENCES orders(order_id),
        FOREIGN KEY(product_id) REFERENCES products(product_id)
    );

    CREATE TABLE payments(
        payment_id TEXT PRIMARY KEY,
        order_id TEXT NOT NULL,
        payment_method TEXT NOT NULL,
        amount REAL NOT NULL,
        payment_status TEXT NOT NULL,
        transaction_timestamp TEXT NOT NULL,
        FOREIGN KEY(order_id) REFERENCES orders(order_id)
    );
    """
    connection.executescript(create_sql)
    connection.commit()


def ingest_customers(connection, csv_path):
    rows = []
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                (
                    row["customer_id"],
                    row["full_name"],
                    row["email"],
                    row["phone"],
                    row["address"],
                    row["city"],
                    row["state"],
                    row["country"],
                    row["created_at"],
                )
            )
    sql = """
    INSERT INTO customers(
        customer_id, full_name, email, phone, address, city, state, country, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    connection.executemany(sql, rows)
    connection.commit()
    return len(rows)


def ingest_products(connection, csv_path):
    rows = []
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                (
                    row["product_id"],
                    row["name"],
                    row["category"],
                    row["sub_category"],
                    decimal_str(row["price"]),
                    int(row["stock_quantity"]),
                    row["added_at"],
                )
            )
    sql = """
    INSERT INTO products(
        product_id, name, category, sub_category, price, stock_quantity, added_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    connection.executemany(sql, rows)
    connection.commit()
    return len(rows)


def ingest_orders(connection, csv_path):
    rows = []
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                (
                    row["order_id"],
                    row["customer_id"],
                    row["order_date"],
                    decimal_str(row["total_amount"]),
                    row["status"],
                    row["city"],
                    row["state"],
                    row["country"],
                )
            )
    sql = """
    INSERT INTO orders(
        order_id, customer_id, order_date, total_amount, status, city, state, country
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    connection.executemany(sql, rows)
    connection.commit()
    return len(rows)


def ingest_order_items(connection, csv_path):
    rows = []
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                (
                    row["order_item_id"],
                    row["order_id"],
                    row["product_id"],
                    int(row["quantity"]),
                    decimal_str(row["item_price"]),
                    decimal_str(row["subtotal"]),
                )
            )
    sql = """
    INSERT INTO order_items(
        order_item_id, order_id, product_id, quantity, item_price, subtotal
    ) VALUES (?, ?, ?, ?, ?, ?)
    """
    connection.executemany(sql, rows)
    connection.commit()
    return len(rows)


def ingest_payments(connection, csv_path):
    rows = []
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                (
                    row["payment_id"],
                    row["order_id"],
                    row["payment_method"],
                    decimal_str(row["amount"]),
                    row["payment_status"],
                    row["transaction_timestamp"],
                )
            )
    sql = """
    INSERT INTO payments(
        payment_id, order_id, payment_method, amount, payment_status, transaction_timestamp
    ) VALUES (?, ?, ?, ?, ?, ?)
    """
    connection.executemany(sql, rows)
    connection.commit()
    return len(rows)


def ingest_all_tables(connection, dataset_dir):
    counts = {}
    counts["customers"] = ingest_customers(connection, dataset_dir / "customers.csv")
    counts["products"] = ingest_products(connection, dataset_dir / "products.csv")
    counts["orders"] = ingest_orders(connection, dataset_dir / "orders.csv")
    counts["order_items"] = ingest_order_items(connection, dataset_dir / "order_items.csv")
    counts["payments"] = ingest_payments(connection, dataset_dir / "payments.csv")
    return counts


def verify_row_counts(connection, expected_counts):
    for table_name, expected in expected_counts.items():
        query = f"SELECT COUNT(*) FROM {table_name}"
        actual = connection.execute(query).fetchone()[0]
        if actual != expected:
            raise ValueError(
                f"Row count mismatch for {table_name}: expected {expected}, found {actual}"
            )


def verify_order_amounts(connection):
    order_totals = {}
    cursor = connection.execute("SELECT order_id, total_amount FROM orders")
    for order_id, total_amount in cursor:
        order_totals[order_id] = decimal_from_db(total_amount)

    computed_totals = {}
    cursor = connection.execute("SELECT order_id, subtotal FROM order_items")
    for order_id, subtotal in cursor:
        subtotal_decimal = decimal_from_db(subtotal)
        current = computed_totals.get(order_id)
        if current is None:
            computed_totals[order_id] = subtotal_decimal
        else:
            computed_totals[order_id] = current + subtotal_decimal

    missing = [order_id for order_id in order_totals if order_id not in computed_totals]
    if missing:
        raise ValueError(
            "Orders missing order_items: " + ", ".join(missing[:5])
        )

    mismatches = []
    for order_id, total_amount in order_totals.items():
        if total_amount != computed_totals.get(order_id, Decimal("0")):
            mismatches.append(order_id)
            if len(mismatches) == 5:
                break

    if mismatches:
        raise ValueError(
            "Order total mismatch detected for IDs: " + ", ".join(mismatches)
        )


def verify_payment_success_rate(connection):
    cursor = connection.execute(
        "SELECT payment_status, COUNT(*) FROM payments GROUP BY payment_status"
    )
    total = 0
    success = 0
    for status, count in cursor:
        total += count
        if str(status).strip().lower() == "success":
            success += count

    if total == 0:
        raise ValueError("Payments table is empty; cannot verify success rate.")

    ratio = Decimal(success) / Decimal(total)
    expected_ratio = Decimal("0.92")
    tolerance = Decimal("0.01")
    difference = ratio - expected_ratio
    if difference.copy_abs() > tolerance:
        raise ValueError(
            f"Payment success ratio {format(ratio, '.5f')} outside tolerance for expected 0.92"
        )


def run_verifications(connection, counts):
    verify_row_counts(connection, counts)
    verify_order_amounts(connection)
    verify_payment_success_rate(connection)


def main():
    root_dir = Path(__file__).resolve().parent.parent
    dataset_dir = root_dir / "ecommerce_dataset"
    if not dataset_dir.exists():
        raise FileNotFoundError(f"Dataset directory not found: {dataset_dir}")

    database_dir = ensure_directories(root_dir)
    db_path = database_dir / "ecommerce.db"

    connection = sqlite3.connect(db_path)
    try:
        enable_foreign_keys(connection)
        reset_schema(connection)
        counts = ingest_all_tables(connection, dataset_dir)
        run_verifications(connection, counts)
    finally:
        connection.close()

    print("Created SQLite database at database/ecommerce.db")


if __name__ == "__main__":
    main()

