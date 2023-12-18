import sqlite3
import pandas as pd

# Database connection
db_path = 'cluster_usage.db'
conn = sqlite3.connect(db_path)

# Query to select data from the database
query = 'SELECT * FROM cluster_usage'

# Load the data into a Pandas DataFrame
data = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Data Analysis
# For example, aggregating usage hours per user
# Replace 'usedcpus' and 'usedgpus' with the actual column names for CPU and GPU hours
user_usage = data.groupby('User').agg({'AllocCPUS': 'sum'}).reset_index()

# Now, 'user_usage' DataFrame contains the total CPU and GPU usage hours per user
print(user_usage)

# Further analysis can be done as needed

