import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
months = ['january', 'february', 'march', 'april', 'may', 'june']

def check_input(prompt,valid_items):
    """
    This function provides a while loop to allow user to correct spelling mistakes
    It also checks for input of 3 character common abbreviations
    Args:
        (str) prompt: string prompt to ask user what type of data to filter by
        (list) valid_items: list of valid days, months, or cities to choose from
    Returns: either an accepted day, month or city as "ret_obj" with str format
    """
    while True:
        ret_obj = input(prompt).lower()
        if ret_obj not in valid_items:
            for item in valid_items:
                if item[0:3]==ret_obj: #check for 3 character abbreviation input
                    ret_obj=item
                    print('Interpreting abbreviation as \'{}\'.\n'.format(ret_obj.title()))
                    break
            if ret_obj in valid_items:
                break
            print('Invalid entry. Check spelling and try again.\n')
        else:
            break
    return ret_obj

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    prompt = 'Please select a city to evaluate: (Chicago, New York City, Washinton) : '
    valid_items = ['chicago','new york city','washington']
    city = check_input(prompt,valid_items)

    # get user input for month (all, january, february, ... , june)
    prompt = 'Please select a month to evaluate: (January, February, March, April, May, June, or type \'all\' for no month filter) : '
    valid_items = months
    valid_items.append('all')
    month = check_input(prompt,valid_items)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    prompt = 'Please select a day to evaluate: (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or type \'all\' for no day filter) : '
    valid_items = days
    valid_items.append('all')
    day = check_input(prompt,valid_items)

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start and End Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])


    # extract month and day of week from Start Time to create new columns
    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    df['day_of_week'] = pd.DatetimeIndex(df['Start Time']).day_of_week
    #the day of the week with Monday=0, Sunday=6.

    #extract start hour as new column as well
    df['start_hour'] = pd.DatetimeIndex(df['Start Time']).hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe

        day = days.index(day)
        df = df[df['day_of_week']==day]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Common Month:', months[popular_month-1].title())

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Common Day of Week:', days[popular_day].title())

    # display the most common start hour
    popular_start_hour = df['start_hour'].mode()[0]
    print('Most Common Start Hour:', popular_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station:', popular_start_station.title())

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Common End Station:', popular_end_station.title())

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station']+" -> "+df['End Station']
    popular_trip = df['trip'].mode()[0]
    print('Most Common Combination of Start and End Stations:', popular_trip.title())



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration=df['Trip Duration'].sum() #total duration in seconds
    print('Total trip duration: {} seconds, or {}'.format(total_duration,datetime.timedelta(seconds=int(total_duration))))


    # display mean travel time
    avg_duration=df['Trip Duration'].mean() #total duration in seconds
    print('Average trip duration: {} seconds, or {}'.format(avg_duration,datetime.timedelta(seconds=int(avg_duration))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
        # Display counts of user types
        user_types = df['User Type'].value_counts()
        print('\nUser Types:\n{}'.format(user_types))
    except KeyError:
        print('\nNo User Type Data')
    
    try:
        # Display counts of gender
        genders = df['Gender'].value_counts()
        print('\nGender Counts:\n{}'.format(genders))
    except KeyError:
        print('\nNo Gender Data')

    try:
        # Display earliest, most recent, and most common year of birth
        by = df['Birth Year']
        print('\nEarliest birth year: {}\nMost recent birth year: {}\nMost common birth year: {}'.format(int(by.min()),int(by.max()),int(by.mode())))
    except:
        print('\nNo Birth Year Data')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
    
        i_max=int(df.count()[1])
      
        for i in range(0,i_max,5):
            #start at i=0, count in increments of 5, and end at max count of dataframe
            raw = input('\nWould you like to see the raw data? Enter yes or no.\n')
            if raw.lower() != 'yes':
                break
            print(df[i:i+5])
            #display only five rows of raw data at a time




        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
