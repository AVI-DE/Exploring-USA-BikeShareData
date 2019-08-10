import time
import pandas as pd
import numpy as np
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Creating list of the relevent cities, months and days to be used

feasible_cities     = [ "new york city", "chicago", "washington" ]
feasible_months     = [ "january", "february", "march", "april", "may", "june", "all" ]
feasible_days       = [ "monday", "tuesday", "wednesday", "thursday",
                        "friday", "saturday", "sunday", "all" ]

# Defining a function to validate the user input at runtime

def ask_user_selection(options, prompt_message):
    while True:
        answer = input(prompt_message).strip().lower()

        if answer in options:
            return answer

        print("Please enter one of the offered options.\n")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\n ---- Hello! Let\'s explore some US bikeshare data! ----\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = ask_user_selection(
            feasible_cities,
            "Please enter: 'new york city', 'chicago' or 'washington' > ")

    # TO DO: get user input for month (all, january, february, ... , june)
    month = ask_user_selection(
        feasible_months,
        "Please enter month: 'january', 'february', 'march', 'april', 'may', 'june' or 'all' > ")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ask_user_selection(
        feasible_days,
        "Please enter day: 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'or 'all' > ")

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
    df = pd.read_csv(CITY_DATA[city], index_col = 0)

    df['Start Time'] = pd.to_datetime(df['Start Time'])     # Casting "Start Time" to datetime.
    df["month"] = df['Start Time'].dt.month                 # Get the weekday out of the "Start Time"
    df["week_day"] = df['Start Time'].dt.weekday_name       # Month-part from "Start Time" value.
    df["start_hour"] = df['Start Time'].dt.hour             # Hour-part from "Start Time" value.
    df["start_end"] = df['Start Station'].astype(str) + ' to ' + df['End Station']

    if month != 'all':
        month_index = feasible_months.index(month) + 1      # Get the list-index of the month.
        df = df[df["month"] == month_index ]                # Establish a filter for month.

    if day != 'all':
        df = df[df["week_day"] == day.title() ]             # Establish a filter for week day.

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    month_index = df["month"].mode()[0] - 1
    most_common_month = feasible_months[month_index].title()

    print("Most common month: ", most_common_month)


    # TO DO: display the most common day of week
    most_common_day = df["week_day"].mode()[0]
    print("Most common day: ", most_common_day)

    # TO DO: display the most common start hour
    most_common_hour = df["start_hour"].mode()[0]
    print("Most common hour: ", most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_used_start = df['Start Station'].mode()[0]
    print("Most used start: ", most_used_start)

    # TO DO: display most commonly used end station
    most_used_end = df['End Station'].mode()[0]
    print("Most used end: ", most_used_end)

    # TO DO: display most frequent combination of start station and end station trip
    most_common_combination = df["start_end"].mode()[0]
    print("Most common used combination concerning start- and end-station: ",
            most_common_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print("Total time of travel in seconds: ", total_travel_time)

    # TO DO: display mean travel time
    average_time = df["Trip Duration"].mean()
    print("The average travel-time in seconds: ", average_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("Count of user types: ",
            df["User Type"].value_counts())

    # TO DO: Display counts of gender
    if "Gender" in df:
        print("\nCounts concerning client`s gender")
        print("Male persons: ", df.query("Gender == 'Male'").Gender.count())
        print("Female persons: ", df.query("Gender == 'Female'").Gender.count())

    # TO DO: Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        print("\nEarliest year of birth: ", df["Birth Year"].min())
        print("Most recent year of birth: ", df["Birth Year"].max())
        print("Most common year of birth: ", df["Birth Year"].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Defining a function to display the user raw data on request at runtime

def display_data(df):
    """Displays raw bikeshare data."""
    row_length = df.shape[0]

    # iterate from 0 to the number of rows in steps of 5
    for i in range(0, row_length, 5):

        yes = input('\nWould you like to examine the particular user trip data? Type \'yes\' or \'no\'\n> ')
        if yes.lower() != 'yes':
            break

        # retrieve and convert data to json format
        # split each json row data
        row_data = df.iloc[i: i + 5].to_json(orient='records', lines=True).split('\n')
        for row in row_data:
            # pretty print each user data
            parsed_row = json.loads(row)
            json_row = json.dumps(parsed_row, indent=2)
            print(json_row)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
