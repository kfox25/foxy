### Bottom Dollar is a financial phone app that displays the amount your savings is increasing in real-time. 
### It subtracts your monthly expenses from your monthly take-home pay to arrive at a monthly, net-savings amount.
### It then displays that savings in real-time by the second, minute, hour or day.
### Having this information at hand is meant to provide positive feedback on your savings progress and 
### encourage thought on opportunities to decrease your monthly expenses.
### In the future, this app will use a link to your checking account to pull credits and debits
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


### functions to check
def check_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print('Entry must be an integer.')
            continue
        break
    return value

def check_time_2400(prompt):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print('Entry must be an integer.')
            continue
            
        if value >= 0 and value < 2400:
            break
        else:
            print('Entry must be between 0 and 2400.')
            continue    
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

def check_report_pref(prompt):
    while True:
        value = input(prompt)
        if value.upper() in ['D','H','M','S']:
            value = value.upper()
            break
        else:
            print('Entry must be "D", "H", "M", or "S".')
    return value


## get user input on financials and reporting preference and run them through checking functions.
starting_balance = check_integer('Enter your balance as of today: ')
monthly_takehome = check_integer('Enter your monthly takehome pay: ')
monthly_expenses = check_integer('Enter the total of your monthly expenses: ')
work_pref = check_y_or_n('Do you want calculations restricted to workdays/workhours? Y/N: ')
if work_pref == 'Y':
    day_start = check_time_2400('What time does your workday start? 830 = 8:30AM: ')
    day_end = check_time_2400('What time does your workday end? 1730 = 5:30PM: ')
report_pref = check_report_pref('Do you want to increment by (D)ays, (H)ours, (M)inutes, or (S)econds?: ')


### breakdown monthly net into smaller amounts
monthly_net = monthly_takehome - monthly_expenses
net_day = monthly_net / days_in_current_month
net_hour = net_day / 24
#if work days/hours
if work_pref == 'Y':
    net_day = monthly_net / workdays_in_current_month
    net_hour = net_day / 8  
net_min = net_hour / 60
net_sec = net_min / 60


### ticker
global position
position = starting_balance
while True:

    #cast preferences, sleep is set to 1 second for all of them
    if report_pref == 'D':
        incrmt_str, increase_save, slp = 'day', net_day, 1 #86400
    elif report_pref =='H':
        incrmt_str, increase_save, slp = 'hour', net_hour, 3600
    elif report_pref == 'M':
        incrmt_str, increase_save, slp = 'minute', net_min, 60
    elif report_pref == 'S':
        incrmt_str, increase_save, slp = 'second', net_sec, 1
    else:
        print('Something has gone wrong.')
        break

    #get current time  
    def now_time():
        x = datetime.now().time()
        x = str(x)
        x = x[0:5]
        x = x.replace(':','')
        x = int(x)
        return x

    ## control flow for workdays/hours
    if work_pref == 'Y':
        while day_start <= now_time() < day_end and date.today().weekday() in [1,2,3,4,5]:
            print('Your Bottom Dollar by', incrmt_str, 'is:', '${:.2f}'.format(position))
            position += increase_save
            time.sleep(slp) 

    else:
        while True:
            print('Your Bottom Dollar by', incrmt_str, 'is:', '${:.2f}'.format(position))
            position += increase_save
            time.sleep(slp) 

# TO-DO/QUESTIONS
# * Use user input start time and end time to adjust net calc.
# * How to play a tone using just python?
# * Which blocks of script need to be inside of the Ticker, while loop?
# * Is monthrange() the best way to get the number of days in the current month?
# * Is it better to use date or datetime to get arguments for monthrange()?
# * Does Python/VS code have an automated testing module that handles user input.
