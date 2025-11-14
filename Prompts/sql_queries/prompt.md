You are an expert data engineer. Generate a single SQL query that joins multiple tables from the ecommerce SQLite database and produces a meaningful analytical output.

IMPORTANT:
- Use only SQLite-compatible SQL.
- Do NOT modify the schema or database.
- Do NOT wrap the query in code comments or explanations.
- Output the SQL query ONLY.

GOAL:
Write a SELECT query that joins the following tables:
- customers
- orders
- order_items
- products
- payments

REQUIREMENTS FOR THE QUERY:
- Join all five tables through their correct foreign keys.
- Return one row per order item.
- Include the following columns:
  - customers.full_name
  - customers.city
  - orders.order_id
  - orders.order_date
  - products.name AS product_name
  - order_items.quantity
  - order_items.subtotal
  - payments.payment_method
  - payments.payment_status
- Sort results by orders.order_date descending.

OUTPUT:
Return ONLY the final SQL query with no commentary.