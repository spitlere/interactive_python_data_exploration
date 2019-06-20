import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # initialize the variables
    city = " "
    month = " "
    day = " "
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York, or Washington?\n')
        cities = ['chicago', 'new york', 'washington']
        if city.lower() in cities:
            city = city.lower()
            break
        else:
            print('Please try entering a city again.\n')
    print('You selected ' + city.title())
    # lets user choose between month, day, or no time filter
    while True:
        filter = input('Would you like to filter the data by month, day, or not at all? Type "none" for no time filter.\n')
        filters =  ['month', 'day', 'none']
        if filter.lower() in filters:
            filter = filter.lower()
            break
        else:
            print('Please try entering a filter again.')
    print('\nYou selected to filter by '+ filter)

    # lets user select month
    if filter == 'month':
        while True:
            month = input('Please enter the full name of the month for which you would like to see bikeshare data.\n')
            months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
            if month.lower() in months:
                month = month.lower()
                print('\nYou selected ' + month.title())
                break
            else:
                print('Please try entering a month again.\n')
    # lets user select day
    elif filter == 'day':
        while True:
            day = input('Please enter the full name of the day of the week for which you would like to see bikeshare data.\n')
            days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            if day.lower() in days:
                print('\n You selected ' + day.title())
                day = day.lower()
                break
            else:
                print('Please try entering a day again.\n')
    else:
        month == 'all'
        day == 'all'
        print('')
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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    df['And'] = ' & '
    # create a new column of concatenated Start and End Stations so we can find the most common combination
    df['StartEnd'] = df[['Start Station', 'And', 'End Station']].apply(lambda x: ''.join(x), axis=1)

    # drop rows with missing values
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most common month: ')
    print(df['month'].mode()[0])

    # display the most common day of week
    print('Most common day: ')
    print(df['day'].mode()[0])

    # display the most common start hour
    print('Most common start hour: ')
    print(df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most common start station: ')
    print(df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most common end station: ')
    print(df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print('Most frequent combination of start and end station: ')
    # calculates mode of the column we created in load_data
    print(df['StartEnd'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time: ')
    print(df['Trip Duration'].sum())

    # display mean travel time
    print('Average travel time: ')
    print(df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of user types: ')
    print(df['User Type'].value_counts())

    # Display counts of gender and handle Washington.csv missing gender column
    if 'Gender' in df.columns:
        print('Counts of gender: ')
        print(df['Gender'].value_counts())
    else:
        print('No Gender Data Available.\n')

    # Display earliest, most recent, and most common year of birth and handle Washington.csv missing gender column
    #earliest year of birth
    if 'Birth Year' in df.columns:
        print('Earliest birth year: ')
        print(df['Birth Year'].min())
        #most recent year of birth
        print('Most recent birth year: ')
        print(df['Birth Year'].max())
        #most common year of birth
        print('Most common birth year: ')
        print(df['Birth Year'].mode()[0])
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    else:
        print('No Birth Year Data Available.\n')

# ask users if they want to view the raw data
def raw_data(df):
    # set terminal size so dataframe will display
    pd.set_option('max_columns', 13)
    # initialize user_input
    user_input = " "
    user_input_next = " "
    user_input_last = " "
    # get user_input
    while True:
        user_input = input('Would you like to view the raw data from the above analysis?\n')
        if user_input.lower() == 'yes':
            print(df.head())
            # initialize row counter so next loop can add to it to get row numbers for iloc
            first_row = 5
            last_row = 10
            # ask user if they want to view next 5 rows
            while True:
                user_input_next = input('Would you like to view the next 5 rows in the data?\n')
                if user_input_next.lower() == 'yes':
                    print(df.iloc[first_row:last_row, 2:13])
                    first_row +=5
                    last_row +=5
                    while True:
                        user_input_last = input('Would you like to view the next 5 rows in the data?\n')
                        if user_input_last == 'yes':
                            print(df.iloc[first_row:last_row, 2:13])
                            first_row +=5
                            last_row +=5
                        elif user_input_last == 'no':
                            break
                elif user_input_last == 'no':
                    break
                elif user_input_next.lower() == 'no':
                    break
                else:
                    print("Please enter a response, 'yes' or 'no'.\n")
        elif user_input.lower() == 'no':
            break
        else:
            print("Please enter a response, 'yes' or 'no'.\n")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
