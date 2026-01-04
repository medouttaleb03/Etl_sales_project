import csv
import json

users = []
errors = []

with open("input/sales.csv", "r") as f:
    reader = csv.DictReader(f)

    for row in reader:
        if row["status"] != "paid":
            continue

        try:
            price = int(row["price"])
            quantity = int(row["quantity"])
            total = price * quantity

            users.append({
                "order_id": row["order_id"],
                "user": row["user"],
                "total": total
            })

        except Exception as e:
            errors.append({
                "order_id": row.get("order_id"),
                "error": str(e),
                "row": row
            })


summary = {}

for order in users:
    name = order["user"]
    if name not in summary:
        summary[name] = {"orders_count": 0, "total_spent": 0}

    summary[name]["orders_count"] += 1
    summary[name]["total_spent"] += order["total"]

results = []

for user, data in summary.items():
    label = "VIP" if data["total_spent"] >= 50 else "Normal"
    results.append({
        "user": user,
        "orders_count": data["orders_count"],
        "total_spent": data["total_spent"],
        "label": label
    })

with open("output/sales_clean.json", "w") as f:
    json.dump(results, f, indent=4)

with open("output/errors.log", "w") as f:
    for err in errors:
        f.write(json.dumps(err) + "\n")

