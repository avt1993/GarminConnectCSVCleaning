import pandas as pd
import numpy as np
import datetime    

# Cleans and formats a csv file for swim, bike or run activities from garmin connect.
def clean_csv(file_path: str):

    # Convert all columns with time related fields to total seconds or minutes.
    def time_format_to_float(row):
        try:
            # Check if time string is in format 'HH:MM:SS'
            time_obj = datetime.datetime.strptime(str(row), '%H:%M:%S')
            minutes = time_obj.minute + time_obj.hour * 60
            return float(minutes)
        except ValueError:
            try:
                # Check if time string is in format 'M:SS'
                time_obj = datetime.datetime.strptime(str(row), '%M:%S')
                seconds = time_obj.second + time_obj.minute * 60
                return float(seconds)
            except ValueError:
                return np.nan
            
    df = pd.read_csv(file_path)

    columnsToDrop = ['Favorite', 'Title', 'Avg GAP', 'Decompression', 'Surface Interval', 'Dive Time', 'Total Reps', 'Flow', 'Grit', 'Best Lap Time', 'Avg GCT Balance']
    columnsToSkip = ['Activity Type', 'Date', 'L/R Balance']

    # Loop to drop the columns from the list 'columnsToDrop' if in fact they exist. 
    for column in columnsToDrop:
        if column in df.columns:
            df = df.drop(column, axis = 1)

    # Loop that will format columns to type float if they meet the conditions.
    df = df.replace('--', np.nan)
    columnNames = df.columns

    for col in columnNames:
        if col not in columnsToSkip:
            if df[col].dtype == 'object':
                if df[col].str.contains(':').any():
                    df[col] = df[col].apply(time_format_to_float)
                else:
                    df[col] = df[col].str.replace(',', '').astype(float).round(2)
            elif df[col].dtype == 'int':
                df[col] = df[col].astype(float).round(2)
    
    # Convert meters to km for total distance if the activity is a swim.
    df['Distance'] = df.apply(lambda row: row['Distance'] / 1000 if 'Swim' in row['Activity Type'] else row['Distance'], axis = 1).round(2)

    # Change Date to datatype 'DateTime'.
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    return df

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def csv_concat(*dfs):
    return pd.concat(dfs, axis = 0)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Function that converts an int to time format Example: 300 to 5:00.
def int_to_time_format(time):
     # Calculate minutes and seconds
    minutes, seconds = divmod(time, 60)
    # Format minutes and seconds as a string
    time_str = f"{minutes:01d}:{seconds:02d}"

    return time_str

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Function that will create a dataframe with ranges and means
# df - dataframe to analyze, min - minimum value in time range, max - maximum value in time range,
# jumps - time jump between ranges, string1 - Time column name in dataframe, string2 - Column to correlate with Time.
def create_ranges(df: pd.DataFrame, min: int, max: int, jumps: int, string1: str, string2: str, rangeType: str):
    """
    Description of create_ranges.

    Parameters
    ----------
    df : DataRFrame
        Dataframe with swim/bike/run data.
    min : int
        The lowest the range will go.
    max : int
        The higest the range will go.
    jumps : int
        The jump gap between each range calculated.
    string1: string
        The time column used to generate the time/pace ranges.
    string2: string
        The column to analyze and fit into time/pace ranges.
    rangeType: string
        Power or Pace

    Returns
    -------
    return_type
        Returns a Dataframe with time/pace ranges and the parameter we want to fit into the different ranges.
    """

        
    range_df = pd.DataFrame(columns = [string1, string2])
    i = min

    if rangeType == 'Pace':
        while i < max:
            mean = round(df.loc[df[string1].between(i, i + jumps), string2].mean(), 2)

            minRange = int_to_time_format(i)
            maxRange = int_to_time_format(i + jumps)
            complete_range = minRange + ' - ' + maxRange

            row = pd.DataFrame({string1: [complete_range], string2: [mean]})
            range_df = pd.concat([range_df, row], ignore_index = True)
            i = i + jumps
            
        range_df = range_df.dropna(axis = 0)
    
    elif rangeType == 'Power':
        while i < max:
            mean = round(df.loc[df[string1].between(i, i + jumps), string2].mean(), 2)
            complete_range = str(i) + '-' + str(i + jumps) + ' W'
            
            row = pd.DataFrame({string1: [complete_range], string2: [mean]})
            range_df = pd.concat([range_df, row], ignore_index = True)
            i = i + jumps

        range_df = range_df.dropna(axis = 0)

    return range_df