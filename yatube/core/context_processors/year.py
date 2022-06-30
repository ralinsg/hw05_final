from datetime import date


def year(request):
    dt = date.today().year
    """Добавляет переменную с текущим годом."""
    return {"year": dt}
