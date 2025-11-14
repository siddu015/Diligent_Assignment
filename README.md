# Diligent Assignment – Cursor A-SDLC Project

1. Generate a synthetic ecommerce dataset (5 CSV files)
2. Ingest the dataset into a fully constrained SQLite database
3. Generate a SQL query that joins multiple tables and returns meaningful output

Each step includes the exact prompt used, validation results, and observations.

---

## Project Structure

Diligent_Assignment/
│
├── ecommerce_dataset/
│ ├── customers.csv
│ ├── products.csv
│ ├── orders.csv
│ ├── order_items.csv
│ └── payments.csv
│
├── database/
│ └── ecommerce.db
│
├── scripts/
│ ├── generate_ecommerce_dataset.py
│ └── ingest_ecommerce_sqlite.py
│
├── prompts/
│ ├── dataset_generation/
│ │ ├── prompt.md
│ │ └── observations.md
│ │
│ ├── ingestion/
│ │ ├── prompt.md
│ │ └── observations.md
│ │
│ └── sql_queries/
│ ├── prompt.md
│ └── observations.md
│
└── README.md

---

## What Each Folder Contains

### **ecommerce_dataset/**

Five CSV files generated using the dataset-generation prompt.  
They are deterministic, relationally consistent, and validated.

### **database/**

Contains the final SQLite database (`ecommerce.db`) produced by the ingestion script.

### **scripts/**

Auto-generated Python files created by Cursor:

- `generate_ecommerce_dataset.py`  
  Creates the 5-file ecommerce dataset.

- `ingest_ecommerce_sqlite.py`  
  Builds the SQLite schema, loads all CSV data, enforces FK constraints, checks totals, and validates payment ratios.

### **prompts/**

Contains the exact prompts used in each stage plus associated observations.

#### dataset_generation/

- `prompt.md` – Final dataset generation prompt
- `observations.md` – Prompt-1, Prompt-2 results, fixes, validation checks

#### ingestion/

- `prompt.md` – Final ingestion prompt
- `observations.md` – Ingestion validation, FK enforcement fix, final confirmation

#### sql_queries/

- `prompt.md` – Prompt used to generate the SQL join query
- `observations.md` – Query output and validation steps

---

## How to Run

All steps are reproducible using Cursor IDE.

### **1. Generate Dataset**

```
cursor apply prompts/dataset_generation/prompt.md
```

### **2. Ingest into SQLite**

```
cursor apply prompts/ingestion/prompt.md
```

### **3. Generate SQL Query**

```
cursor apply prompts/sql_queries/prompt.md
```

### Models Used

All prompts were executed with **GPT-5.1 Codex High** inside Cursor.
