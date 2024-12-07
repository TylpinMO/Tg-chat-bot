# utils/helper.py

def format_time(delta):
    """Форматирует объект timedelta в строку 'дд:чч:мм'."""
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{days}д:{hours}ч:{minutes}м"