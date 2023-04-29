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