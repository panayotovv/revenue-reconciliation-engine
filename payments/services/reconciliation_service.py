from payments.services import config
from payments.services.orders_loader import load_orders
from payments.services.payments_loader import load_payments_from_stripe
from payments.services.reconcile import reconcile
from payments.services.exporter import export_results
from payments.services.logger import setup_logger
from payments.services.alerts import analyze_and_alert


def run_reconciliation():
    logger = setup_logger()

    logger.info("Starting reconciliation process")

    try:
        orders = load_orders()
        logger.info(f"Loaded {len(orders)} orders")
    except Exception as e:
        logger.error(f"Failed to load orders: {e}")
        return

    payments = load_payments_from_stripe(
        api_key=config.STRIPE_API_KEY,
        limit=100
    )
    logger.info(f"Loaded {len(payments)} payments from Stripe")

    results = reconcile(orders, payments, logger)
    logger.info("Reconciliation completed")

    total = len(orders)
    matched = [r for r in results if "matched" in r["status"]]
    mismatched = [r for r in results if "mismatch" in r["status"]]
    missing = [r for r in results if r["status"] == "missing"]
    extra = [r for r in results if r["status"] == "extra_payment"]

    match_rate = (len(matched) / total) * 100 if total else 0

    alerts = analyze_and_alert(
        results,
        logger,
        webhook_url=config.SLACK_WEBHOOK_URL
    )

    logger.info(f"Low confidence: {alerts['low_confidence']}")
    logger.info(f"Missing payments: {alerts['missing']}")

    export_results(results, "report.csv")
    logger.info("Results exported to report.csv")

    logger.info("Reconciliation process finished")

    summary = (
        f"Total orders: {total}\n"
        f"Matched: {len(matched)}\n"
        f"Mismatched: {len(mismatched)}\n"
        f"Missing: {len(missing)}\n"
        f"Extra: {len(extra)}\n"
        f"Match rate: {match_rate:.2f}%\n"
    )

    print(summary)