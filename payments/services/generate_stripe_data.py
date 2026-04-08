import stripe
import random
import config
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orders_service.settings')
django.setup()

from orders_loader import load_orders

stripe.api_key = config.STRIPE_API_KEY

orders = load_orders()

for order in orders:
    if random.random() < 0.7:
        stripe.PaymentIntent.create(
            amount=order["amount"],
            currency="usd",
            payment_method_types=["card"],
            payment_method="pm_card_visa",
            confirm=True,
            metadata={
                "order_id": str(order["order_id"])
            }
        )

    elif random.random() < 0.5:
        stripe.PaymentIntent.create(
            amount=order["amount"] - 200,
            currency="usd",
            payment_method_types=["card"],
            payment_method="pm_card_visa",
            confirm=True,
            metadata={
                "order_id": str(order["order_id"])
            }
        )

    else:
        stripe.PaymentIntent.create(
            amount=order["amount"],
            currency="usd",
            payment_method_types=["card"],
            payment_method="pm_card_visa",
            confirm=True,
            metadata={
                "order_id": str(order["order_id"])
            }
        )

        # stripe.PaymentIntent.create(
        #     amount=order["amount"],
        #     currency="usd",
        #     payment_method_types=["card"],
        #     payment_method="pm_card_visa",
        #     confirm=True,
        #     metadata={
        #         "order_id": str(order["order_id"])
        #     }
        # )