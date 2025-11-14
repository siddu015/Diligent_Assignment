You are an expert data engineer. Ingest the synthetic ecommerce dataset into a fully constrained SQLite database.

IMPORTANT:

- Use Cursor Agent actions only.
- Do not print any CSV rows or table contents in chat.
- Create all required files inside the workspace.
- Save the ingestion script as: scripts/ingest_ecommerce_sqlite.py
- Read all CSV files from ecommerce_dataset/
- The script must run end-to-end without manual edits.
- Use only Python standard libraries: csv, sqlite3, decimal, pathlib, datetime.
- Do not modify or regenerate the dataset files.

GOAL:
Create a SQLite database at:
database/ecommerce.db

The Python script must perform the following steps exactly:

1. Directory setup

   - Create database/ if missing
   - Create scripts/ if missing

2. Initialize SQLite with a clean schema

   - Connect to database/ecommerce.db
   - Enable foreign key enforcement: PRAGMA foreign_keys = ON
   - After enabling, verify PRAGMA foreign_keys returns 1; if not, raise an error
   - Drop existing tables if present
   - Recreate tables exactly as specified:

     customers(
     customer_id TEXT PRIMARY KEY,
     full_name TEXT NOT NULL,
     email TEXT UNIQUE NOT NULL,
     phone TEXT UNIQUE NOT NULL,
     address TEXT NOT NULL,
     city TEXT NOT NULL,
     state TEXT NOT NULL,
     country TEXT NOT NULL,
     created_at TEXT NOT NULL
     )

     products(
     product_id TEXT PRIMARY KEY,
     name TEXT NOT NULL,
     category TEXT NOT NULL,
     sub_category TEXT NOT NULL,
     price REAL NOT NULL,
     stock_quantity INTEGER NOT NULL,
     added_at TEXT NOT NULL
     )

     orders(
     order_id TEXT PRIMARY KEY,
     customer_id TEXT NOT NULL,
     order_date TEXT NOT NULL,
     total_amount REAL NOT NULL,
     status TEXT NOT NULL,
     city TEXT NOT NULL,
     state TEXT NOT NULL,
     country TEXT NOT NULL,
     FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
     )

     order_items(
     order_item_id TEXT PRIMARY KEY,
     order_id TEXT NOT NULL,
     product_id TEXT NOT NULL,
     quantity INTEGER NOT NULL,
     item_price REAL NOT NULL,
     subtotal REAL NOT NULL,
     FOREIGN KEY(order_id) REFERENCES orders(order_id),
     FOREIGN KEY(product_id) REFERENCES products(product_id)
     )

     payments(
     payment_id TEXT PRIMARY KEY,
     order_id TEXT NOT NULL,
     payment_method TEXT NOT NULL,
     amount REAL NOT NULL,
     payment_status TEXT NOT NULL,
     transaction_timestamp TEXT NOT NULL,
     FOREIGN KEY(order_id) REFERENCES orders(order_id)
     )

3. Deterministic ingestion rules

   - Load each CSV using csv.DictReader
   - Insert rows in this exact order:
     1. customers
     2. products
     3. orders
     4. order_items
     5. payments
   - Convert numeric values to Decimal before inserting to avoid float drift
   - Commit after each table batch
   - After inserting all tables, run programmatic verification:
     - Confirm each table row count equals the CSV row count
     - Confirm for every order: orders.total_amount == sum(order_items.subtotal)
     - Confirm payments reflect the expected success rate of 92 percent (raise or report if off)
     - If any verification fails, raise an exception and do not print row data

4. Completion output
   After successful ingestion and verification, the script must print ONLY:
   Created SQLite database at database/ecommerce.db

OUTPUT RESTRICTIONS:

- Do NOT print table rows or CSV contents.
- After creating the script, respond only with the filename(s) created.
