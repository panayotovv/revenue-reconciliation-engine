from django.core.management.base import BaseCommand
from payments.services.reconciliation_service import run_reconciliation


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        run_reconciliation()