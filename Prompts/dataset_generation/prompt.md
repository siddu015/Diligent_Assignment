You are an expert data engineer. Generate a complete synthetic ecommerce dataset with realistic relational integrity, business logic, and time distributions. Use Cursor Agent actions to create actual files in the workspace.

IMPORTANT:

- Use Cursor Agent actions only.
- Do NOT print or display any CSV content in chat.
- After generation, list only the filenames created.
- Create a folder named ecommerce_dataset at the project root and store all CSVs inside it.
- Create a folder named scripts and save the Python generator script as scripts/generate_ecommerce_dataset.py.
- Do not delete or modify any generated scripts.

GOAL:
Generate exactly 5 CSV files in ecommerce_dataset/.
All files must:

- Be valid UTF-8
- Use comma delimiters
- Use quoted strings only when necessary
- Contain no trailing commas
- Preserve consistent schemas
- Avoid header duplication
- Maintain clean formatting with no extra whitespace

DETERMINISM & NUMERIC PRECISION (Critical):

- Apply a fixed random seed of 42 at the start of every data generation step.
- All arithmetic must use precise, unrounded values.
- Never call round() or perform format-based rounding.
- subtotal = quantity \* item_price (exact)
- total_amount = SUM(order_items.subtotal) (exact)

DATASET SIZE:

- customers.csv: 1500 rows
- products.csv: 300 rows
- orders.csv: 1500 rows
- order_items.csv: 4000–6000 rows (1–5 items per order)
- payments.csv: 1500 rows

FILES & SCHEMAS:

1. customers.csv

   - customer_id (UUID, unique)
   - full_name (realistic Indian + global names)
   - email (unique; gmail, outlook, yahoo)
   - phone (valid Indian or international +country-code)
   - address
   - city
   - state
   - country
   - created_at (past 3 years, realistic distribution)

2. products.csv

   - product_id (UUID)
   - name
   - category (distribution: electronics 20%, fashion 25%, home 15%, beauty 15%, sports 10%, grocery 15%)
   - sub_category (exact mapping):
     electronics → mobiles, laptops, headphones, tablets
     fashion → menswear, womenswear, footwear, accessories
     home → furniture, decor, kitchenware
     beauty → skincare, haircare, cosmetics
     sports → fitness, outdoor, athletic wear
     grocery → snacks, beverages, staples
   - price (positive float, realistic, precise)
   - stock_quantity (5–500)
   - added_at (within past 3 years)

3. orders.csv

   - order_id (UUID, unique)
   - customer_id (FK → customers.customer_id)
   - order_date with seasonal spikes:
     Republic Day (Jan 20–25)
     Summer Sale (May)
     Independence Day (Aug 10–15)
     Dasara (late Oct)
     Diwali (early Nov)
     Black Friday (late Nov)
     Christmas (Dec 20–25)
   - total_amount (exact SUM(order_items.subtotal))
   - status (created, shipped, delivered, cancelled, returned)
   - city, state, country (copied from customer)

4. order_items.csv

   - order_item_id (UUID)
   - order_id (FK)
   - product_id (FK)
   - quantity (1–3)
   - item_price (must match products.price exactly)
   - subtotal (quantity \* item_price, no rounding)
   - Each order: 1–5 items

5. payments.csv
   - payment_id (UUID)
   - order_id (FK)
   - payment_method (Gift Card, UPI, Credit Card, Debit Card, COD, Netbanking)
   - amount (must equal orders.total_amount exactly)
   - payment_status (92% success, 8% failed)
   - transaction_timestamp = order_date + 5–180 seconds

STRICT RELATIONAL RULES:

- No orphan rows.
- customers → orders: one‑to‑many
- orders → order_items: one‑to‑many
- orders → payments: one‑to‑one
- products.price = order_items.item_price exactly
- Unique emails and phone numbers only
- No unrealistic names, dates, or placeholder values

QUALITY RULES:

- Use realistic, diverse product names and prices.
- Ensure category → subcategory consistency.
- Maintain clean, well‑formed CSV structure.

OUTPUT:
After generating all files, respond ONLY with a confirmation message listing filenames inside ecommerce_dataset/ (no CSV content).
