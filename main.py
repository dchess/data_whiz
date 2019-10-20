import urllib.request
import zipfile
import pandas as pd
from sqlsorcery import MSSQL

# Download 2019 SBAC Research Files
url = "http://caaspp-elpac.cde.ca.gov/caaspp/researchfiles/sb_ca2019_1_csv_v2.zip"
urllib.request.urlretrieve(url, "sb_ca2019_1_csv_v2.zip")

# Extract flat files from zip folder
with zipfile.ZipFile("sb_ca2019_1_csv_v2.zip", "r") as z:
    z.extractall()

# Read datasets into dataframes
entities = pd.read_csv("sb_ca2019entities_csv.txt", encoding="ISO-8859-1")
scores = pd.read_csv("sb_ca2019_1_csv_v2.txt", encoding="ISO-8859-1")

# Establish database connection
sql = MSSQL()

# Insert SBAC files into database tables
sql.insert_into("sbac_entities_2019", entities, chunksize=1000)
sql.insert_into("sbac_scores_2019", scores, chunksize=1000)

# Query district scores for Oakland and San Francisco
df = sql.query_from_file("query.sql")
print(df)
