#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


# Load and process the data
file_path = './project/cluster_usage_data.txt'
df = pd.read_csv(file_path, delimiter='|')


# Adding column of totalCpuTime for each job by seconds and converting start and end dates

# In[3]:


def parse_time(time_str):
    parts = time_str.split('-')
    if len(parts) == 2:
        days, time = parts
    else:
        days = 0
        time = parts[0]

    hours, minutes, seconds = map(int, time.split(':'))
    total_seconds = int(days) * 86400 + hours * 3600 + minutes * 60 + seconds
    return total_seconds


df["CPUTimeSeconds"] = df["CPUTime"].apply(parse_time)

df['Start'] = pd.to_datetime(df['Start'], errors='coerce', utc=True)
df['End'] = pd.to_datetime(df['End'], errors='coerce', utc=True)


df.head()
print(df.columns)


# # Processing by User

# In[4]:


def getTotalTimeAll():
    temp = df.groupby('User')['CPUTimeSeconds'].sum()
    return temp


# example usage
getTotalTimeAll()


# In[5]:


def getTotalTimeUser(user):
    return getTotalTimeAll()[user]

#example usage:
getTotalTimeUser('safae')


# Cpu time per Partition

# In[6]:


#Grouping by the type partitions
def CpuTimePartitionAll():
    return df.groupby("Partition")["CPUTimeSeconds"].sum()

def CpuTimePartition(partition):
    return CpuTimePartitionAll()[partition]


CpuTimePartitionAll()


# In[18]:


df.groupby(["Partition", "User"])["CPUTimeSeconds"].sum()
# df.head()


# Cpu Time per Account

# In[7]:


def TotalTimeAccountAll():
    return df.groupby("Account")["CPUTimeSeconds"].sum()

def TotalTimeAccount(account):
    return TotalTimeAccountAll()[account]


TotalTimeAccountAll()


# Filtering by start and end Date

# In[8]:


def filter_jobs_within_dates(start_date, end_date):
    # Convert input dates to UTC timezone-aware datetime objects
    start_date_utc = pd.to_datetime(start_date).tz_localize('UTC')
    end_date_utc = pd.to_datetime(end_date).tz_localize('UTC')

    # Filter the DataFrame for jobs within the specified date range
    # Both Start and End dates must be within the range
    filtered_df = df[(df['Start'] >= start_date_utc) & (df['End'].fillna(pd.Timestamp('now').tz_localize('UTC')) <= end_date_utc)]
    return filtered_df


# Example usage
start_date = '2023-12-08T00:00:00'
end_date = '2023-12-12T23:59:59'

filtered_jobs = filter_jobs_within_dates(start_date, end_date)
print(filtered_jobs)



# Group by state

# In[9]:


def jobsState():
    return df.groupby("State").size()

jobsState()



# TotalCpuTime per day for each user for a given period of time

# In[10]:


def calculate_daily_cpu_times(row):
    start = row['Start']
    end = row['End'] if pd.notna(row['End']) else pd.Timestamp('now').tz_localize('UTC')
    daily_times = {}

    current = start
    while current.date() <= end.date():
        next_day = (current + pd.Timedelta(days=1)).replace(hour=0, minute=0, second=0)
        daily_end = min(end, next_day)
        seconds = (daily_end - current).total_seconds()
        date_str = f"{current.date()} {current.strftime('%A')}"
        daily_times[date_str] = seconds * row['AllocCPUS']
        current = next_day

    return pd.Series(daily_times)


def aggregate_daily_cpu_times(df, column):
    daily_data = df.apply(calculate_daily_cpu_times, axis=1)
    daily_data[column] = df[column]
    return daily_data.melt(id_vars=[column], var_name='Date', value_name='CPUTimeSeconds').groupby([column, 'Date']).sum()

# wa7d l exemple
start_date = '2023-12-12T00:00:00'
end_date = '2023-12-13T23:59:59'


filtered_df = filter_jobs_within_dates( start_date, end_date)
daily_cpu_times = aggregate_daily_cpu_times(filtered_df, 'User')
print(daily_cpu_times)


# In[11]:


filtered_df = filter_jobs_within_dates(start_date, end_date)
daily_cpu_times = aggregate_daily_cpu_times(filtered_df, 'Account')
print(daily_cpu_times)


# In[12]:


aggregate_daily_cpu_times(filtered_df, 'Partition')


# Top users according to TotalCpuTime within a period of time

# In[13]:


def topUsers(startDate, endDate):
    return filter_jobs_within_dates(startDate, endDate).groupby('User')['CPUTimeSeconds'].sum().sort_values(ascending=False)


# In[14]:


topUsers(start_date, end_date)

