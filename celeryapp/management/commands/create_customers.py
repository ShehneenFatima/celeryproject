import pytz
import random
import string
from django.core.management.base import BaseCommand
from django.utils import timezone
from celeryapp.models import Customer

def random_string(length=8):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

class Command(BaseCommand):
    help = 'Creates 100 dummy customers with PST timestamps'

    def handle(self, *args, **kwargs):
        pst = pytz.timezone('America/Los_Angeles')
        now_utc = timezone.now()

        for i in range(100):
            name = f"Customer {i+1}"
            email = f"{random_string()}@example.com"
            # Generate a random time in the last 24 hours (in PST)
            random_minutes = random.randint(0, 60 * 24)
            created_at_pst = now_utc.astimezone(pst) - timezone.timedelta(minutes=random_minutes)

            Customer.objects.create(
                name=name,
                email=email,
                created_at_pst=created_at_pst
            )
            self.stdout.write(self.style.SUCCESS(f'Created customer {name}'))

        self.stdout.write(self.style.SUCCESS('Successfully created 100 customers'))
