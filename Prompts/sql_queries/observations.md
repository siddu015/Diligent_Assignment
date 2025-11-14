## SQL Query Generated

Model used: GPT-5.1 Codex High

Cursor produced the following SQL query based on the prompt:

```
SELECT c.full_name,
c.city,
o.order_id,
o.order_date,
p.name AS product_name,
oi.quantity,
oi.subtotal,
pay.payment_method,
pay.payment_status
FROM order_items AS oi
JOIN orders AS o ON oi.order_id = o.order_id
JOIN customers AS c ON o.customer_id = c.customer_id
JOIN products AS p ON oi.product_id = p.product_id
JOIN payments AS pay ON o.order_id = pay.order_id
ORDER BY o.order_date DESC;
```

## Verification Query using prompt

```
Run the following SQL query against database/ecommerce.db and show the first 10 rows of output.
Do NOT modify the database.

QUERY:
SELECT c.full_name,
c.city,
o.order_id,
o.order_date,
p.name AS product_name,
oi.quantity,
oi.subtotal,
pay.payment_method,
pay.payment_status
FROM order_items AS oi
JOIN orders AS o ON oi.order_id = o.order_id
JOIN customers AS c ON o.customer_id = c.customer_id
JOIN products AS p ON oi.product_id = p.product_id
JOIN payments AS pay ON o.order_id = pay.order_id
ORDER BY o.order_date DESC;
```

## Final Result

Result — first 10 rows ordered by `order_date` DESC:

```
full_name         city       order_id                              order_date           product_name                        quantity  subtotal  payment_method  payment_status
Saanvi Patel      Mumbai     e489d089-8fcf-4be8-9761-91201f4f604d  2024-12-30 20:39:27  Madura Living Haven Decor 1         3         205.62    Netbanking      success
Saanvi Patel      Mumbai     e489d089-8fcf-4be8-9761-91201f4f604d  2024-12-30 20:39:27  Aether Pulse Tablets 1              1         6663.51   Netbanking      success
Saanvi Patel      Mumbai     e489d089-8fcf-4be8-9761-91201f4f604d  2024-12-30 20:39:27  Green Trail Origin Staples 1        3         353.37    Netbanking      success
Akira Mathew      New York   1e70d34a-007b-4de4-9f23-34c6ac91db7a  2024-12-30 15:50:13  Urban Loom Heritage Footwear 3      3         1247.88   Gift Card       success
Akira Mathew      New York   1e70d34a-007b-4de4-9f23-34c6ac91db7a  2024-12-30 15:50:13  Lumina Nova Mobiles 2               3         12577.68  Gift Card       success
Akira Mathew      New York   1e70d34a-007b-4de4-9f23-34c6ac91db7a  2024-12-30 15:50:13  Daily Roots Select Snacks 1         2         63.98     Gift Card       success
Akira Mathew      New York   1e70d34a-007b-4de4-9f23-34c6ac91db7a  2024-12-30 15:50:13  Veda Glow Pulse Cosmetics 2         2         131.26    Gift Card       success
Akira Mathew      New York   1e70d34a-007b-4de4-9f23-34c6ac91db7a  2024-12-30 15:50:13  Daily Roots Select Beverages 1      2         117.44    Gift Card       success
Vivaan Fernandes  Hyderabad  6422bc5b-57c0-455d-ac24-cc58d829b6fe  2024-12-28 12:46:07  StridePro Catalyst Athletic Wear 1  2         1400.78   Credit Card     failed
Elias Thomas      Jaipur     33513388-1f9c-4fff-854d-553a1ca23b54  2024-12-25 22:32:32  Allied Drift Menswear 1             2         406.96    Debit Card      success
```

Explanation: executed your exact join across `order_items`, `orders`, `customers`, `products`, and `payments` on `database/ecommerce.db`, sorting newest orders first; added `LIMIT 10` just to keep output to the first 10 rows as requested—read-only, DB untouched.

The SQL query successfully joins all required tables and produces the intended analytical output.
