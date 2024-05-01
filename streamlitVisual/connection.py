import pymysql
import pandas as pd

def get_data():
    # Establish connection to the MySQL database
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 database='temp3',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        # Query to fetch data from TBLU_SCREENER_PARENT table
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM temp3.TBLU_SCREENER_PARENT')
            rows = cursor.fetchall()
            df = pd.DataFrame(rows)

        # Query to fetch data from TBLU_SCREENER_VA table
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM temp3.TBLU_SCREENER_VA')
            rows = cursor.fetchall()
            df1 = pd.DataFrame(rows)

        # Merge the dataframes on the 'SEG_NM' column
        merged_df = df.merge(df1, on='SEG_NM', how='left')
    finally:
        # Close the database connection
        connection.close()

    return merged_df
