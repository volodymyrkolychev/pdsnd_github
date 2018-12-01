import datetime
import pandas as pd
import numpy as np

print("Welcome to the Bikeshare Analysis Program.")

def prepare_data():

    """ This function does not take in any data but instead offers the user several options and then returns these options.
    These are used later in the calculate function of the program. """

    city_name, sort_type, month, day = '','','',''

    while city_name.title() not in ["Chicago", "New York", "Newyork", "Washington"]:
        city_name = input("\nPlease select a city from Chicago, New York or Washington: ")
        
        if city_name.title() == 'Chicago':
            city_file_name = 'chicago.csv'
        elif city_name.title() == 'New York' or city_name.title() == 'Newyork':
            city_file_name = 'new_york_city.csv'
        elif city_name.title() == 'Washington':
            city_file_name = 'washington.csv'
        else:
            print("That is not an option. Try again.")

    while sort_type.lower() not in ['month', 'day', 'neither']:
        sort_type = input("\nPlease select a sorting option: month, day or neither: ")         
        if sort_type.lower() == 'month':
            sort_option = 'm'
        elif sort_type.lower() == 'day':
            sort_option = 'd'
        elif sort_type.lower() == 'neither':
            sort_option = 'n'
        else: 
            print("That is not an option. Try again.")

    if sort_option == 'm':
        month = ''
        day_selected = None
        month_options = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6}
        while month.title() not in month_options.keys():
            month = input("\nPlease select a 3 letter month code: Jan, Feb, Mar, Apr, May or Jun: ").title()
            month_selected = month_options.get(month)
            if month_selected is None:
                print("That is not an option. Try again.")

    if sort_option == 'd':
        day = ''
        month_selected = None
        day_options = {'Mon':1, 'Tue':2, 'Wed':3, 'Thu':4, 'Fri':5, 'Sat':6, 'Sun':0}
        while day.title() not in day_options.keys():
            day = input("\nPlease select a 3 letter day code: Mon, Tue, Wed, Thu, Fri, Sat or Sun: ").title()
            day_selected = day_options.get(day)
            if day_selected is None:
                print("That is not an option. Try again.")

    if sort_option == 'n':
        month_selected = None
        day_selected = None

    return city_file_name, month_selected, day_selected



def calculate(city_file_name, month_selected, day_selected):

    """ This function takes in the City File Name, month by which to sort(if any) and day by which to sort (if any) and then
    creates a dataframe with these parameters. The function then parses this dataframe providing input. This function has
    several loops to avoid asking for data that does not exist, such as gender data for Washington among others. """
    
    df = pd.read_csv(city_file_name, parse_dates = ['Start Time', 'End Time'])
    
    df['Trip'] = df['Start Station'].str.cat(df['End Station'], sep = ' to ')
    if month_selected is not None:
        df = df[df['Start Time'].dt.month == month_selected]
    if day_selected is not None:
        df = df[df['Start Time'].dt.dayofweek == day_selected]

    if month_selected is None:
        month_index = {'1':'January', '2':'February', '3':'March', '4':'April', '5':'May', '6':'June'}
        print('The most popular month is: ' + month_index[str(df['Start Time'].dt.month.mode().values[0])])

    if day_selected is None:
        day_index = {'1':'Mon', '2':'Tue', '3':'Wed', '4':'Thu', '5':'Fri', '6':'Sat', '0':'Sun'}
        print('The most popular day is: ' + day_index[str(df['Start Time'].dt.dayofweek.mode().values[0])])

    print('The most popular hour is: ' + df['Start Time'].dt.hour.mode().to_string(index = False))
    print('The most popular start station is: ' + df['Start Station'].mode().to_string(index = False))
    print('The most popular end station is: ' + df['End Station'].mode().to_string(index = False))
    print('The most popular trip is: ' + df['Trip'].mode().to_string(index = False))
    print('The total trip duration of ALL customers is: ' +  str(datetime.timedelta(seconds = int((df['Trip Duration'].sum())))) + ' hours, minutes, seconds')
    print('The average trip duration of ALL customers is: ' +  str(datetime.timedelta(seconds = int((df['Trip Duration'].mean())))) + ' hours, minutes, seconds')
    subscribers = df[df["User Type"] == "Subscriber"]["User Type"].count()
    customers = df[df["User Type"] == "Customer"]["User Type"].count()
    print('There are ' + str(subscribers) + ' subscribers and ' + str(customers) + ' customers.')

    if city_file_name == "chicago.csv" or city_file_name == "new_york_city.csv": #this data is unique to dataframes created from       
        #chicago and New York City csv files only
        males = df[df["Gender"] == "Male"]["Gender"].count()
        females = df[df["Gender"] == "Female"]["Gender"].count()           
        oldest_user = int(df['Birth Year'].min())
        youngest_user = int(df['Birth Year'].max())
        average_birth_year = int(df['Birth Year'].mode())
        print('There are ' + str(males) + ' males and ' + str(females) + ' females.')
        print('The youngest and oldest customers were born in ' + str(youngest_user) + ' and ' + str(oldest_user) + ' respectively.')
        print("The average birth year for your selected sample is: " + str(average_birth_year) + ".")

    display_5_lines(df)

def display_5_lines(df):
    
    """Takes the Dataframe we set up in the function calculate and offers the user the option to print 5 lines of trip data. """

    head = 0
    tail = 5
    show_options = 0
    while show_options == 0:    
        user_option = input("Would you like to see trip data? Type Y for yes, anything else to quit: ").title()
        if user_option == 'Y':
            print(df[df.columns[0:-1]].iloc[head:tail])
            head += 5
            tail += 5
        else:
            print("Thank you for using the Bikeshare Analysis Program!")
            exit()

city_file_name, month_selected, day_selected = prepare_data() #assigns values to these variables returned bythe function prepare_data()

calculate(city_file_name, month_selected, day_selected) #calls the function calculate with the following variables




