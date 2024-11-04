from parse.messenge_process import MessengeProcess
import os

RED_COLOR = "\033[91m"
GREEN_COLOR = "\033[92m"
YELLOW_COLOR = "\033[93m"
WHILE_COLOR = "\033[90m"




def app(preference_path: str, splitword_path: str, negative_path: str) -> None:
    """
    Run app
    """
    list_message = []
    while True:
        print("Input the number of users: ")
        try:
            num_users = int(input())
            if num_users == -99:
                break
            if num_users <= 0:
                print(f"{RED_COLOR}Number of users must be greater than 0.{WHILE_COLOR}")
                continue

        except ValueError:
            print(f"{RED_COLOR}Invalid input. Please enter a number.{WHILE_COLOR}")
        for i in range(num_users):
            print(f"Input message of user {i+1}: ")
            message = input()
            list_message.append(message)
        messenges_process = MessengeProcess(preference_path, splitword_path, negative_path)
        list_user, available_slots = messenges_process.process(list_message)
        print(f"{GREEN_COLOR}List of users:{WHILE_COLOR}")
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
            print(f"{GREEN_COLOR}Found available meeting time:{WHILE_COLOR}")
            for day, time_slot in available_slots:
                start_time, end_time = time_slot
                start_str = f"{start_time:02d}:00"
                end_str = f"{end_time:02d}:00"
                print(f"{YELLOW_COLOR}{day.capitalize()}: {start_str} - {end_str}{WHILE_COLOR}")
    

if __name__ == "__main__":
    current_path = os.path.dirname(os.path.abspath(__file__))
    preference_path = os.path.join(current_path, "pattern/prefer.txt")
    splitword_path = os.path.join(current_path, "pattern/splitword.txt")
    negative_path = os.path.join(current_path, "pattern/negative.txt")
    app(preference_path, splitword_path, negative_path)




# list_test = [
# " I'm busy all day, but free in the afternoon on Friday.",
# "I already have a meeting booked on Friday from 2 to 4 PM.",
# "I can meet anytime after 3 PM."
# ]
# current_path = os.path.dirname(os.path.abspath(__file__))
# preference_path = os.path.join(current_path, "pattern/prefer.txt")
# splitword_path = os.path.join(current_path, "pattern/splitword.txt")
# negative_path = os.path.join(current_path, "pattern/negative.txt")

# messenges_process = MessengeProcess(preference_path, splitword_path, negative_path)
# list_user, available_slots = messenges_process.process(list_test)

# for idx, user in enumerate(list_user):
#     print(f"User {idx+1}:")
#     print(f"Message: {user.messenge}")
#     print(f"Available_part: {user.available_extract}")
#     print(f"Exception_part: {user.exception_extract}")
#     print(f"Preference_part: {user.preference_extract}")
#     print(f"Available days: {user.day_available}")
#     print(f"Unavailable days: {user.day_unavailable}")
#     print(f"Time available: {user.time_available}")
#     print(f"Time available in unavailable days: {user.time_available_in_unavailable}")
#     print("="*50)

# if available_slots:
#     for day, time_slot in available_slots:
#         start_time, end_time = time_slot
#         start_str = f"{start_time:02d}:00"
#         end_str = f"{end_time:02d}:00"
#         print(f"{day.capitalize()}: {start_str} - {end_str}")
# else:
#     print(f"Cannot create any schedule.")
