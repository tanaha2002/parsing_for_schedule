import os
from utils.utils import init_keywords
from parse.day_process import extract_days
from parse.time_process import time_extraction
from typing import List, Optional

class User:
    def __init__(self, messenge: str, available_extract: Optional[str] = None, exception_extract: Optional[str] = None, preference_extract: Optional[str] = None, day_available: List[str] = None, day_unavailable: List[str] = None, time_available: List[str] = None, time_available_in_unavailable: List[str] = None):
        self.messenge = messenge
        self.available_extract = available_extract
        self.exception_extract = exception_extract
        self.preference_extract = preference_extract
        self.day_available = day_available if day_available is not None else []
        self.day_unavailable = day_unavailable if day_unavailable is not None else []
        self.time_available = time_available if time_available is not None else []
        self.time_available_in_unavailable = time_available_in_unavailable if time_available_in_unavailable is not None else []

class MessengeProcess:
    def __init__(self, preference_path, splitword_path, negative_path):
        self.preference_keywords = init_keywords(preference_path)
        self.splitword_keywords = init_keywords(splitword_path)
        self.negative_keywords = init_keywords(negative_path)
    

    def is_preference(self, sentence: str) -> bool:
        """
        Determine if the sentence is a preference or not.
        """
        for pref in self.preference_keywords:
            if pref in sentence:
                return True
        return False
    
    def split_sentence(self, sentence: str) -> tuple:
        """
        Split sentence into available and exception parts, identifying preferences.
        """
        original_sentence = sentence.strip()
        sentence = original_sentence.lower()

        index = -1
        for word in self.splitword_keywords:
            if word in sentence:
                index = sentence.index(word)
                break

        if index == -1:
            parts = [sentence]
        else:
            parts = [sentence[:index].strip(), sentence[index:].strip()]

        available_part = None
        exception_part = None
        preference_part = None

        # Check if part contain more than one element
        part_one = parts[0]
        part_two = parts[1] if len(parts) > 1 else None

        if any(word in part_one for word in self.negative_keywords):
            exception_part = part_one
            if part_two:
                available_part = part_two
        else:
            available_part = part_one
            if part_two:
                exception_part = part_two

        if available_part and self.is_preference(available_part):
            preference_part = available_part
            available_part = None
        if exception_part and self.is_preference(exception_part):
            if preference_part:
                preference_part += " and " + exception_part
            else:
                preference_part = exception_part
            exception_part = None

        return available_part, exception_part, preference_part

    def find_available_slots(self,list_user: list) -> list:
        """
        find scheduler for all user
        """
        available_days = set(list_user[0].day_available)
        # find all day that all user available
        for user in list_user[1:]:
            available_days = available_days.intersection(set(user.day_available))

        if not available_days:
            return []

        available_slots = []
        for day in available_days:
            # get time available of each user in day
            user_slots = []
            for user in list_user:
                #just free 1 period
                if len(user.time_available) == 1:
                    user_slots.append(user.time_available[0])
                else:
                    day_index = user.day_available.index(day)
                    user_slots.append(user.time_available[day_index])
            
            # Find overlap time
            overlap_slots = user_slots[0] 
            for other_user_slots in user_slots[1:]:
                new_overlap = []
                for slot1 in overlap_slots:
                    for slot2 in other_user_slots:
                        start = max(slot1[0], slot2[0])
                        end = min(slot1[1], slot2[1])
                        # Atleast 1 hour for meeting
                        if end - start >= 1:  
                            new_overlap.append((start, end))
                overlap_slots = new_overlap
                
            if overlap_slots:
                for slot in overlap_slots:
                    available_slots.append((day, slot))

        return available_slots

    def process(self, list_messenge: list) -> tuple:
        """
        extract and create scheduler available
        """
        available_list = []
        exception_list = []
        preference_list = []
        list_user = []
        for messenge in list_messenge:
            # split sentence, extract available, exception, preference
            available, exception, preference = self.split_sentence(messenge)
            available_list.append(available)
            exception_list.append(exception)
            preference_list.append(preference)
            # get day available and day unavailable
            day_available, day_unavailable = extract_days(available, exception, preference)
            # create user with information extracted
            list_user.append(User(messenge = messenge, 
                                  available_extract = available, 
                                  exception_extract = exception, 
                                  preference_extract = preference, 
                                  day_available = day_available, 
                                  day_unavailable = day_unavailable))
        # extract time from available, exception
        list_user = time_extraction(list_user)
        # find available slots for all user
        available_slots = self.find_available_slots(list_user)
        return list_user, available_slots
            
