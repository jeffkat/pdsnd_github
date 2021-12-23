import time
import pandas as pd
import numpy as np

SECTION_DIVIDER = '-'*40

CITY_TO_FILENAME_MAPPING = { 'Chicago': 'chicago.csv',
                             'New York City': 'new_york_city.csv',
                             'Washington': 'washington.csv' }

VALID_MONTHS = ["January", "February", "March", "April", "May", "June"]
VALID_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!\n")

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input("Would you like to view data for Chicago, New York City or Washington?\n")
            city = city.title()
            if city in CITY_TO_FILENAME_MAPPING:
                break
            else:
                print("Incorrect city name! Please try again: ")
        except:
                print("Invalid input! Please try again: ")
    print("You have chosen {}. ".format(city))

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input("Next, enter the full name of a month (from January to June) to view data for, or enter 'All' to view all months:\n")
            month = month.title()
            if month in VALID_MONTHS or month == "All":
                break
            else:
                print("That's not an option! Please try again:")
        except:
            print("Invalid input! Please try again:")
    print("You have chosen {}. ".format(month))
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("Next, enter the full name of a day of the week (Monday to Sunday) to view data for, or enter 'All' to view all days:\n")
            day = day.title()
            if day in VALID_DAYS or day == "All":
                break
            else:
                print("That's not an option! Please try again:")
        except:
            print("Invalid input! Please try again:")
    print("You have chosen {}".format(day))

    print(SECTION_DIVIDER)

    print("You have chosen to filter the data as follows: \n**City: {}** **Month: {}** **Day: {}**".format(city, month, day))
    while True:
        try:
            cont = input("Please enter 'Y' to continue with these filters or 'N' to restart:")
            if cont.upper() == "Y":
                print("Ok, let's continue!")
                print(SECTION_DIVIDER)
                break
            elif cont.upper() == "N":
                print("Ok, restarting now!")
                print(SECTION_DIVIDER)
                main()
        except:
            print("Invalid input! Please try again:")
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "All" to apply no month filter
        (str) day - name of the day of week to filter by, or "All" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_TO_FILENAME_MAPPING[city])

    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.weekday_name

    if month != "All":
        #use index of VALID_MONTHS list to get corresponding int
        month = VALID_MONTHS.index(month) + 1
        df = df[df["month"] == month]

    if day != "All":
        df = df[df["day_of_week"] == day]

    return df

def display_raw(df):
    """Displays five rows of filtered raw data at a time"""
    i = 0
    view_raw = input("Would you like to view 5 rows of the raw data? Please enter 'Y' to view or 'N' to continue: ")
    while view_raw.upper() == "Y" and i+5 < df.shape[0]:
        pd.set_option('display.max_columns',200)
        print(df.iloc[i:i+5])
        i += 5
        view_raw = input("Would you like to view 5 more rows of the raw data? Please enter 'Y' to view or 'N' to continue: ")
        print(SECTION_DIVIDER)


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df["month"].mode()[0]
    MONTH_DICTIONARY = {1: "January",
                        2: "February",
                        3: "March",
                        4: "April",
                        5: "May",
                        6: "June"}
    print("The most popular month for travel was: {}.".format(MONTH_DICTIONARY[popular_month]))

    # TO DO: display the most common day of week
    print("The most popular day of the week for travel was: {}.".format(df['day_of_week'].mode()[0]))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most popular hour of the day to start travel was: {}:00.".format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(SECTION_DIVIDER)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("'{}' was the most commonly used start station.".format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print("'{}' was the most commonly used end station.".format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    df['Combined Stations'] = (df['Start Station'] + " and " + df['End Station'])
    print("The most common combination of start and end station was: {}.".format(df['Combined Stations'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(SECTION_DIVIDER)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Trip Duration'] = (df['End Time'] - df['Start Time'])
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time was {}.".format(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The average travel time was {}.".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(SECTION_DIVIDER)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_counts = df["User Type"].value_counts()
    print("There were {} subscribers.".format(user_counts.loc["Subscriber"]))
    print("There were {} customers.".format(user_counts.loc["Customer"]))

    # TO DO: Display counts of gender
    if "Gender" in df.columns:
        df["Gender"].fillna(value="Unknown", inplace=True)
        gender_counts = df["Gender"].value_counts()
        print("\nThere were {} female users.".format(gender_counts.loc["Female"]))
        print("There were {} male users.".format(gender_counts.loc["Male"]))
        print("Gender data was not recorded for {} users.".format(gender_counts.loc["Unknown"]))
    else:
        print("\nSorry, no gender data is available for your chosen city.")

    # TO DO: Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        print("\nThe oldest user was born in {}.".format(int(df["Birth Year"].min())))
        print("The youngest user was born in {}.".format(int(df["Birth Year"].max())))
        print("The year in which the most users were born was {}.".format(int(df["Birth Year"].mode()[0])))
    else:
        print("\nSorry, no birth year data is available for your chosen city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(SECTION_DIVIDER)




def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_raw(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input("\nPlease enter 'Y' to restart or 'N' to exit program:\n")
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
