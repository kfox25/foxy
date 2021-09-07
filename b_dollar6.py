### Bottom Dollar is a financial phone app that displays the amount your savings is increasing in real-time. 
### It subtracts your monthly expenses from your monthly take-home pay to arrive at a monthly, net savings.
### It then displays that savings in real-time by the second, minute, hour or day.
### Having this information at hand is meant to provide positive feedback on your progress and 
### encourage thought on opportunities to decrease your monthly expenses.
### In the future, this app will use a link to the your checking account to pull credits and debits
### which will yield a more accurate rolling, net-savings.

import time
import calendar
from datetime import date, datetime


### get the total number of days in the current month
month = datetime.now().month
year = datetime.now().year
days_in_current_month = calendar.monthrange(year, month)[1]


## get the number of WORKDAYS in the current month
workdays_in_current_month = 0
for x in range(days_in_current_month):
    if date(year, month, x+1).weekday() in range(0,5):
        workdays_in_current_month +=1


### functions to catch bad input
def check_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print('Entry must be an integer.')
            continue
        break
    return value

def check_y_or_n(prompt):
    while True:
        value = input(prompt)
        if value.upper() in ['Y','N']:
            value = value.upper()
            break
        else:
            print('Entry must be "Y" or "N".')
    return value

def check_rep_pref(prompt):
    while True:
        value = input(prompt)
        if value.upper() in ['D','H','M','S']:
            value = value.upper()
            break
        else:
            print('Entry must be "D", "H", "M", or "S".')
    return value


## get user input on dollars and preference and run them through cleaning functions.
starting_balance = check_integer('Enter your balance as of today: ')
monthly_takehome = check_integer('Enter your monthly takehome pay: ')
monthly_expenses = check_integer('Enter the total of your monthly expenses: ')
work_pref = check_y_or_n('Do you want calculations restricted to workdays/workhours? Y/N:')
report_pref = check_rep_pref('Do you want to increment by (D)ays, (H)ours, (M)inutes, or (S)econds?: ')


### breakdown monthly net into smaller amounts
monthly_net = monthly_takehome - monthly_expenses
net_day = monthly_net / days_in_current_month
net_hour = net_day / 24
#if work days/hours
if work_pref == 'Y':
    net_day = monthly_net / workdays_in_current_month
    net_hour = net_day / 8
# if NOT work days/hours    
net_min = net_hour / 60
net_sec = net_min / 60


### ticker
x = starting_balance
while True:
    if report_pref == 'D':
        incrmt_str, increase_save, slp = 'day', net_day, 1 #8640
    elif report_pref =='H':
        incrmt_str, increase_save, slp = 'hour', net_hour, 1 #360
    elif report_pref == 'M':
        incrmt_str, increase_save, slp = 'minute', net_min, 1, #60
    elif report_pref == 'S':
        incrmt_str, increase_save, slp = 'second', net_sec, 1
    else:
        print('Something has gone wrong')
        break

    print('Your Bottom Dollar by', incrmt_str, 'is:', '{:.2f}'.format(starting_balance))
    starting_balance += increase_save
    time.sleep(slp) 



# todo
# x try-except to handle bad user input and other issues (0 for beginning balance)
# * should app just display during working hours and working days. 
#   The increment can be discouraging if it is spread over every hour and every day.
# x I will need to calculate the number of workdays in the current month.
# * Is monthrange() the best way to get the number of days in the current month?
# * Is it better to use date or datetime to get arguments for monthrange()?
# * Does Python/VS code have an automated testing module that handles user input.
# * How to play a tone using just python?
# x Do I wrap up the input lines in a function?
# * How do I get the ticker to only run between 8 and 5?
