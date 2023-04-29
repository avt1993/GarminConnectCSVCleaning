# **Garmin Connect ETL Script**

Python module "GarminConnectETL" contains multiple functions that will clean, format and transform a raw CSV file previously extracted from Garmin Connect. These CSV files contain swim, bike and run metrics collected by the athlete while training and racing.

GarminCoonectETL contains the following funtions:
- **clean_csv()** ---> This function will recieve the string variable containing the file pathname of the csv file stored locally. This function will clean, format and transform the csv file and will return a modified dataframe.
- **csv_concat()** ---> This function will recieve multiple Dataframes that have been previously cleaned, formatted and transformed through the **clean_csv()** funtion and will concantenate all Dataframes into one main Dataframe.
- **create_ranges()** ---> This function will receive multiple variables and will return a Dataframe with **pace** or **power** ranges. The purpose of this function is to order data into ranges in order to better understand and identify patterns or trends depending on the athletes swim/run pace or bike power output.
