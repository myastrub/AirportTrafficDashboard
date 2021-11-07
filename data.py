import pandas as pd
import numpy as np
import constants as c
from datetime import timedelta

dataset = pd.read_csv('datasets/Airport_Traffic.csv', delimiter=';')
dataset[c.DATE] = pd.to_datetime(dataset[c.DATE], format='%d/%m/%Y')

def has_airport_data(data):
    if (c.AIRPORT_DEP_FLIGHTS in data.columns or
        c.AIRPORT_ARR_FLIGHTS in data.columns or
        c.AIRPORT_TOTAL_FLIGHTS in data.columns):
        return True
    else:
        return False

def filter_dataset_by_date(data, start_date, end_date):
    if start_date is None:
        beginning_date = pd.to_datetime(get_date(data, min))
    else:
        beginning_date = pd.to_datetime(start_date)
    if end_date is None:
        ending_date = pd.to_datetime(get_date(data, max))
    else:
        ending_date = pd.to_datetime(end_date)

    filtered_dataset = data[
        data[c.DATE].ge(beginning_date)
        & data[c.DATE].le(ending_date)
    ]

    return filtered_dataset
    

def filter_dataset(data, airports=None, states=None, start_date=None, end_date=None):
    
    filtered_dataset = filter_dataset_by_date(
        data, start_date, end_date
    )
    
    if airports and states:
        filtered_dataset = filtered_dataset[
            filtered_dataset[c.AIRPORT_NAME].isin(airports)
            & filtered_dataset[c.STATE_NAME].isin(states)
        ]
    elif (airports is None or airports == []) and states:
        filtered_dataset = filtered_dataset[
            filtered_dataset[c.STATE_NAME].isin(states)
        ]
    elif (states is None or states == []) and airports:
        filtered_dataset = filtered_dataset[
            filtered_dataset[c.AIRPORT_NAME].isin(airports)
        ]
    
    return filtered_dataset


def get_date(data, func):
    return pd.to_datetime(
        str(func(data[c.DATE].unique()))
    ).strftime('%m/%d/%Y')

def get_last_date(data):
    return pd.to_datetime(
        str(max(data[c.DATE].unique()) + np.timedelta64(1, 'D'))
    ).strftime('%m/%d/%Y')


def get_flight_columns(ifr_movements):
    if len(ifr_movements) == 2 or len(ifr_movements) == 0:
        flight_columns = [c.NM_TOTAL_FLIGHTS, c.AIRPORT_TOTAL_FLIGHTS]
    elif ifr_movements[0] == 'Arrival':
        flight_columns = [c.NM_ARR_FLIGHTS, c.AIRPORT_ARR_FLIGHTS]
    elif ifr_movements[0] == 'Departure':
        flight_columns = [c.NM_DEP_FLIGHTS, c.AIRPORT_DEP_FLIGHTS]
    return flight_columns

def get_number_of_flights(data, flight_columns):
    """
    Takes a dataset and flight columns (arrival, departure or total)
    and returns dataframe with dates of flights and a number of flights
    according to NM and airport
    """

    pivot = pd.pivot_table(
        data, values=flight_columns, index=c.DATE,
        aggfunc=np.sum
    )
    pivot = pivot.reset_index()
    return pivot


def get_top_flight_airports(data, source='NM'):
    """
    Returns top 5 countries with daily average flights
    source indicates which column to use: NM or APT one.
    Default is set to NM.
    """
    if source == 'APT':
        flight_column = c.AIRPORT_TOTAL_FLIGHTS
    else:
        flight_column = c.NM_TOTAL_FLIGHTS
    pivot = pd.pivot_table(
        data, values=flight_column, index=c.AIRPORT_NAME,
        aggfunc=np.mean
    )
    if not pivot.empty:
        pivot = pivot.reset_index()
        pivot = pivot.rename(columns={
            flight_column:c.DAILY_AVERAGE
        })
        pivot = pivot.sort_values(by=c.DAILY_AVERAGE, ascending=False)
        return pivot.head()
    else:
        return pd.DataFrame(columns=[c.AIRPORT_NAME, c.DAILY_AVERAGE])


def get_daily_average_per_state(data, flight_columns):
    """
    Takes a dataset and flight columns (arrival, departure or total)
    and returns dataframe with states and a number of daily flights
    according to NM and airport
    """
    if has_airport_data(data):
        pivot = pd.pivot_table(
            data, values=flight_columns, index=c.STATE_NAME,
            aggfunc=np.sum
        )
    else:
        pivot = pd.pivot_table(
            data, values=flight_columns[0], index=c.STATE_NAME,
            aggfunc=np.sum
        )
    pivot = pivot.reset_index()
    pivot = pivot.sort_values(by=c.STATE_NAME)
    return pivot


def get_average_per_month(data, flight_columns):
    """
    Takes a dataset and flight columns (arrival, departure or total)
    and returns dataframe with months and a number of daily flights
    according to NM and airport
    """
    pivot = pd.pivot_table(
        data, values=flight_columns, index=[c.MONTH_MON, c.MONTH_NUM],
        aggfunc=np.mean
    )
    pivot = pivot.sort_values(by=c.MONTH_NUM)
    pivot = pivot.reset_index()
    return pivot
    


def get_list_of_states(data):
    """
    Returns a list of states from the dataset
    """
    return data[c.STATE_NAME].unique()


def get_list_of_airports(data):
    """
    Returns a list of states from the dataset
    """
    return data[c.AIRPORT_NAME].unique()