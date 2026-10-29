import pyodbc

server = r"PRIYA\SQLEXPRESS"
database ="HarvardArtDB"

connection = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_connection=yes"
)

cursor = connection.cursor()

print("connected to SQL Server successfully")
