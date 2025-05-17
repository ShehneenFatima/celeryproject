from celery import shared_task
from django.utils import timezone
from django.db.models import F
from celeryapp.models import Customer
import logging
import pytz
from datetime import timezone as dt_timezone
from datetime import timezone as dt_timezone
dt_timezone.utc

logger = logging.getLogger(__name__)

@shared_task
def convert_times():
    logger.info("Running convert_times task")

    # Convert PST -> UTC
    to_convert_to_utc = Customer.objects.filter(created_at_utc__isnull=True)[:10]
    logger.info(f"Found {len(to_convert_to_utc)} customers without UTC time")

    if to_convert_to_utc.exists():
        for customer in to_convert_to_utc:
            try:
                # Ensure created_at_pst is localized properly
                created_at_pst = customer.created_at_pst

                if timezone.is_naive(created_at_pst):
                    # If naive, assume it's in PST and localize it
                    created_at_pst = pytz.timezone("America/Los_Angeles").localize(created_at_pst)

                # Convert to UTC
                utc_time = created_at_pst.astimezone(pytz.utc)
                customer.created_at_utc = utc_time
                customer.save(update_fields=['created_at_utc'])
                logger.info(f"Converted {customer.name} to UTC: {utc_time}")
            except Exception as e:
                logger.error(f"Error converting {customer.name} to UTC: {e}")
        return

    # Once all are converted to UTC, start converting back to PST
    to_convert_to_pst = Customer.objects.exclude(created_at_pst=F('created_at_utc'))[:10]
    logger.info(f"Found {len(to_convert_to_pst)} customers to convert back to PST")

    if to_convert_to_pst.exists():
        for customer in to_convert_to_pst:
            try:
                pst_time = customer.created_at_utc.astimezone(pytz.timezone("America/Los_Angeles"))
                customer.created_at_pst = pst_time
                customer.save(update_fields=['created_at_pst'])
                logger.info(f"Converted {customer.name} to PST: {pst_time}")
            except Exception as e:
                logger.error(f"Error converting {customer.name} to PST: {e}")