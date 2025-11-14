# Observations After SQLite Ingestion and Validation

Model used: GPT-5.1 Codex High

This document summarizes the ingestion and validation process for the synthetic ecommerce dataset into a SQLite database. It includes the prompts used for ingestion and validation, the results of the validation, an interpretation of those results, and suggested next steps.

## Ingestion Prompt Used

The following prompt was used to generate and execute the ingestion script for the ecommerce dataset:

```
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
```

After executing the ingestion prompt using Cursor Agent actions, the script `scripts/ingest_ecommerce_sqlite.py` was generated and executed successfully. The ingestion workflow ran end-to-end without any manual edits, and the SQLite database `database/ecommerce.db` was created as expected.

## Validation Prompt Used

The following prompt was used to validate the SQLite database created from the ecommerce dataset:

```
You are an expert data engineer. Validate the SQLite @database created from the @ecommerce_dataset .

IMPORTANT:

- Use Cursor Agent actions only.
- Do NOT print full table contents.
- Never modify the database.
- You may run SELECT queries for validation logic.
- Report only mismatches, if any. If everything is valid, say so clearly.

VALIDATE THE FOLLOWING:

1. Schema correctness

   - Confirm all tables exist: customers, products, orders, order_items, payments
   - Confirm each table’s columns match the required schema
   - Confirm foreign key constraints are active (PRAGMA foreign_keys = ON)

2. Row count verification

   - Compare row counts in each table against:
     customers: 1500
     products: 300
     orders: 1500
     order_items: between 4000 and 6000
     payments: 1500

3. Referential integrity

   - Check that every FK resolves:
     - orders.customer_id exists in customers
     - order_items.order_id exists in orders
     - order_items.product_id exists in products
     - payments.order_id exists in orders
   - Check no order has more than 1 payment row
   - Check no orphan rows exist anywhere

4. Numeric precision & totals

   - Verify: subtotal == quantity \* item_price
   - Verify: orders.total_amount == SUM(order_items.subtotal)
   - Verify: payments.amount == orders.total_amount

5. Payment success ratio

   - Confirm success rate is exactly 92 percent (± tolerance 0.01)

6. Formatting checks
   - No empty strings in key fields
   - Datetimes parse cleanly

OUTPUT:
If all checks pass:
“SQLite database validation passed. No mismatches detected.”

If mismatches exist:
List each mismatch category with a short description.

```

## Validation Results

- **Foreign key enforcement disabled** – Running `PRAGMA foreign_keys;` against `/Users/siddu/Developer/Diligent_Assignment/database/ecommerce.db` returns `0`, so FK constraints aren’t being enforced even though they’re defined. Connect with `PRAGMA foreign_keys = ON;` (or configure the client/ORM to enable it automatically) before issuing DML so the constraints actually protect the data.

Everything else in your validation brief checked out: schemas match `scripts/ingest_ecommerce_sqlite.py`, row counts are customers 1500 / products 300 / orders 1500 / order_items 5309 / payments 1500, all FK references resolve with no orphans or duplicate payments, monetary math holds to ±0.0001, payment success rate is 0.928 (within the 0.92±0.01 window), and key fields plus datetime columns have no empty or invalid values.

Restating your request: you asked for a full integrity audit of the SQLite build from the ecommerce CSVs; the only issue I found is that FK enforcement is off for new connections.

Sources: sqlite3 queries against `/Users/siddu/Developer/Diligent_Assignment/database/ecommerce.db`; `scripts/ingest_ecommerce_sqlite.py`.

## Prompt Refinement

Based on the validation results, one issue surfaced: **foreign key enforcement was disabled for new SQLite connections**.  
The ingestion script correctly enabled it during ingestion, but validation showed that external connections still saw `PRAGMA foreign_keys = 0`.

To fix this, the ingestion prompt was updated with one specific line:
**“- After enabling, verify PRAGMA foreign_keys returns 1; if not, raise an error.”**

This ensures:

- FK enforcement is verified immediately after connection is opened
- Any ingestion script failure is surfaced early
- The database is always created with constraints confirmed as active

Only this single requirement was added in the refined prompt.

## Updated Prompt

```
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
```

## Validation Prompt Used

The following prompt was used to validate the SQLite database created from the ecommerce dataset:

```
You are an expert data engineer. Validate the SQLite @database created from the @ecommerce_dataset .

IMPORTANT:

- Use Cursor Agent actions only.
- Do NOT print full table contents.
- Never modify the database.
- You may run SELECT queries for validation logic.
- Report only mismatches, if any. If everything is valid, say so clearly.

VALIDATE THE FOLLOWING:

1. Schema correctness

   - Confirm all tables exist: customers, products, orders, order_items, payments
   - Confirm each table’s columns match the required schema
   - Confirm foreign key constraints are active (PRAGMA foreign_keys = ON)

2. Row count verification

   - Compare row counts in each table against:
     customers: 1500
     products: 300
     orders: 1500
     order_items: between 4000 and 6000
     payments: 1500

3. Referential integrity

   - Check that every FK resolves:
     - orders.customer_id exists in customers
     - order_items.order_id exists in orders
     - order_items.product_id exists in products
     - payments.order_id exists in orders
   - Check no order has more than 1 payment row
   - Check no orphan rows exist anywhere

4. Numeric precision & totals

   - Verify: subtotal == quantity \* item_price
   - Verify: orders.total_amount == SUM(order_items.subtotal)
   - Verify: payments.amount == orders.total_amount

5. Payment success ratio

   - Confirm success rate is exactly 92 percent (± tolerance 0.01)

6. Formatting checks
   - No empty strings in key fields
   - Datetimes parse cleanly

OUTPUT:
If all checks pass:
“SQLite database validation passed. No mismatches detected.”

If mismatches exist:
List each mismatch category with a short description.

```

## Validation Results

Mismatch detected: payment success ratio is 92.8%, outside the required 92% ±0.01 (1392 successes, 108 failures; should be 1380 successes for target tolerance). You asked for a full validation of the ecommerce SQLite build; here’s what I checked:

- `customers`, `products`, `orders`, `order_items`, `payments` exist with the exact column specs from the ingestion prompt; foreign keys are defined and `PRAGMA foreign_keys = ON` returns 1 once enabled for the session.
- Row counts match expectations: customers 1500, products 300, orders 1500, payments 1500, and order_items 5309 (within 4k–6k range).
- Referential integrity holds: FK checks return zero orphans, every order has exactly one payment, and `PRAGMA foreign_key_check` is silent.
- Numeric integrity passes: each order_item subtotal equals `quantity * item_price`, each order total equals the sum of its items, and each payment amount matches its order total (all within 1e-5 tolerance).
- Formatting: no empty strings in key text columns, and all timestamp fields parse via `strftime('%s', …)`.

Only outstanding issue is the success ratio; adjust the payment ingestion logic or source data so only 8% (±0.01) of the 1500 payments are failures (target 1380 successes / 120 failures) to satisfy the requirement.

No other mismatches found.

## final verdict

I can confirm there is no issue with the SQLite ingestion process. The only discrepancy came from the dataset’s payment‑success distribution, not the ingestion prompt or script. Based on all validation steps, the ingestion prompt is correct and complete.
