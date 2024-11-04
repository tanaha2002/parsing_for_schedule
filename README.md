### Requirements
- python 3.8+
### Problem Definition
#### Assumptions:
- All user using a same time zone
- The meeting will only init in workday (from Monday to Friday)
- The scheduler is only for this week.
- If they don't tell except day, assumptions they free from Monday to Friday. (that mean initilaze is Available from Monday to Friday).


### Analyze and Code
- Using the divide and conquer method, break this problem down into the simplest possible subproblems. I will break it to:
    #### Split messenges
    
     - Each messenges will fall into 1 in 2 case:
        - Messenges can devide into 2 part:
            - One is "available".
            - The other be "exception" ( assuming exception can be on of two value: (exception, prefer))
            - The "exception" can be appear before or after "available".
        - Messenge is single sentence:
            - This sentence can only be "available" or an Exception (assuming exception can be either "except" or "prefer").
        #### Example:
            [IMG_0012]
        #### Method:
        - Build a subset of word for split messenges. For split word:
        - Build a subset of word negative and prefer for classify the split sentence is "exception" or "available" or "prefer":
    #### Day extraction
    
    - Extract the workday in `available_sentence`, `exception_sentence`, `prefer_sentence` by loop these messenge in a list of `['monday', 'tuesday', 'wednesday', 'thursday', 'friday']` to extract.

    #### Time extraction 
    
    - Extract time in `available_sentence`, `exception_sentence`, `prefer_sentence`.
        #### Condition for time
        - the meeting is atleast 1 hours.
        - Morning: 7 AM to 11 AM
        - Afternoon: 1 PM to 5 PM
        - For available days:
            - From X AM to Y AM: From X to Y (7 <= X < Y <= 11)
            - From X PM to Y PM: From X to Y (1 <= X < Y <= 5)
            - From X AM to Y PM: From X to 11, 1 to Y (7 <= X < 11,  1 < Y <= 5 ).
            - After X AM: From X to 11, 1 to 5 (7 <= X < 11)
            - Afer X PM: From X to 5 (1 <= X < 5)
            - Before/Till/Untill X AM: From 7 to X (7 < X <= 11)
            - Before/Till/Untill X PM: 7 to 11, 1 to X (1 < X <= 5)

        - For unavailable days:
            - From X AM to Y AM: 7 to X and Y to 11, 1 to 5 (7 < X < Y < 11)
            - From X PM to Y PM: 7 to 11, 1 to X and Y to 5 (1 < X < Y < 5)
            - From X AM to Y PM: From 7 to X, Y to 5 (7 < X <= 11, 1 <= Y < 5)
            - After X AM: 7 to X (7 < X <= 11)
            - After X PM: 7 to 11, 1 to X (1 < X <= 5)
            - Before/Till/Untill X AM: X to 11, 1 to 5 ( 7 <= X < 11)
            - Before/Till/Untill X PM: X to 5 (1 <= X < 5)
        
        #### Example:
        
        Available Time Examples:
        ```
        1. "From X AM to Y AM" (7 ≤ X < Y ≤ 11)
        - Example: "I am free on Monday from 8 AM to 10 AM"
        - Available time slots: 8 to 10 on Monday

        2. "From X PM to Y PM" (1 ≤ X < Y ≤ 5)
        - Example: "I am available on Thursday from 2 PM to 4 PM" 
        - Available time slots: 2 to 4 on Thursday
        ```
        Unavailable Time Examples: 
        ```
        1. "From X AM to Y AM" (7 < X < Y < 11)
        - Example: "I am busy on Tuesday from 8 AM to 10 AM"
        - Available time slots: 7 to 8, 10 to 11, 1 to 5 on Tuesday

        2. "From X PM to Y PM" (1 < X < Y < 5)
        - Example: "I have a meeting on Wednesday from 2 PM to 4 PM"
        - Available time slots: 7 to 11, 1 to 2, 4 to 5 on Wednesday
        ```
    - Pattern define for extract time:
        ```
        r'(\d{1,2}) (am|pm) to (\d{1,2}) (am|pm)',    # From X AM/PM to Y AM/PM
        r'(\d{1,2}) to (\d{1,2}) (am|pm)',            # From X to Y AM/PM         
        r'after (\d{1,2}) (am|pm)',                   # After X AM/PM
        r'before (\d{1,2}) (am|pm)',                  # Before X AM/PM
        r'until (\d{1,2}) (am|pm)',                   # Until X AM/PM
        r'till (\d{1,2}) (am|pm)',                    # Till X AM/PM
        r'(morning|afternoon)'                        # Morning or afternoon
        ```
    #### Create a schedule
    
    - After we can find `available day`, `available time`, we can create a schedule base on overlapping of each user messenge.
    
    
### Full flow example
- Create each python script cover the logic I were analyze above.
    - Split messenge:
        ```
        # Example
        Message: I already have a meeting booked on Friday from 2 to 4 PM.
        Available_part: None
        Exception_part: i already have a meeting booked on friday from 2 to 4 pm.
        Preference_part: None
        ```
    - Day extraction:
        ```
        Message: I already have a meeting booked on Friday from 2 to 4 PM.
        Available_part: None
        Exception_part: i already have a meeting booked on friday from 2 to 4 pm.
        Preference_part: None
        Available days: ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        Unavailable days: ['friday']

    - Time extraction:
        ```
        Message: I already have a meeting booked on Friday from 2 to 4 PM.
        Available_part: None
        Exception_part: i already have a meeting booked on friday from 2 to 4 pm.
        Preference_part: None
        Available days: ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        Unavailable days: ['friday']
        Time available: [[(7, 11), (13, 17)], [(7, 11), (13, 17)], [(7, 11), (13, 17)], [(7, 11), (13, 17)], [(7, 11), (13, 14), (16, 17)]]
        Time available in unavailable days: [[(7, 11), (13, 14), (16, 17)]]
        ```
### Usage
#### Interactive app
- Go to `/src/` and run the `main.py` file for interactive app.
    - Input num of user
    - For each user, input the messenges, the detail extract for each user will appear after you hit enter.
#### Test
- Go to `/src` and open file `test.py`. Edit messenges you want test from `list_test` variable. Then run the `test.py` file via terminal to see the extraction and available schedule.

#### Demo

    

