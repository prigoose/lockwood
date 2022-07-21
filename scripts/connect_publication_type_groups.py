# clean up data so that the lawyers table refers to publication types

# add new column 
# for publicationtypegroups column
# iterate through array
# assign foreign key

# Example python program to read data from a PostgreSQL table

# and load into a pandas DataFrame

import pandas as pds
import psycopg2
from sqlalchemy import create_engine

# Create an engine instance

alchemyEngine   = create_engine('postgresql+psycopg2://test:@127.0.0.1', pool_recycle=3600);

 

# Connect to PostgreSQL server

dbConnection    = alchemyEngine.connect();

 

# Read data from PostgreSQL database table and load into a DataFrame instance

dataFrame       = pds.read_sql("select id, publicationtypegroups from \"firms_clean\"", dbConnection);


df = pds.DataFrame({'c1': [10, 11, 12], 'c2': [100, 110, 120]})
df = df.reset_index()  # make sure indexes pair with number of rows

for index, row in df.iterrows():
    array = row['publicationtypegroup']
    # iterate through array, add a foreign key
    array.
    row["publicationtypegroup_clean"] = 


pds.set_option('display.expand_frame_repr', False);

 

# Print the DataFrame

print(dataFrame);

 

# Close the database connection

dbConnection.close();

         

alchemyEngine           = create_engine('postgresql+psycopg2://test:test@127.0.0.1/test', pool_recycle=3600);

postgreSQLConnection    = alchemyEngine.connect();

postgreSQLTable         = "StudentScores";

 

try:

    frame           = dataFrame.to_sql(postgreSQLTable, postgreSQLConnection, if_exists='fail');

except ValueError as vx:

    print(vx)

except Exception as ex:  

    print(ex)

else:

    print("PostgreSQL Table %s has been created successfully."%postgreSQLTable);

finally:

    postgreSQLConnection.close();

 
