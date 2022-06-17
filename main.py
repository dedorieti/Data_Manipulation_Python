import pandas as pd
import numpy as np
import matplotlib
from sqlalchemy import create_engine
# to read and write to PostgreSQL
import psycopg2
# to read and write to Excel
import xlwt
import openpyxl
import xlrd

pd.set_option("display.max_columns", 10)
pd.set_option("display.max_rows", 50)

# Tutorial
# https://www.youtube.com/watch?v=ZyhVh-qRZPA
df = pd.read_csv("survey_results_public.csv", index_col='ResponseId')
df_schema = pd.read_csv("survey_results_schema.csv")

country_summary = df['Country'].value_counts()
age_summary = df['Age1stCode'].value_counts()

print(df.info())
print(df.shape)
# print(df.head(50))

# Example how to convert a dict into a df
people = {
    "first": ["name1", "name2", "name3"],
    "last": ["sd", "tr", "re"],
    "email": ["one@email.com", "two@email.com", "three@email.com"]
}

people_df = pd.DataFrame(people)
# set the index
people_df.set_index('email', inplace=True)
print(people_df)
print(people_df.index)
print(people_df.loc['one@email.com', 'last'])
print(people_df.iloc[0, 1])
people_df.reset_index(inplace=True)


# Slicing and sorting
# https://www.youtube.com/watch?v=zmdjNSmRXF4
print(df.loc[1:10:2, 'Country':'LearnCode'])
print(df.loc[1:10, ['Country', 'LearnCode']])
print(df.iloc[0:10, 2:4])
print(df[['Country', 'LearnCode']])
print(df.sort_index(ascending=False))

# df.sort_index(ascending=False, inplace=True)

# Filtering
# https://www.youtube.com/watch?v=Lw2rlcxScZY
filt = df['Country'] == 'Italy'
print(df.loc[filt])
print(df.loc[filt, 'MainBranch'])

# And operator
filt = (df['Country'] == 'Italy') & (df['MainBranch'] == 'I am a developer by profession')
print(df.loc[filt])
print(df.loc[filt, 'MainBranch'])

# Or operator and Negate the filter
filt = (df['Country'] == 'Italy') | (df['MainBranch'] == 'I am a developer by profession')
print(df.loc[~filt])
print(df.loc[~filt, 'MainBranch'])

# Filter over salary
high_salary = (df['ConvertedCompYearly'] > 70000)
dimensions = ['Country', 'EdLevel', 'LanguageHaveWorkedWith', 'ConvertedCompYearly']
print(df.loc[high_salary, dimensions])

# Filer multiple countries
countries = ['Italy', 'Germany', 'United States of America', 'United Kingdom of Great Britain and Northern Ireland',
             'India', 'Netherlands']
filt = df['Country'].isin(countries)
print(df.loc[filt, dimensions])

# Filter language
filt = df['LanguageHaveWorkedWith'].str.contains('Python', na=False)
print(df.loc[filt, dimensions])

# Update rows and columns
# https://www.youtube.com/watch?v=DCDe29sIKcE&list=RDCMUCCezIgC97PvUuR4_gbFUs5g&index=2

# update columns
df.columns = [x.upper() for x in df.columns]
df.columns = df.columns.str.replace(' ', '_')
df.rename(columns={'COUNTRY': 'COUNTRY_ORIGIN', 'US_STATE': 'STATE_US'}, inplace=True)
print(df)

# update rows
# use people_df as an example first
# change a single row
people_df.loc[2] = ['my@email.com', 'me', 'myself']
people_df.loc[2, 'first'] = 'dd'

# this does not work
filt = (people_df['first'] == 'dd')
people_df[filt]['first'] == 'pp'  # row assignment need .loc .iloc
people_df.loc[filt, 'first'] = 'pp'  # correct way to do it

# change email to upper case
people_df['email'] = people_df['email'].str.upper()  # grab the series from the df and apply a string operation

# Apply: works on df and series. It calls a function to a data object
# to a series. Apply a function to all values of the series
people_df['email'].apply(len)


# define custom email
def update_email(email):
    new_email = email.title()
    return new_email


people_df['email'].apply(update_email)

# Example with a lambda function
# lambda function is usually a simple no name function
people_df['email'].apply(lambda x: x.lower())  # x represents each value in the series

# apply to a df. Apply a function to all columns of a df
people_df.apply(len)
# apply the function NOT to the columns but to the rows
people_df.apply(len, axis='columns')

people_df.apply(pd.Series.min)
people_df.apply(lambda x: x.min())  # x represents each series in the df. HINT: use Series methods

# Applymap: apply a function to each element in the df. It does not work with series
people_df.applymap(len)
people_df.applymap(str.upper)

# Map (replace): it works only with series. It is use to substitute each value in a series with another value
people_df['first'].map({'name1': 'Mary', 'name2': 'John'})  # use replace if one needs to avoid nas
people_df['first'].replace({'name1': 'Mary', 'name2': 'John'})

# Perform some operation on the stack overflow df
df.rename(columns={'CONVERTEDCOMPYEARLY': 'SALARY_USD'}, inplace=True)
df['COUNTRY_ORIGIN'] = df['COUNTRY_ORIGIN'].replace({'Russian Federation': 'Russia'})

# Add/Remove Rows and Columns From DataFrames
# https://www.youtube.com/watch?v=HQ6XO9eT-fc&list=RDCMUCCezIgC97PvUuR4_gbFUs5g&index=3

# Columns
df['COUNTRY_ORIGIN_UPPER'] = df['COUNTRY_ORIGIN'].apply(lambda x: x.upper())

# Combine 2 columns
df['Country_Comb'] = df['COUNTRY_ORIGIN_UPPER'] + '_' + df['COUNTRY_ORIGIN']

# Remove columns
df.drop(columns=['COUNTRY_ORIGIN_UPPER', 'COUNTRY_ORIGIN'], inplace=True)

# Split columns and assign the output to 2 different columns
df[['Country_upper', 'Country']] = df['Country_Comb'].str.split('_', expand=True)

# Rows
# people_df.append({'first': 'dd'})   # error as it expects an index for the row
people_df.append({'first': 'dd'}, ignore_index=True)  # it produces Nas for the missing rows

# create a new dictionary and append to the existing df
people_2 = {
    "first": ["tony", "pony"],
    "last": ["ted", "tod"],
    "email": ["tony@email.com", "pony@email.com"]
}
people_df_2 = pd.DataFrame(people_2)

people_df['full_name'] = people_df['first'] + '_' + people_df['last']

people_df = people_df.append(people_df_2, ignore_index=True)

# Remove rows
people_df.drop(index=4)
filt = people_df[people_df['full_name'].isna()].index
people_df.drop(index=filt, inplace=True)

# Sort Data
# https://www.youtube.com/watch?v=T11QYVfZoD0&list=RDCMUCCezIgC97PvUuR4_gbFUs5g&index=9

people_df.sort_values(by='first')  # ascending order
people_df.sort_values(by='first', ascending=False)

# on multiple rows
people_df.sort_values(by=['first', 'email'], ascending=False)
people_df.sort_values(by=['first', 'email'], ascending=[False, False], inplace=True)

# sort by index
people_df.sort_index(inplace=True)

# Sort series
people_df['first'].sort_values(ascending=False)

# Apply sorting to the survey
df.sort_values(by='Country', inplace=True)
df.sort_values(by=['Country', 'SALARY_USD'], ascending=[True, False], inplace=True)
df[['Country', 'SALARY_USD']].head(100)

# Get the highest salaries
df['SALARY_USD'].nlargest(10)
df.nlargest(10, 'SALARY_USD')
df.nsmallest(10, 'SALARY_USD')

# Grouping and Aggregating - Analyzing and Exploring Your Data
# https://www.youtube.com/watch?v=txMdrV1Ut64&list=RDCMUCCezIgC97PvUuR4_gbFUs5g&index=2

df.describe()
df['SALARY_USD'].median()
df['SALARY_USD'].count()  # count counts the not-NAs values
df['Country_Comb'].value_counts()
df['GENDER'].value_counts()

filt = (df['SALARY_USD'] > 100000) & (df['Country'] == 'United States of America')
df[filt].loc[40587]

(df['ORGSIZE'].value_counts() / df['ORGSIZE'].count()) * 100
df['ORGSIZE'].value_counts(normalize=True)

# Grouping
# according to the Pandas documentation grouping involves:
# Split + Apply a function + Combine the results

# Split the data into groups
country_group = df.groupby(['Country'])
country_group.get_group('Italy')

# Apply a function to the groupby object
country_group_sum = country_group['GENDER'].value_counts()  # it outputs a series object
country_group_sum.loc['Germany']
country_group['GENDER'].value_counts(normalize=True).loc['Sweden']

country_group['SALARY_USD'].median().sort_values(ascending=False)
country_group['SALARY_USD'].median().loc['United States of America']

# apply multiple functions using the agg() function
country_group['SALARY_USD'].agg(['median', 'mean'])
country_group['SALARY_USD'].agg(['median', 'mean']).loc['Germany']

# analyse the data for people using Python
# by using a filter method
filt = df['Country'] == 'India'
df.loc[filt]['LANGUAGEHAVEWORKEDWITH'].str.contains('Python').sum()  # apply a method to a selected series

# use the group by function
country_group['LANGUAGEHAVEWORKEDWITH'].apply(lambda x: x.str.contains('Python').sum())  # apply method to all series
# in the group
country_group['LANGUAGEHAVEWORKEDWITH'].apply(lambda x: x.str.contains('Python').value_counts(normalize=True))

# Find out the percentage of people using Python
# use concat
country_uses_python = country_group['LANGUAGEHAVEWORKEDWITH'].apply(lambda x: x.str.contains('Python').sum())
country_respondents = df['Country'].value_counts()

python_df = pd.concat([country_respondents, country_uses_python], axis='columns')
python_df['Percentage_Uses_Python'] = python_df['LANGUAGEHAVEWORKEDWITH'] / python_df['Country']

# alternative
country_group['LANGUAGEHAVEWORKEDWITH'].apply(lambda x: x.str.contains('Python').sum()) / country_group[
    'Country'].value_counts()

# Cleaning Data - Casting Datatypes and Handling Missing Values
# https://www.youtube.com/watch?v=KdmPHEnPJPs&list=RDCMUCCezIgC97PvUuR4_gbFUs5g&index=2

# define a new dictionary

# Example how to convert a dict into a df
people = {
    "first": ["name1", "name2", "name3", "john", np.nan, None, "NA"],
    "last": ["sd", "tr", "re", "do", np.nan, np.nan, "Missing"],
    "email": ["one@email.com", "two@email.com", "three@email.com", "four@mail.com", "anonymus@mail.com", None,
              'Missing'],
    "age": ["33", "22", "54", "23", None, None, "Missing"]
}

people_df = pd.DataFrame(people)

# drop rows/columns with missing values
# drop columns
people_df.dropna(axis='columns', how='all')  # drop columns if all values are missing
people_df.dropna(axis='columns', how='any')  # drop columns if any value is missing

# drop rows
people_df.dropna()
people_df.dropna(axis='index', how='any')  # drop rows if any value is missing in any of the columns (standard)
people_df.dropna(axis='index', how='all')  # drop rows if all values in the row are missing

people_df.dropna(axis='index', how='any', subset=['email'])  # drop rows if any value is missing in specific columns
people_df.dropna(axis='index', how='all'
                 , subset=['email', 'age'])  # drop rows if all values are missing in specific columns
# using the parameter inplace it makes the changes permanent

# replace undefined missing value with standard np.nan
people_df.replace('NA', np.nan, inplace=True)
people_df.replace('Missing', np.nan, inplace=True)

people_df.fillna('MISSING')
# replace values for just one column
# people_df['age'] = people_df['age'].fillna(0)

# dcast data types
people_df.dtypes
# the type of np.nan is a float
type(np.nan)
# if a column has NAs can be converted to float and not to integer
people_df['age'] = people_df['age'].astype('float')
people_df['age'].mean()

# apply na methods to the survey
# one can handle custom missing value directly when reading a .csv file
na_vals = ['NA', 'Missing']
# df = pd.read_csv("survey_results_public.csv", index_col='ResponseId', na_values=na_vals)

df['YEARSCODE'].unique()
df['YEARSCODE'].replace('Less than 1 year', 0, inplace=True)
df['YEARSCODE'].replace('More than 50 years', 51, inplace=True)

df['YEARSCODE'].value_counts(normalize=True)

df['YEARSCODE'] = df['YEARSCODE'].astype('float')
df['YEARSCODE'].median()
df['YEARSCODE'].mean()

# Working with Dates and Time Series Data
# https://www.youtube.com/watch?v=UFuo7EHI8zc&list=RDCMUCCezIgC97PvUuR4_gbFUs5g&index=2

df = pd.read_csv("ETH_1h.csv")

# convert Date to datetime
# https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %I-%p')
df.loc[0, 'Date'].day_name()

# Alternatively one can in the import define columns with dates
# define first a lambda function to loop trough the rows
# the rows are imported as strings
d_parser = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %I-%p')
df = pd.read_csv('ETH_1h.csv', parse_dates=['Date'], date_parser=d_parser)

# Get the name of the day for the whole series
# access daytime class by typing dt
# https://docs.python.org/3/library/datetime.html#
# via dt one can access various attributes of the object like time, day, year and so on

df['DayOfWeek'] = df['Date'].dt.day_name()

df['Date'].min()
df['Date'].max()
# Time delta
df['Date'].max() - df['Date'].min()

# Filter the data
filt = df['DayOfWeek'] == 'Friday'
df.loc[filt].head(50)

filt = (df['Date'] >= '2020')
df.loc[filt]
filt = (df['Date'] >= pd.to_datetime('2020-01-01'))
df.loc[filt]

filt = (df['Date'] >= '2019') & (df['Date'] < '2020')
df.loc[filt]
filt = (df['Date'] >= pd.to_datetime('2019-01-01')) & (df['Date'] < pd.to_datetime('2020-01-01'))
df.loc[filt]

# set the date column as the index for the df
df.set_index('Date', inplace=True)
# use the index to filter the data
df.loc['2019']
df.loc['2019-01-10']
df.loc['2019-01-10']['High'].max()

# use slicing get Jan and Feb data in 2020
df['2020-01':'2020-02']
df['2020-01':'2020-02']['Close'].mean()

# Resampling
# https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects
highs = df['High'].resample('D').max()
highs['2019-01-10']

# Line plot
highs.plot()

# resample multiple columns
# same metric for all the columns
df.resample('W').mean()
# use different metrics
df.resample('W').agg({'Close': 'mean', 'High': 'max', 'Low': 'min', 'Volume': 'sum'})

# Reading/Writing Data to Different Sources - Excel, JSON, SQL, Etc
# https://www.youtube.com/watch?v=N6hyN6BW6ao&list=RDCMUCCezIgC97PvUuR4_gbFUs5g&index=3

df = pd.read_csv("survey_results_public.csv", index_col='ResponseId')
df_schema = pd.read_csv("survey_results_schema.csv")

df.head()

filt = (df['Country'] == 'India')
india_df = df.loc[filt]

# Save data in different formats
india_df.to_csv('Output/modified.csv')
india_df.to_csv('Output/modified.tsv', sep='\t')

# Excel
india_df.to_excel('Output/modified.xlsx')
test = pd.read_excel('Output/modified.xlsx', index_col='ResponseId')

# Json
# Dictionary-like output
india_df.to_json('Output/modified.json')
# List list-like output
india_df.to_json('Output/modified.json', orient='records', lines=True)
# Read from a json file
test = pd.read_json('Output/modified.json', orient='records', lines=True)

# Read from SQL DB
# Example with PostgreSQL
# create a connection to local postgresql
engine = create_engine('postgresql+psycopg2://postgres:247Trading@localhost:5432/maindb')

# Connect to DB using psycopg2
# conn_string = "host='localhost' dbname='maindb' user='postgres' password='247Trading'"
# conn = psycopg2.connect(conn_string)

india_df.to_sql('stack_overflow_survey', engine)
india_df.to_sql('stack_overflow_survey', engine, if_exists='replace')

sql_df = pd.read_sql('stack_overflow_survey', engine, index_col='ResponseId')
sql_df = pd.read_sql_query("SELECT * FROM stack_overflow_survey", engine, index_col='ResponseId')