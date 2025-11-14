#!/usr/bin/env python3
"""Deterministic ecommerce dataset generator."""

from __future__ import annotations

import csv
import random
import uuid
from datetime import datetime, timedelta
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

SEED = 42
getcontext().prec = 28

OUTPUT_DIR = Path(__file__).resolve().parent / "ecommerce_dataset"
DATE_RANGE_START = datetime(2022, 1, 1, 6, 0, 0)
DATE_RANGE_END = datetime(2024, 12, 31, 22, 0, 0)

CATEGORY_PLAN = {
    "electronics": 60,
    "fashion": 75,
    "home": 45,
    "beauty": 45,
    "sports": 30,
    "grocery": 45,
}

CATEGORY_SPECS = {
    "electronics": {
        "sub_categories": ["mobiles", "laptops", "headphones", "tablets"],
        "brands": ["Aether", "Solace", "Cadenza", "Vertex", "Lumina", "Pulse"],
        "models": ["Edge", "Nova", "Hyper", "Quantum", "Pulse", "Zen"],
        "price_range_cents": (150000, 1250000),
    },
    "fashion": {
        "sub_categories": ["menswear", "womenswear", "footwear", "accessories"],
        "brands": ["Urban Loom", "Saffron Lane", "Ivory Thread", "Northstone", "Allied"],
        "models": ["Heritage", "Drift", "Monsoon", "Kinetic", "Vista"],
        "price_range_cents": (2500, 45000),
    },
    "home": {
        "sub_categories": ["furniture", "decor", "kitchenware"],
        "brands": ["HarborLeaf", "Madura Living", "Oak & Arc", "Casa Meridian"],
        "models": ["Studio", "Element", "Haven", "Sierra", "Breeze"],
        "price_range_cents": (5000, 85000),
    },
    "beauty": {
        "sub_categories": ["skincare", "haircare", "cosmetics"],
        "brands": ["Mirai", "Aurum", "Serene", "Veda Glow"],
        "models": ["Pure", "Radiant", "Bloom", "Aura", "Pulse"],
        "price_range_cents": (1500, 18000),
    },
    "sports": {
        "sub_categories": ["fitness", "outdoor", "athletic wear"],
        "brands": ["StridePro", "PeakForge", "Nimbus Trails", "RapidFlex"],
        "models": ["Velocity", "Summit", "Pulse", "Catalyst", "Momentum"],
        "price_range_cents": (4000, 95000),
    },
    "grocery": {
        "sub_categories": ["snacks", "beverages", "staples"],
        "brands": ["Harvest Bay", "Daily Roots", "Green Trail", "Spiceway"],
        "models": ["Select", "Origin", "Classic", "Pure"],
        "price_range_cents": (800, 12000),
    },
}

PAYMENT_METHODS = [
    "Gift Card",
    "UPI",
    "Credit Card",
    "Debit Card",
    "COD",
    "Netbanking",
]

ORDER_STATUS_WEIGHTS: Sequence[Tuple[str, float]] = (
    ("delivered", 0.58),
    ("shipped", 0.18),
    ("created", 0.12),
    ("cancelled", 0.07),
    ("returned", 0.05),
)

PHONE_PATTERNS = [
    ("+91", 10),
    ("+1", 10),
    ("+44", 10),
    ("+65", 8),
    ("+61", 9),
    ("+971", 9),
    ("+81", 10),
    ("+49", 10),
    ("+33", 9),
    ("+27", 9),
]

FIRST_NAMES = [
    "Aarav",
    "Vihaan",
    "Ishaan",
    "Advait",
    "Reyansh",
    "Kabir",
    "Arjun",
    "Vivaan",
    "Aditya",
    "Rohan",
    "Ananya",
    "Diya",
    "Myra",
    "Kiara",
    "Aadhya",
    "Meera",
    "Saanvi",
    "Navya",
    "Sara",
    "Zara",
    "Emily",
    "Olivia",
    "Sophia",
    "Ava",
    "Mia",
    "Liam",
    "Noah",
    "Ethan",
    "Lucas",
    "Mason",
    "Hiro",
    "Yuna",
    "Akira",
    "Sora",
    "Nia",
    "Elias",
    "Mateo",
    "Luca",
    "Isla",
    "Chloe",
    "Harper",
    "Isabella",
]

LAST_NAMES = [
    "Sharma",
    "Patel",
    "Reddy",
    "Singh",
    "Iyer",
    "Fernandes",
    "Kapoor",
    "Das",
    "Desai",
    "Verma",
    "Gupta",
    "Chopra",
    "Khan",
    "Nair",
    "Bose",
    "Mukherjee",
    "Ahuja",
    "Menon",
    "Kulkarni",
    "Bhat",
    "Ghosh",
    "Mehta",
    "Banerjee",
    "Pillai",
    "Joshi",
    "Mathew",
    "Rao",
    "Thomas",
    "Carter",
    "Green",
    "Lopez",
    "Wong",
    "Kim",
    "Garcia",
    "Murphy",
    "Anderson",
    "Brown",
    "Martinez",
    "Evans",
    "Hughes",
    "Davis",
    "Turner",
    "Collins",
]

CITY_OPTIONS = [
    {"city": "Bengaluru", "state": "Karnataka", "country": "India"},
    {"city": "Mumbai", "state": "Maharashtra", "country": "India"},
    {"city": "Hyderabad", "state": "Telangana", "country": "India"},
    {"city": "Chennai", "state": "Tamil Nadu", "country": "India"},
    {"city": "Pune", "state": "Maharashtra", "country": "India"},
    {"city": "Delhi", "state": "Delhi", "country": "India"},
    {"city": "Kolkata", "state": "West Bengal", "country": "India"},
    {"city": "Ahmedabad", "state": "Gujarat", "country": "India"},
    {"city": "Jaipur", "state": "Rajasthan", "country": "India"},
    {"city": "Lucknow", "state": "Uttar Pradesh", "country": "India"},
    {"city": "Singapore", "state": "Singapore", "country": "Singapore"},
    {"city": "Dubai", "state": "Dubai", "country": "UAE"},
    {"city": "London", "state": "England", "country": "United Kingdom"},
    {"city": "New York", "state": "New York", "country": "USA"},
    {"city": "Toronto", "state": "Ontario", "country": "Canada"},
    {"city": "Sydney", "state": "New South Wales", "country": "Australia"},
    {"city": "Kuala Lumpur", "state": "Federal Territory", "country": "Malaysia"},
    {"city": "Johannesburg", "state": "Gauteng", "country": "South Africa"},
    {"city": "Dublin", "state": "Leinster", "country": "Ireland"},
    {"city": "Berlin", "state": "Berlin", "country": "Germany"},
]

STREET_NAMES = [
    "Mahatma Gandhi Road",
    "Brigade Road",
    "Lavelle Road",
    "Indiranagar 100ft Road",
    "Residency Road",
    "Park Street",
    "Marine Drive",
    "Anna Salai",
    "Linking Road",
    "Commercial Street",
    "Oak Meadows",
    "Cedar Lane",
    "Palm Avenue",
    "Maple Residency",
    "Sunset Boulevard",
    "Sarjapur Main Road",
    "Bandra Kurla Complex",
    "HSR Layout Sector",
    "Kensington High Street",
    "Orchard Boulevard",
]

LOCALITY_SUFFIXES = ["Layout", "Enclave", "Nagar", "Heights", "Residency", "Gardens", "Phase", "Vista"]
EMAIL_DOMAINS = ["gmail.com", "outlook.com", "yahoo.com"]


def make_rng() -> random.Random:
    return random.Random(SEED)


def slugify(value: str) -> str:
    clean_chars: List[str] = []
    previous_dash = False
    for char in value.lower():
        if char.isalnum():
            clean_chars.append(char)
            previous_dash = False
        elif char in {" ", "-", "_"}:
            if not previous_dash:
                clean_chars.append("-")
                previous_dash = True
        else:
            continue
    slug = "".join(clean_chars).strip("-")
    return slug or "user"


def random_datetime_in_range(rng: random.Random, start: datetime, end: datetime) -> datetime:
    total_seconds = int((end - start).total_seconds())
    offset = rng.randint(0, total_seconds)
    return start + timedelta(seconds=offset)


def build_seasonal_windows() -> List[Tuple[datetime, datetime]]:
    specs = [
        (1, 20, 25),  # Republic Day week
        (5, 1, 31),   # Summer sale month
        (8, 10, 15),  # Independence Day
        (10, 20, 30), # Dasara
        (11, 1, 12),  # Diwali early Nov
        (11, 23, 30), # Black Friday late Nov
        (12, 20, 25), # Christmas
    ]
    windows: List[Tuple[datetime, datetime]] = []
    for year in (2022, 2023, 2024):
        for month, start_day, end_day in specs:
            window_start = datetime(year, month, start_day, 7, 0, 0)
            window_end = datetime(year, month, end_day, 23, 0, 0)
            windows.append((window_start, window_end))
    return windows


SEASONAL_WINDOWS = build_seasonal_windows()


def seasonal_order_datetime(rng: random.Random) -> datetime:
    window_start, window_end = rng.choice(SEASONAL_WINDOWS)
    return random_datetime_in_range(rng, window_start, window_end)


def pick_order_datetime(rng: random.Random) -> datetime:
    if rng.random() < 0.72:
        return seasonal_order_datetime(rng)
    return random_datetime_in_range(rng, DATE_RANGE_START, DATE_RANGE_END)


def weighted_choice(rng: random.Random, options: Sequence[Tuple[str, float]]) -> str:
    roll = rng.random()
    cumulative = 0.0
    for value, weight in options:
        cumulative += weight
        if roll <= cumulative:
            return value
    return options[-1][0]


def generate_customers(num_customers: int = 1500) -> List[Dict[str, str]]:
    rng = make_rng()
    customers: List[Dict[str, str]] = []
    used_emails = set()
    used_phones = set()
    for idx in range(num_customers):
        first = rng.choice(FIRST_NAMES)
        last = rng.choice(LAST_NAMES)
        full_name = f"{first} {last}"
        slug = slugify(full_name)
        domain = EMAIL_DOMAINS[idx % len(EMAIL_DOMAINS)]
        email_candidate = f"{slug}.{idx + 1}@{domain}"
        if email_candidate in used_emails:
            email_candidate = f"{slug}.{idx + 1}.{rng.randint(10, 99)}@{domain}"
        used_emails.add(email_candidate)

        phone = create_phone_number(rng, idx, used_phones)

        location = rng.choice(CITY_OPTIONS)
        address = generate_address(rng)
        created_at = random_datetime_in_range(rng, DATE_RANGE_START, DATE_RANGE_END)

        customers.append(
            {
                "customer_id": str(uuid.uuid4()),
                "full_name": full_name,
                "email": email_candidate,
                "phone": phone,
                "address": address,
                "city": location["city"],
                "state": location["state"],
                "country": location["country"],
                "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
    return customers


def create_phone_number(rng: random.Random, seed_idx: int, used: set) -> str:
    attempts = 0
    while True:
        code, length = PHONE_PATTERNS[(seed_idx + attempts) % len(PHONE_PATTERNS)]
        digits = "".join(str(rng.randint(0, 9)) for _ in range(length))
        number = f"{code}-{digits}"
        if number not in used:
            used.add(number)
            return number
        attempts += 1


def generate_address(rng: random.Random) -> str:
    number = rng.randint(12, 980)
    street = rng.choice(STREET_NAMES)
    suffix = rng.choice(LOCALITY_SUFFIXES)
    block = rng.randint(1, 9)
    return f"{number} {street}, Block {block}, {suffix}"


def generate_products(num_products: int = 300) -> List[Dict[str, object]]:
    rng = make_rng()
    products: List[Dict[str, object]] = []
    counters: Dict[Tuple[str, str, str], int] = {}
    for category, target_count in CATEGORY_PLAN.items():
        spec = CATEGORY_SPECS[category]
        for _ in range(target_count):
            sub_category = rng.choice(spec["sub_categories"])
            brand = rng.choice(spec["brands"])
            model = rng.choice(spec["models"])
            key = (brand, model, sub_category)
            counters[key] = counters.get(key, 0) + 1
            suffix = counters[key]
            name = f"{brand} {model} {sub_category.title()} {suffix}"
            min_cents, max_cents = spec["price_range_cents"]
            price_cents = rng.randint(min_cents, max_cents)
            price = Decimal(price_cents) / Decimal("100")
            stock_quantity = rng.randint(5, 500)
            added_at = random_datetime_in_range(rng, DATE_RANGE_START, DATE_RANGE_END)
            products.append(
                {
                    "product_id": str(uuid.uuid4()),
                    "name": name,
                    "category": category,
                    "sub_category": sub_category,
                    "price": price,
                    "stock_quantity": stock_quantity,
                    "added_at": added_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
    return products


def generate_orders(customers: Sequence[Dict[str, str]], num_orders: int = 1500) -> List[Dict[str, object]]:
    rng = make_rng()
    orders: List[Dict[str, object]] = []
    for _ in range(num_orders):
        customer = rng.choice(customers)
        order_datetime = pick_order_datetime(rng)
        status = weighted_choice(rng, ORDER_STATUS_WEIGHTS)
        order = {
            "order_id": str(uuid.uuid4()),
            "customer_id": customer["customer_id"],
            "order_date": order_datetime,
            "total_amount": Decimal("0"),
            "status": status,
            "city": customer["city"],
            "state": customer["state"],
            "country": customer["country"],
        }
        orders.append(order)
    return orders


def allocate_item_counts(num_orders: int, rng: random.Random) -> List[int]:
    counts = [1] * num_orders
    target_total = rng.randint(4000, 6000)
    total_items = num_orders
    adjustable_indices = list(range(num_orders))
    while total_items < target_total:
        idx = rng.choice(adjustable_indices)
        if counts[idx] < 5:
            counts[idx] += 1
            total_items += 1
        else:
            adjustable_indices.remove(idx)
            if not adjustable_indices:
                break
    return counts


def generate_order_items(
    orders: Sequence[Dict[str, object]], products: Sequence[Dict[str, object]]
) -> List[Dict[str, object]]:
    rng = make_rng()
    counts = allocate_item_counts(len(orders), rng)
    order_items: List[Dict[str, object]] = []
    product_choices = list(products)
    for order, item_count in zip(orders, counts):
        for _ in range(item_count):
            product = rng.choice(product_choices)
            quantity = rng.randint(1, 3)
            price: Decimal = product["price"]
            subtotal = price * Decimal(quantity)
            order["total_amount"] += subtotal
            order_items.append(
                {
                    "order_item_id": str(uuid.uuid4()),
                    "order_id": order["order_id"],
                    "product_id": product["product_id"],
                    "quantity": quantity,
                    "item_price": price,
                    "subtotal": subtotal,
                }
            )
    return order_items


def generate_payments(orders: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    rng = make_rng()
    payments: List[Dict[str, object]] = []
    for order in orders:
        payment_status = "success" if rng.random() < 0.92 else "failed"
        payment_method = rng.choice(PAYMENT_METHODS)
        offset_seconds = rng.randint(5, 180)
        order_datetime: datetime = order["order_date"]
        transaction_timestamp = order_datetime + timedelta(seconds=offset_seconds)
        payments.append(
            {
                "payment_id": str(uuid.uuid4()),
                "order_id": order["order_id"],
                "payment_method": payment_method,
                "amount": order["total_amount"],
                "payment_status": payment_status,
                "transaction_timestamp": transaction_timestamp,
            }
        )
    return payments


def serialize_row(row: Dict[str, object]) -> Dict[str, object]:
    serialized: Dict[str, object] = {}
    for key, value in row.items():
        if isinstance(value, Decimal):
            serialized[key] = format(value, "f")
        elif isinstance(value, datetime):
            serialized[key] = value.strftime("%Y-%m-%d %H:%M:%S")
        else:
            serialized[key] = value
    return serialized


def write_csv(path: Path, headers: Sequence[str], rows: Iterable[Dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(serialize_row(row))


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    customers = generate_customers()
    products = generate_products()
    orders = generate_orders(customers)
    order_items = generate_order_items(orders, products)
    payments = generate_payments(orders)

    customers_path = OUTPUT_DIR / "customers.csv"
    products_path = OUTPUT_DIR / "products.csv"
    orders_path = OUTPUT_DIR / "orders.csv"
    order_items_path = OUTPUT_DIR / "order_items.csv"
    payments_path = OUTPUT_DIR / "payments.csv"

    write_csv(
        customers_path,
        [
            "customer_id",
            "full_name",
            "email",
            "phone",
            "address",
            "city",
            "state",
            "country",
            "created_at",
        ],
        customers,
    )

    write_csv(
        products_path,
        [
            "product_id",
            "name",
            "category",
            "sub_category",
            "price",
            "stock_quantity",
            "added_at",
        ],
        products,
    )

    write_csv(
        orders_path,
        [
            "order_id",
            "customer_id",
            "order_date",
            "total_amount",
            "status",
            "city",
            "state",
            "country",
        ],
        orders,
    )

    write_csv(
        order_items_path,
        [
            "order_item_id",
            "order_id",
            "product_id",
            "quantity",
            "item_price",
            "subtotal",
        ],
        order_items,
    )

    write_csv(
        payments_path,
        [
            "payment_id",
            "order_id",
            "payment_method",
            "amount",
            "payment_status",
            "transaction_timestamp",
        ],
        payments,
    )


if __name__ == "__main__":
    main()
