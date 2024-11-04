from utils.utils import MORNING, AFTERNOON, free_full_day, convert_to_24_hour, time_patterns
import re

def adding_available_time_in_unavailable_days(available_time_in_unavailable_days: list,
                                              available_time: list,
                                              available_day: list,
                                              unavailable_day: list) -> list:
    """
    Adding unavailable day to available day and available_time_in_unavailable_days to available_time
    """
    available_day.extend(unavailable_day)
    available_time.extend(available_time_in_unavailable_days)
    return available_day, available_time

def available_time_in_unavailable_days(block_time: list) -> list:
    """
    extract available time in unavailable day
    """
    available_times = []
    morning_available = [MORNING]
    afternoon_available = [AFTERNOON]

    for block in block_time:
        block_start, block_end = block

        # morning
        new_morning_available = []
        for start, end in morning_available:
            # full morning
            if block_start <= start and block_end >= end:
                continue
            # block from 7 to block_end
            if block_start <= start < block_end < end:
                new_morning_available.append((block_end, end))
            # block from block_start to 11
            elif start < block_start < end <= block_end:
                new_morning_available.append((start, block_start))
            # range block inside morning
            elif start < block_start < block_end < end:
                new_morning_available.append((start, block_start))
                new_morning_available.append((block_end, end))
            # no block
            else:
                new_morning_available.append((start, end))

        morning_available = new_morning_available

        # afternoon
        new_afternoon_available = []
        for start, end in afternoon_available:
            # full afternoon
            if block_start <= start and block_end >= end:
                continue 
            # block from 13 to block_end
            if block_start <= start < block_end < end:
                new_afternoon_available.append((block_end, end))
            # block from block_start to 17
            elif start < block_start < end <= block_end:
                new_afternoon_available.append((start, block_start))
            # range block inside afternoon
            elif start < block_start < block_end < end:
                new_afternoon_available.append((start, block_start))
                new_afternoon_available.append((block_end, end))
            # no block
            else:
                new_afternoon_available.append((start, end))

        afternoon_available = new_afternoon_available

    # available time
    available_times.extend(morning_available)
    available_times.extend(afternoon_available)
    return available_times


def extract_time_from_message(message: str) -> list:
    """
    Usig pattern to extract time from messenge
    """
    time_slots = []
    for pattern in time_patterns:
        matches = re.findall(pattern, message)
        for match in matches:
            # print(f"match: {match}")
            # From X AM/PM to Y AM/PM
            if len(match) == 4:
                #case for X am to Y am
                if match[1] == 'am' and match[3] == 'am':
                    start_time = convert_to_24_hour(match[0], match[1])
                    end_time = convert_to_24_hour(match[2], match[3])
                    time_slots.append((start_time, end_time))
                #case for X pm to Y pm
                if match[1] == 'pm' and match[3] == 'pm':
                    start_time = convert_to_24_hour(match[0], match[1])
                    end_time = convert_to_24_hour(match[2], match[3])
                    time_slots.append((start_time, end_time))
                #case for X am to Y pm
                if match[1] == 'am' and match[3] == 'pm':
                    start_time = convert_to_24_hour(match[0], match[1])
                    end_time = convert_to_24_hour(match[2], match[3])
                    time_slots.append((start_time, 11))
                    time_slots.append((13, end_time))

            # From X to Y AM/PM
            elif len(match) == 3: 
                #case X > Y (9 to 5 pm, 10 to 3 pm, 8 to 4 pm),...
                if int(match[0]) > int(match[1]):
                    # print(f"You match special: {match}")
                    start_time = convert_to_24_hour(match[0], "am")
                    end_time = convert_to_24_hour(match[1], match[2])
                    time_slots.append((start_time, 11))
                    time_slots.append((13, end_time))
                else:
                    start_time = convert_to_24_hour(match[0], match[2])
                    end_time = convert_to_24_hour(match[1], match[2])
                    time_slots.append((start_time, end_time))
            # After X AM/PM
            elif len(match) == 2 and 'after' in pattern:
                start_time = convert_to_24_hour(match[0], match[1])
                time_slots.append((start_time, 17))
            # Before X AM/PM
            elif len(match) == 2 and 'before' in pattern:
                end_time = convert_to_24_hour(match[0], match[1])
                time_slots.append((7, end_time))
            # Contains "morning"
            elif match[0] == 'morning':
                time_slots.append(MORNING) 
            # Contains "afternoon"
            elif match[0] == 'afternoon':
                time_slots.append(AFTERNOON)
    return time_slots



def time_extraction(list_user: list) -> list:
    """
    extract time from user's message (available, exception) and calculate for each day.
    """
    for user in list_user:
        # Extract available times from messenge
        available_times = []
        unavailable_times = []

        if user.available_extract:
            available_times = extract_time_from_message(user.available_extract)

            # If user specifies a time slot, only take that time slot
            if available_times:
                user.time_available = [available_times] * len(user.day_available)
            else:
                # If no specific time slot is mention but "morning"/"afternoon" in messenge
                if 'morning' in user.available_extract:
                    user.time_available = [[(7, 11)]] * len(user.day_available)
                elif 'afternoon' in user.available_extract:
                    user.time_available = [[(13, 17)]] * len(user.day_available)
                else:
                    # Assume fullday free if no specific time is mentioned
                    user.time_available = [free_full_day()] * len(user.day_available)
        else:
            # If no time is mention, assume fullday free for available day
            user.time_available = [free_full_day()] * len(user.day_available)

        if user.exception_extract:
            
            unavailable_times = extract_time_from_message(user.exception_extract)
            
            # that mean user have specific time in unavailable day.
            if unavailable_times:
                available_in_unavailable = available_time_in_unavailable_days(unavailable_times)
                user.time_available_in_unavailable = [available_in_unavailable] * len(user.day_unavailable)
            else:
                user.time_available_in_unavailable = []

        #if have available time in unavailable day, add it to available day and available time
        if user.time_available_in_unavailable:
            user.day_available, user.time_available = adding_available_time_in_unavailable_days(
                user.time_available_in_unavailable, 
                user.time_available, 
                user.day_available, 
                user.day_unavailable)

    return list_user