import stripe
from datetime import datetime, timezone, timedelta


def load_payments_from_stripe(api_key, limit=20):
    stripe.api_key = api_key

    payments = []

    start_time = int((datetime.now(timezone.utc) - timedelta(minutes=10)).timestamp())

    response = stripe.PaymentIntent.list(
        limit=100,
        created={"gte": start_time}
    )

    for p in response.auto_paging_iter():
        if len(payments) >= limit:
            break

        if p.status != "succeeded":
            continue

        order_id = None
        try:
            order_id = p.metadata["order_id"]
        except Exception:
            pass

        payments.append({
            "id": p.id,
            "email": p.receipt_email or "unknown@test.com",
            "amount": p.amount,
            "order_id": order_id
        })

    return payments