from datetime import timedelta
from django.utils import timezone
from .models import Date


class TelegramRentalInfo:

    @staticmethod
    def get_tomorrow_rentals():
        """Возвращает все заявки с датой доставки завтра."""
        tomorrow = timezone.now().date() + timedelta(days=1)
        rentals = Date.objects.filter(
            date_delivery=tomorrow
        ).select_related(
            'application'
        )

        result = []
        for rental in rentals:
            app = rental.application
            result.append({
                'application_num': app.num,
                'client_name': app.client_name,
                'contacts': app.contacts,
                'car': app.auto,
                'delivery_location': app.location_delivery,
                'return_location': app.location_return,
                'delivery_date': rental.date_delivery,
                'return_date': rental.date_return,
                'price': f"{app.price} {app.currency}",
                'deposit': f"{app.deposit_in_hand} {app.currency}",
            })

        return result

    @staticmethod
    def format_tomorrow_rentals():
        """Форматирует заявки на завтра в читаемое сообщение для Telegram."""
        rentals = TelegramRentalInfo.get_tomorrow_rentals()

        if not rentals:
            return "На завтра аренд нет."

        message = ["📅 *Аренды на завтра:*"]
        for i, rental in enumerate(rentals, 1):
            message.append(
                f"\n{i}. *Заявка #{rental['application_num']}*\n"
                f"👤 Клиент: {rental['client_name']}\n"
                f"📞 Контакты: {rental['contacts']}\n"
                f"🚗 Авто: {rental['car']}\n"
                f"📍 Локация доставки: {rental['delivery_location']}\n"
                f"📆 Дата доставки: {rental['delivery_date'].strftime('%d.%m.%Y')}\n"
                f"📆 Дата возврата: {rental['return_date'].strftime('%d.%m.%Y')}\n"
                f"💵 Цена: {rental['price']}\n"
                f"💰 Депозит: {rental['deposit']}"
            )

        return "\n".join(message)
