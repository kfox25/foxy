#######################################################################################################################
###                                      YOU CAN BET YOUR BOTTOM DOLLAR!                                            ###
###                                                                                                                 ###
###  Bottom Dollar is a financial phone app that displays the amount your savings is increasing in real-time.       ###
###  It subtracts your monthly expenses from your monthly take-home pay to arrive at a monthly, net-savings amount. ###
###  It then displays that savings in real-time as it accrues by the second, minute, hour or day.                   ###
###  Having this information at hand is meant to provide positive feedback on your savings' progress and            ###
###  encourage thought on opportunities to decrease your monthly expenses.                                          ###
###  In the future, this app will use a link to your checking account to pull credits and debits                    ###
###  which will yield a more accurate rolling, net-savings.                                                         ###
###                                                                                                                 ###
#######################################################################################################################


import time
import calendar
from datetime import date, datetime


### functions to check user input
def check_integer(prompt):
    while True:
        value = input(prompt)
        if value.isdecimal():
            return int(value)
        else:
            print('Entry must be a positive integer.')

def check_time_2400(prompt):
    while True:
        value = input(prompt)
        if value.isdecimal():
            if int(value) <= 2400:
                if int(value[-2:]) < 60:
                    return int(value)
                else:
                    print('Minutes must be less than 60.')  
            else:
                print('Entry must be less than 2400.')              
        else:
            print('Entry must be a positive integer.')

def check_y_or_n(prompt):
    while True:
        value = input(prompt).casefold()
        if value == 'y':            
            return True
        elif value == 'n':
            return False
        else:
            print('Entry must be "Y" or "N".')

def check_report_pref(prompt):
    while True:
        value = input(prompt).casefold()
        if value in ['d','h','m','s']:
            return value
        else:
            print('Entry must be "D", "H", "M", or "S".')


### get user input on financials and reporting preference and run them through checking functions.
starting_balance = check_integer('Enter your balance as of today: ')
monthly_takehome = check_integer('Enter your monthly takehome pay: ')
monthly_expenses = check_integer('Enter the total of your monthly expenses: ')
work_pref = check_y_or_n('Do you want calculations restricted to workdays/workhours? Y/N: ')
if work_pref:
    day_start = check_time_2400('What time does your workday start? 8:30AM = 830: ')
    day_end = check_time_2400('What time does your workday end? 5:30PM = 1730: ')
report_pref = check_report_pref('Do you want to increment by (D)ays, (H)ours, (M)inutes, or (S)econds?: ')


### get the total number of days in the current month
month = datetime.now().month
year = datetime.now().year
days_in_current_month = calendar.monthrange(year, month)[1]


### get the number of WORKDAYS in the current month
workdays_in_current_month = 0
for x in range(days_in_current_month):
    if date(year, month, x+1).weekday() in range(0,5):
        workdays_in_current_month +=1


### get duration of workday to use to calculate net hour amount
def base_60_to_100(time_from_input):
    hours = str(time_from_input)[:-2]
    minutes = str(time_from_input)[-2:]
    minutes = str(int(int(minutes) * (5/3)))
    minutes = minutes.zfill(2)
    hour_min = int(hours + minutes) /100
    return hour_min

if work_pref:
    work_day_duration = base_60_to_100(day_end) - base_60_to_100(day_start)


### breakdown monthly net into smaller amounts
monthly_net = monthly_takehome - monthly_expenses
net_day = monthly_net / days_in_current_month
net_hour = net_day / 24
# if work days/hours
if work_pref:
    net_day = monthly_net / workdays_in_current_month
    net_hour = net_day / work_day_duration  
net_min = net_hour / 60
net_sec = net_min / 60


### ticker
global position
position = starting_balance
while True:

    # cast preferences
    # Set slp to 1 for testing
    if report_pref == 'd':
        incrmt_str, saved_amt, sleep_dur = 'day', net_day, 1 #86400
    elif report_pref =='h':
        incrmt_str, saved_amt, sleep_dur = 'hour', net_hour, 1 #3600
    elif report_pref == 'm':
        incrmt_str, saved_amt, sleep_dur = 'minute', net_min, 1 #60
    elif report_pref == 's':
        incrmt_str, saved_amt, sleep_dur = 'second', net_sec, 1
    else:
        print('Something has gone wrong.')
        break

    # get current time  
    def now_time():
        ntime = datetime.now().time()
        ntime = str(ntime)[0:5]
        ntime = int(ntime.replace(':',''))
        return ntime

    # control flow for workdays/hours
    if work_pref:
        while day_start <= now_time() <= day_end and date.today().weekday() in [0,1,2,3,4,5]:
            print('Your Bottom Dollar by', incrmt_str, 'is:', '${:,.2f}'.format(position))
            position += saved_amt
            time.sleep(sleep_dur) 
    else:
        while True:
            print('Your Bottom Dollar by', incrmt_str, 'is:', '${:,.2f}'.format(position))
            position += saved_amt
            time.sleep(sleep_dur) 

# TO-DO/QUESTIONS
# * Which sections do I wrap up into Main()? Phil!?
# * For if statements using strings, should the strings always be lower case and utilize CASEFOLD() on input. 
# * Should a function return an integer as a int, float, or str. Styleguide?
# * How to play a tone using just python?
# * Which blocks of script need to be inside of the Ticker's while loop?
# * Is monthrange() the best way to get the number of days in the current month?
# * Is it better to use date or datetime to get arguments for monthrange()?
# * Does Python/VS code have an automated testing module that handles user input.
# * Is there one day a month when a checking account is more 'accurate' than other days? 


# * Should I put the checking functions into a class and run methods on prompts?

# class Check_it():
#     def __init__(self):
#         pass

#     def check_integer(self,prompt):
#         while True:
#             value = input(prompt)
#             if value.isdecimal():
#                 return int(value)
#             else:
#                 print('Entry must be a positive integer.')

# starting_balance = Check_it().check_integer('Enter an Integer: ')
# print(type(starting_balance), starting_balance)

#