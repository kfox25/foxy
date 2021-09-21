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

def main():

    ### functions to check user input
    def check_integer(prompt):
        """Validate the user has entered an integer"""
        while True:
            value = input(prompt)
            if value.isdecimal():
                return int(value)
            else:
                print('Entry must be a positive integer.')

    def check_time_2400(prompt):
        """Validate the user has entered an integer that represents military time"""
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
        """Validate the user has entered a y or n"""
        while True:
            value = input(prompt).casefold()
            if value == 'y':            
                return True
            elif value == 'n':
                return False
            else:
                print('Entry must be "Y" or "N".')

    def check_report_pref(prompt):
        """Validate the user has entered a D, H, M, or S"""
        while True:
            value = input(prompt).casefold()
            if value in ['d','h','m','s']:
                return value
            else:
                print('Entry must be "D", "H", "M", or "S".')


    ### Helper functions
    def curr_time():
        """get current time and convert to 4 digit integer. 12:30:23.12... to 1230"""
        curr_time = datetime.now().time()
        curr_time = str(curr_time)[0:5]
        curr_time = int(curr_time.replace(':',''))
        return curr_time

    def curr_month():
        """get current month as integer"""
        return datetime.now().month

    def curr_year():   
        """get current year as integer"""
        return datetime.now().year 

    def days_in_current_month():
        """get the total number of days in the current month"""
        return calendar.monthrange(curr_year(), curr_month())[1]

    def workdays_in_current_month():
        """gets the number of WORKDAYS in the current month"""
        workdays_in_current_month = 0
        for x in range(days_in_current_month()):
            if date(curr_year(), curr_month(), x+1).weekday() in range(0,5):
                workdays_in_current_month +=1
        return workdays_in_current_month
        
    def base_60_to_100(time_from_input):
        """Converts the last two digits of user input of military time to decimal.
            ex. 1730 to 17.50. That is, 17 hours and 30 minutes to 17.5 hours
            """
        hours = str(time_from_input)[:-2]
        minutes = str(time_from_input)[-2:]
        minutes = str(int(int(minutes) * (5/3)))
        minutes = minutes.zfill(2)
        time_as_float = int(hours + minutes) /100
        return time_as_float

    def work_day_duration():
        """Takes the users workday start and end times and returns the length of the users workday"""
        return base_60_to_100(day_end) - base_60_to_100(day_start)


    """Get user input on financial data and reporting preference and run them through checking functions."""
    starting_balance = check_integer('Enter your balance as of today: ')
    monthly_takehome = check_integer('Enter your monthly takehome pay: ')
    monthly_expenses = check_integer('Enter the total of your monthly expenses: ')
    work_pref = check_y_or_n('Do you want calculations restricted to workdays/workhours? Y/N: ')
    if work_pref:
        day_start = check_time_2400('What time does your workday start? 8:30AM = 830: ')
        day_end = check_time_2400('What time does your workday end? 5:30PM = 1730: ')
    report_pref = check_report_pref('Do you want to increment by (D)ays, (H)ours, (M)inutes, or (S)econds?: ')


    """Breakdown monthly net into smaller amounts"""
    monthly_net = monthly_takehome - monthly_expenses
    net_day = monthly_net / days_in_current_month()
    net_hour = net_day / 24
    # if work days/hours
    if work_pref:
        net_day = monthly_net / workdays_in_current_month()
        net_hour = net_day / work_day_duration() 
    net_min = net_hour / 60
    net_sec = net_min / 60


    def ticker():
        """This function runs continuously. It displays the current position as it increases."""
        global position
        position = starting_balance

        """Tuple assignment containing the variables to be used in the subsequent while loop.
            ([0]duration string for formatted output, [1]net savings amount to add to each increment, [2]sleep duration)
            """
        if report_pref == 'd':
            prefs = ('day', net_day, 1) #86400, 1 for testing.
        elif report_pref =='h':
            prefs = ('hour', net_hour, 1) #3600, 1 for testing.
        elif report_pref == 'm':
            prefs = ('minute', net_min, 1) #60, 1 for testing.
        elif report_pref == 's':
            prefs = ('second', net_sec, 1)

        while True:
            """This while loop displays the total position as it increases by the time-frame the user has specified"""
            if work_pref:
                while day_start <= curr_time() <= day_end and date.today().weekday() in [0,1,2,3,4]:
                    print('Your Bottom Dollar by', prefs[0], 'is:', '${:,.2f}'.format(position))
                    position += prefs[1]
                    time.sleep(prefs[2]) 
            else:
                while True:
                    print('Your Bottom Dollar by', prefs[0], 'is:', '${:,.2f}'.format(position))
                    position += prefs[1]
                    time.sleep(prefs[2]) 
    ticker()


if __name__=='__main__':
    main()

# TO-DO/QUESTIONS
# * Which sections do I wrap up into Main()? Phil?!
# * If I throw all the data collection statements into a function, whats the best way to get them out?
#   Tuple, dictionary, declare globals?

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