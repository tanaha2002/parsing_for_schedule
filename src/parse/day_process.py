from utils.utils import days_of_week


def extract_days(available_sentence: str, exception_sentence: str, prefer_sentence: str) -> tuple:
    """
    Extract available day from available_sentence and exception_sentence including prefer_sentence
    """
    available_days = []
    unavailable_days = []
    
    # Available day
    if available_sentence:
        for day in days_of_week:
            if day in available_sentence:
                available_days.append(day)
    elif prefer_sentence:
        for day in days_of_week:
            if day in prefer_sentence:
                available_days.append(day)

    # Assume monday to friday if no days are specific
    if not available_days:
        available_days = days_of_week.copy()

    # Unavailable day
    if exception_sentence:
        for day in days_of_week:
            if day in exception_sentence:
                unavailable_days.append(day)

    for day in unavailable_days:
        if day in available_days:
            available_days.remove(day)

    return available_days, unavailable_days
