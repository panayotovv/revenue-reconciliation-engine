import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orders_service.settings')
django.setup()

from payments.services.reconciliation_service import run_reconciliation

run_reconciliation()