import pyodbc

SERVER_NAME = 'TLRDBIBD-P-001'
DATABASE_NAME = 'DB_ONPREMISE_CLOUD'
USER = 'dwh_tbl'
SQL_PASSWORD = 'D3h0_T4b1_2020'


try:
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+SERVER_NAME+';DATABASE='+DATABASE_NAME+'UID='+USER+'; PWD='+SQL_PASSWORD+'')
    print('Conexión Exitosa')

except :
    print('No ha sido Posible Concretar la Conexión')
