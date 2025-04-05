from datetime import datetime, timedelta

SEASONS = {
    'peak': {'start': (12, 21), 'end': (1, 31)},
    'high': {'start': (11, 1), 'end': (4, 30)},
    'low': {'start': (5, 1), 'end': (10, 31)},
}

COEFFICIENTS = {
    '3-8': 0.97,
    '9-21': 0.95,
    '22-30': 0.85,
    '31+': 0.80
}


def get_season(date):
    """Определение сезона."""
    if isinstance(date, datetime):
        date = date.date()
    for season, details in SEASONS.items():
        start_month, start_day = details['start']
        end_month, end_day = details['end']
        start_date = datetime(date.year, start_month, start_day).date()
        end_date = datetime(date.year, end_month, end_day).date()
        if start_month > end_month:
            if date >= start_date or date <= end_date:
                return season
        else:
            if start_date <= date <= end_date:
                return season
    return None


def calculate_rental_cost(start_date, end_date, pricing):
    "Расчет цены исходя из даты."
    total_cost = 0
    current_date = start_date

    while current_date < end_date:
        next_date = current_date + timedelta(days=1)
        season = get_season(current_date)
        if season:
            total_cost += pricing.get(season, 0)
        current_date = next_date

    rental_days = (end_date - start_date).days

    if 3 <= rental_days <= 8:
        coefficient = COEFFICIENTS['3-8']
    elif 9 <= rental_days <= 21:
        coefficient = COEFFICIENTS['9-21']
    elif 22 <= rental_days <= 30:
        coefficient = COEFFICIENTS['22-30']
    elif rental_days >= 31:
        coefficient = COEFFICIENTS['31+']
    else:
        coefficient = 1.0

    total_cost *= coefficient
    return round(total_cost, 2)
