import time
import pandas as pd
import numpy as np
import json


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = ['chicago', 'washington', 'new york']

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

def get_city():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hey there! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Please select a city you want to explore: Chicago, Washington, or New York? ').lower()
        if city in CITIES:
            print('\nYou selected {}.\n'.format(city))
            break
        else:
            print('ERROR! PLEASE ONLY SELECT A CITY LISTED ABOVE.')
    return city


def get_filters():

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Great! Now it\'s time to select a month name '\
                        'or just select \'all\' to apply no month filter. \n(e.g. all, January, February, March, April, May, June) \n> ').lower()
        if month in MONTHS:
            print('\nYou selected {}.\n'.format(month))
            break
        else:
            print('ERROR! PLEASE ONLY SELECT A MONTH IN THE LIST ABOVE.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('And lastly, could you select one day of the week you want to analyze?'\
                        ' You can select \'all\' again to apply no day filter. \n(e.g. all, Monday, Sunday) \n> ').lower()
        if day in DAYS:
            print('\nYou selected {}.\n'.format(day))
            break
        else:
            print('ERROR! PLEASE SELECT A CORRECT DAY OF THE WEEK.')

    print('-'*40)
    return month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.weekday_name
    df['Hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['Month'] == month]
    else:
        print('No Month filter was used')

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day of Week'] == day.title()]

    else:
        print('No Day filter was used')

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['Month'].value_counts().idxmax()
    print("The most common month is:", most_common_month)

    # display the most common day of week
    most_common_day_of_week = df['Day of Week'].value_counts().idxmax()
    print("The most common day of week is:", most_common_day_of_week)

    # display the most common start hour
    most_common_start_hour = df['Hour'].value_counts().idxmax()
    print("The most common start hour is:", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station:", most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station:", most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_common_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most commonly used start station and end station: {}, {}"\
          .format(most_common_start_end_station[0], most_common_start_end_station[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print("Total travel time:", total_travel)

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("Mean travel time :", mean_travel)

    # display max travel time
    max_travel = df['Trip Duration'].max()
    print("Max travel time:", max_travel)

    print("Travel time for each user type:\n")
    # display the total trip duration for each user type
    group_by_user_trip = df.groupby(['User Type']).sum()['Trip Duration']
    for index, user_trip in enumerate(group_by_user_trip):
        print("  {}: {}".format(group_by_user_trip.index[index], user_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(city):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    #"""Displays statistics on bikeshare users."""

    if city != 'washington':

        # Display counts of user types
        user_counts = df['User Type'].value_counts()
        print("\nCounts of User Types: \n", user_counts)

        # Display counts of gender
        gender_counts = df['Gender'].value_counts()
        print(gender_counts)

        # Display earliest, most recent, and most common year of birth
        birth_year = df['Birth Year']

        # the most common birth year
        most_common_year = birth_year.value_counts().idxmax()
        print("The most common Birth Year:", most_common_year)

        # the most recent birth year
        most_recent = birth_year.max()
        print("The most recent Birth Year:", most_recent)

        # the most earliest birth year
        earliest_year = birth_year.min()
        print("The most earliest Birth Year:", earliest_year)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    else:
        print('No Gender or Birth Year columns found in Washington')

def display_raw_data(df):
    """Displays raw bikeshare data."""
    row_length = df.shape[0]

    # iterate from 0 to 5
    for i in range(0, row_length, 5):
        raw_data = input('\nWould you like to review the raw data? Type \'yes\' or \'no\'\n> ')
        if raw_data.lower() == 'no':
            break

        # receive then convert data to json
        # split each json row data
        row_data = df.iloc[i: i + 5].to_json(orient='records', lines=True).split('\n')
        for row in row_data:
            # pretty print each user data
            analyze_row = json.loads(row)
            json_row = json.dumps(analyze_row, indent=2)
            print(json_row)

def main():
    while True:
        city = get_city()
        month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter Yes or No.\n')
        if restart.lower() == 'yes':
            city = get_city()
            month, day = get_filters()
            df = load_data(city, month, day)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(city)
            break
        elif restart.lower() == 'no':
            break
        else:
            print('Error. Please choose to either restart or not.')

if __name__ == "__main__":
	city = main()
