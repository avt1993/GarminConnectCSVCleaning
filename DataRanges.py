import pandas as pd

# Function that converts an int to time format Example: 300 to 5:00.
def int_to_time_format(time):
     # Calculate minutes and seconds
    minutes, seconds = divmod(time, 60)
    # Format minutes and seconds as a string
    time_str = f"{minutes:01d}:{seconds:02d}"

    return time_str



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