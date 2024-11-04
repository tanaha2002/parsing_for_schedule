import os

MORNING = (7, 11)
AFTERNOON = (13, 17)
days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

time_patterns = [
    r'(\d{1,2}) (am|pm) to (\d{1,2}) (am|pm)',    # From X AM/PM to Y AM/PM
    r'(\d{1,2}) to (\d{1,2}) (am|pm)',            # From X to Y AM/PM         
    r'after (\d{1,2}) (am|pm)',                   # After X AM/PM
    r'before (\d{1,2}) (am|pm)',                  # Before X AM/PM
    r'until (\d{1,2}) (am|pm)',                   # Until X AM/PM
    r'till (\d{1,2}) (am|pm)',                    # Till X AM/PM
    r'(morning|afternoon)'                        # Morning or afternoon
]


def convert_to_24_hour(time_str: str, period: str) -> int:
    """
    convert from 12 hour to 24 hour
    """
    time = int(time_str)
    if period == 'pm' and time != 12:
        time += 12
    elif period == 'am' and time == 12:
        time = 0
    return time

def free_full_day() -> list:
    return [MORNING, AFTERNOON]

def init_keywords(path: str) -> list:
    """
    initialize keyword from file.
    """
    with open(path, "r") as file:
        keywords = file.read().splitlines()
    return keywords