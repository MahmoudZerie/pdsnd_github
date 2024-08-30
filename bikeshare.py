import time
import pandas as pd
import numpy as np

CITY_DATA = { 
    'chicago': '/mnt/data/chicago.csv',
    'new york city': '/mnt/data/new_york_city.csv',
    'washington': '/mnt/data/washington.csv'
}

def get_user_input(prompt, valid_options):
    """Gets and validates user input."""
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input
        else:
            print(f"Invalid input. Please enter one of the following: {', '.join(valid_options)}")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.`
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city = get_user_input('Would you like to see data for Chicago, New York City, or Washington? ', CITY_DATA.keys())
    month = get_user_input('Which month? January, February, March, April, May, June, or "all"? ', 
                            ['january', 'february', 'march', 'april', 'may', 'june', 'all'])
    day = get_user_input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or "all"? ', 
                          ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'])

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
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print(f'Most Common Month: {common_month}')

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print(f'Most Common Day of Week: {common_day}')

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print(f'Most Common Start Hour: {common_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station, end station, and combination trip
    common_start_station = df['Start Station'].mode()[0]
    common_end_station = df['End Station'].mode()[0]
    df['Start-End Combination'] = df['Start Station'] + " to " + df['End Station']
    common_trip = df['Start-End Combination'].mode()[0]

    print(f'Most Commonly Used Start Station: {common_start_station}')
    print(f'Most Commonly Used End Station: {common_end_station}')
    print(f'Most Common Trip: {common_trip}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f'Total Travel Time: {total_travel_time} seconds')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f'Mean Travel Time: {mean_travel_time} seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f'User Types:\n{user_types}')

    # Display counts of gender (only available for NYC and Chicago)
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        print(f'\nGender Distribution:\n{genders}')

    # Display earliest, most recent, and most common year of birth (only available for NYC and Chicago)
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f'\nEarliest Year of Birth: {earliest_year}')
        print(f'Most Recent Year of Birth: {most_recent_year}')
        print(f'Most Common Year of Birth: {common_year}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays raw data upon request by the user."""
    row_index = 0
    display_raw = input('Would you like to see 5 lines of raw data? Enter yes or no: ').strip().lower()
    
    while display_raw == 'yes':
        print(df.iloc[row_index:row_index + 5])
        row_index += 5
        display_raw = input('Would you like to see 5 more lines of raw data? Enter yes or no: ').strip().lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no: ').strip().lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()
