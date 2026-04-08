def load_orders():
    from Order.models import Order

    queryset = Order.objects.all()

    orders = []

    for row in queryset:
        orders.append({
            "order_id": str(row.id),
            "email": row.email,
            "amount": int(row.amount)
        })

    return orders