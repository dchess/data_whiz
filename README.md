# README

## Prerequisites
1. Install [pipenv](https://pipenv-fork.readthedocs.io/en/latest/)
2. Install [odbc drivers](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15) OR install [Docker](https://docs.docker.com/docker-for-mac/install/)

## Tutorial
1. Install [SQLSorcery](https://sqlsorcery.readthedocs.io/en/latest/cookbook/installation.html)
2. Set up [.env](https://sqlsorcery.readthedocs.io/en/latest/cookbook/environment.html) file

    ```bash
    MS_SERVER=dchess.database.windows.net
    MS_DB=data_whiz                                                                         
    MS_SCHEMA=dbo                                                                      
    MS_USER=sql_admin                                                                  
    MS_PWD=DataWhiz2019
    ```

3. Download [2019 SBAC Research Files](https://caaspp-elpac.cde.ca.gov/caaspp/ResearchFileList)

    This can be done manually or using some simple python:

    ```python
    import urllib.request

    url = "http://caaspp-elpac.cde.ca.gov/caaspp/researchfiles/sb_ca2019_1_csv_v2.zip"
    urllib.request.urlretrieve(url, "sb_ca2019_1_csv_v2.zip")
    ```

4. Unzip the files

    Again, this can be done manually in the file system or with a little python:

    ```python
    from zipfile import ZipFile

    with ZipFile("sb_ca2019_1_csv_v2.zip", "r") as z:
        z.extractall()
    ```

5. Read the CSV files into [Pandas](https://pandas.pydata.org/) dataframes 

    ```python 
    import pandas as pd

    entities = pd.read_csv("sb_ca2019entities_csv.txt", encoding="ISO-8859-1")
    scores = pd.read_csv("sb_ca2019_1_csv_v2.txt", encoding="ISO-8859-1")
    ```

    The additional encoding is necessary because the SBAC files do not use the standard UTF-8.

6. Load them as tables in the database

    ```python
    from sqlsorcery import MSSQL

    sql = MSSQL()
    sql.insert_into("sbac_entities_2019", entities, chunksize=1000)
    sql.insert_into("sbac_scores_2019", scores, chunksize=1000)
    ```

    The additional chunksize param allows for batch insertions, greatly improving performance.

7. Now you can query as you like. Some samples are provided.

    ```python
    from sqlsorcery import MSSQL

    sql = MSSQL()
    df = sql.query("SELECT * FROM sbac_entities_2019")
    ```

8. Run the source code

    If you are using the provided Dockerfile:

    ```bash
    $ docker build -t data_whiz .
    $ docker run --rm -it data_whiz
    ```

    If you have installed the Microsoft ODBC drivers locally:

    ```bash
    $ pipenv run python main.py
    ```
