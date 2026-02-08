# export_mysql_to_csv.py
import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="sales_user",
    password="sales123",
    database="sales_pipeline"
)

df = pd.read_sql("SELECT * FROM sales_data", conn)
df.to_csv("data/sales_data_cleaned.csv", index=False)

print("CSV exported successfully")
