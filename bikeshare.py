import time
import pandas as pd
import numpy as np
import math

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

    print('Hello! Let\'s explore some US bikeshare data!\nWhich of the following cities would you like to see more information about Chicago, New York, or Washington?\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
      city_chosen = input().lower()
      if city_chosen.lower() not in CITY_DATA.keys():
        print("That is not one of the available cities. Please select Chicago, New York, or Washington.")
        continue
      else:
        print('Nice choice! We\'ll use %s.' % city_chosen.lower().title())
        break

    # TO DO: get user input for month (all, january, february, ... , june)

    while True:
      month_chosen = input("\n In which month would you like to see data for? January, February, March, April, May, June. Type 'all' if you do not have any preference?\n").lower()
      if month_chosen not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
        print("It seems you have either not entered the month's full name or you have entered a month on a different planet. Please, try again.")
        continue
      else:
        print('Ok then! We\'ll use %s.' % month_chosen.lower().title())
        break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
      day_chosen = input("\nAre you looking for a particular day? If so, kindly enter the day as follows: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type 'all' if you do not have any preference.\n").lower()
      if day_chosen not in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'):
        print("It seems you have not entered a valid day of the week. kindly enter the day as follows: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type 'all' if you do not have any preference.\n")
        continue
      else:
        print('Sounds good! We\'ll use %s.' % day_chosen.lower().title())
        break

    print('-'*40)
    return city_chosen, month_chosen, day_chosen


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
    # load the city data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and start hour from Start Time to create new columns

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
   	 	# use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

    	# filter by month to create the new dataframe
        df = df[df['month'] == month]

        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most popular month
    month_list = ['january','february','march','april','may','june','all']
    common_month_num = df['month'].mode()[0]
    popular_month = month_list[common_month_num-1].title()
    print('Most popular month:', popular_month)


    # TO DO: display the most popular day of week

    popular_day = df['day_of_week'].mode()[0]
    print('Most popular day:', popular_day)



    # TO DO: display the most common start hour

    common_start_hour = df['hour'].mode()[0]
    print('Most common hour:', common_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nDetermining the most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    # idxmx() get the row label of the maximum value
    Start_Station = df['Start Station'].value_counts().idxmax()
    print('Most Commonly used start station:', Start_Station)


    # TO DO: display most commonly used end station
    End_Station = df['End Station'].value_counts().idxmax()
    print('\nMost Commonly used end station:', End_Station)


    # TO DO: display most frequent combination of start station and end station trip
    frequent_journey =df.groupby(['Start Station', 'End Station']).size().nlargest(1)    
    print("\nThe most frequent trip from start to end is:\n{}".format(frequent_journey))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time

    Total_Travel_Time = sum(df['Trip Duration'])
    # Converting seconds to days
    print('Total travel time:', round_up((Total_Travel_Time/86400),2), " Days")


    # TO DO: display mean travel time

    Mean_Travel_Time = df['Trip Duration'].mean()
    # Converting seconds to minutes
    print('Mean travel time:', round_up((Mean_Travel_Time/60),2), " Minutes")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    # Washington does not have data for earliest, most recent, and most common year of birth therefore try and except were used.
    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)

    # TO DO: Display counts of gender

    try:
      gender_types = df['Gender'].value_counts()
      print('\nGender Types:\n', gender_types)
    except KeyError:
      print("\nGender Types:\nThere does not seem to be data available to display information about genders for this city.")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
      Earliest_Year = df['Birth Year'].min()
      print('\nThe oldest person using the system was born in:', int(Earliest_Year))
    except KeyError:
      print("\nThe oldest person using the system was born in:\nThere does not seem to be data available to determine the oldest person for this city.")

    try:
      Most_Recent_Year = df['Birth Year'].max()
      print('\nThe youngest person using the systen was born in:', int(Most_Recent_Year))
    except KeyError:
      print("\nThe youngest person using the systen was born in:\nThere does not seem to be data available to determine the youngest person for this city.")
    # idxmax() get the row label of the maximum value
    try:
      Most_Common_Year = df['Birth Year'].value_counts().idxmax()
      print('\nMost common year that people using the system were born in:', int(Most_Common_Year))
    except KeyError:
      print("\nMost common year that people using the system were born in:\nThere does not seem to be data available to determine the oldest person for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """
    Display individual trip data
    Args:
        bikeshare dataframe.
    Returns:
        None.
    """
    start = 0
    end = 5
    choice = ''
    while choice.lower() not in ['yes', 'no']:
        choice = input('Do you want to view indiviual trip data? Enter \'Yes\' or \'No\'.\n')
        if choice.lower() not in ['yes', 'no']:
            print('There are only two options \'Yes\' or \'No\'. Please try again.\n')
        elif choice.lower() == "yes":
            print(df.iloc[start:end])
            while True:
                second_choice = input('\nDo you want to view more trip data? Enter \'Yes\' or \'No\'.\n')
                if second_choice.lower() not in ['yes', 'no']:
                    print('Maybe you made a typo. Please try again.\n')
                elif second_choice.lower() == "yes":
                    start += 5
                    end += 5
                    print(df.iloc[start:end])
                elif second_choice == "no":
                    return
        elif choice.lower() == "no":
            return
    return

def restart():
  restart = input('\nWould you like to restart your search? Enter \'Yes\' or \'No\'.\n')
  if restart.lower() != 'yes':
    return
  else:
    main()


def main():
    while True:
        city, month, day = get_filters()
        print('Fetching some insightful data from {} for you...'.format(city).title())
        df = load_data(city, month, day)
        confirm_choice = ''
        while confirm_choice.lower() not in ['yes', 'no']:
          if month != 'all' and day != 'all':
            confirm_choice = input('Just to confirm you would like to see data for {} in {} on a {}. Type \'Yes\' or \'No\'.\n'.format(city.title(),month.title(),day.title()))
          elif month == 'all' and day == 'all':
            confirm_choice = input('Just to confirm you would like to see \'all\' data for {}. Type \'Yes\' or \'No\'.\n'.format(city.title()))
          elif month == 'all':
            confirm_choice = input('Just to confirm you would like to see data for {} for {} months on a {} . Type \'Yes\' or \'No\'.\n'.format(city.title(),month.title(),day.title()))
          else:
            confirm_choice = input('Just to confirm you would like to see data for {} in {} for {} days. Type \'Yes\' or \'No\'.\n'.format(city.title(),month.title(),day.title()))    
          if confirm_choice.lower() not in ['yes', 'no']:
            print('Maybe you made a typo. Please try again\n')
          elif confirm_choice.lower() == "yes":
            break
          elif confirm_choice.lower() == "no":
           restart()
       
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart()
        break

if __name__ == "__main__":
	main()
