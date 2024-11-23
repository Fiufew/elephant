from celery import shared_task
from django.utils import timezone

from .models import Bid
from .management.commands.telegram import send_message_sync


@shared_task
def check_rental_expiration():
    bids = Bid.objects.all()
    expired_list = []
    bids_to_update = []
    for bid in bids:
        if bid.dropoff_time < timezone.now() and not bid.is_expired and not bid.is_pending:
            expired_list.append(f'Заявка №{bid.id} истекла')
            bid.is_expired = True
            bids_to_update.append(bid)
    if expired_list:
        message = '\n'.join(expired_list)
        send_message_sync(message=message)
    if bids_to_update:
        Bid.objects.bulk_update(bids_to_update, ['is_expired'])
