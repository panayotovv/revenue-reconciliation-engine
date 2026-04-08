from collections import defaultdict

def reconcile(orders, payments, logger, tolerance=1):
    results = []

    used_payment_ids = set()

    payments_by_order_id = {}
    payments_by_email = defaultdict(list)

    for p in payments:
        if p.get("order_id"):
            payments_by_order_id[str(p["order_id"])] = p

        payments_by_email[p["email"]].append(p)

    for order in orders:
        order_id = str(order["order_id"])
        result = {
            "order_id": order_id,
            "email": order["email"],
            "amount": order["amount"],
            "status": None,
            "confidence": 0.0,
            "payment_id": None
        }

        if order_id in payments_by_order_id:
            p = payments_by_order_id[order_id]

            if p["id"] not in used_payment_ids:
                result["payment_id"] = p["id"]

                if abs(p["amount"] - order["amount"]) <= tolerance:
                    result["status"] = "matched"
                    result["confidence"] = 1.0
                else:
                    result["status"] = "amount_mismatch"
                    result["confidence"] = 0.8
                    logger.warning(f"Amount mismatch for order {order_id}")

                used_payment_ids.add(p["id"])
                results.append(result)
                continue

        possible = payments_by_email.get(order["email"], [])

        for p in possible:
            if p["id"] in used_payment_ids:
                continue

            result["payment_id"] = p["id"]

            if abs(p["amount"] - order["amount"]) < tolerance:
                result["status"] = "matched_fallback"
                result["confidence"] = 0.7
            else:
                result["status"] = "weak_mismatch"
                result["confidence"] = 0.4

            used_payment_ids.add(p["id"])
            results.append(result)
            break

        if result["status"] is None:
            result["status"] = "missing"
            result["confidence"] = 0.0
            logger.warning(f"Missing payment for order {order_id}")
            results.append(result)

    for p in payments:
        if p["id"] not in used_payment_ids:
            results.append({
                "order_id": None,
                "email": p["email"],
                "amount": p["amount"],
                "status": "extra_payment",
                "confidence": 0.0,
                "payment_id": p["id"]
            })

    return results