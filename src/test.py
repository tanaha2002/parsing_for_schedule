from parse.messenge_process import MessengeProcess
import os


list_test_ = [
    ["I am available every morning from 9 to 11 AM, except on Wednesdays",
    "I am free on Tuesdays, but if possible, I prefer an early morning slot.",
    "I already have a meeting booked on Friday from 2 to 4 PM.",],

    [" I'm busy all day, but free in the afternoon on Friday.",
    "I already have a meeting booked on Friday from 2 to 4 PM.",
    "I can meet anytime after 3 PM."],

    ["Not available on Thursday.",
    "Available all day except on Wednesday.",
    "I'm not free on Tuesday but available on Wednesday.",],

    ["Not available on Thursday.",
    "Available all day except on Wednesday.",
    "I am free on Tuesdays, but if possible, I prefer an early morning slot.",]

]
current_path = os.path.dirname(os.path.abspath(__file__))
preference_path = os.path.join(current_path, "pattern/prefer.txt")
splitword_path = os.path.join(current_path, "pattern/splitword.txt")
negative_path = os.path.join(current_path, "pattern/negative.txt")

messenges_process = MessengeProcess(preference_path, splitword_path, negative_path)

for list_test in list_test_:
    print("*"*50)
    print(f"Test case: {list_test_.index(list_test)+1}")
    list_user, available_slots = messenges_process.process(list_test)

    for idx, user in enumerate(list_user):
        print(f"User {idx+1}:")
        print(f"Message: {user.messenge}")
        print(f"Available_part: {user.available_extract}")
        print(f"Exception_part: {user.exception_extract}")
        print(f"Preference_part: {user.preference_extract}")
        print(f"Available days: {user.day_available}")
        print(f"Unavailable days: {user.day_unavailable}")
        print(f"Time available: {user.time_available}")
        print(f"Time available in unavailable days: {user.time_available_in_unavailable}")
        print("="*50)

    if available_slots:
        print(f"Found available meeting time:")
        for day, time_slot in available_slots:
            start_time, end_time = time_slot
            start_str = f"{start_time:02d}:00"
            end_str = f"{end_time:02d}:00"
            print(f"{day.capitalize()}: {start_str} - {end_str}")
    else:
        print(f"Cannot create any schedule.")
    print("*"*50)