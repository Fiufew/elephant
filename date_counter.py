from datetime import datetime, timedelta


SEASONS = {
    'peak': {'start': (12, 21), 'end': (1, 31), 'price': 1400},
    'high': {'start': (11, 1), 'end': (4, 30), 'price': 1000},
    'low': {'start': (5, 1), 'end': (10, 31), 'price': 800}
}


COEFFICIENTS = {
    '3-8': 0.97,
    '9-21': 0.95,
    '22-30': 0.85,
    '31+': 0.80
}


def get_season(date):
    """Определение сезона."""
    for season, details in SEASONS.items():
        start_month, start_day = details['start']
        end_month, end_day = details['end']

        start_date = datetime(date.year, start_month, start_day)
        end_date = datetime(date.year, end_month, end_day)

        if start_month > end_month:
            if date >= start_date or date <= end_date:
                return season
        else:
            if start_date <= date <= end_date:
                return season
    return None


def calculate_rental_cost(start_date, end_date):
    """Рассчет стоимости - коэффициенты."""
    total_cost = 0
    current_date = start_date

    while current_date < end_date:
        next_date = current_date + timedelta(days=1)
        season = get_season(current_date)
        if season:
            total_cost += SEASONS[season]['price']
        current_date = next_date

    rental_days = (end_date - start_date).days
    print(rental_days)
    if rental_days >= 3 and rental_days <= 8:
        coefficient = COEFFICIENTS['3-8']
    elif rental_days >= 9 and rental_days <= 21:
        coefficient = COEFFICIENTS['9-21']
    elif rental_days >= 22 and rental_days <= 30:
        coefficient = COEFFICIENTS['22-30']
    elif rental_days >= 31:
        coefficient = COEFFICIENTS['31+']
    else:
        coefficient = 1.0

    total_cost *= coefficient
    return total_cost


start_date = datetime(2025, 12, 1)
end_date = datetime(2025, 12, 8)
cost = calculate_rental_cost(start_date, end_date)

print(f"Стоимость аренды: {cost}")
