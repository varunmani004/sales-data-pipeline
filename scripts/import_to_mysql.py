import pandas as pd
import mysql.connector
import numpy as np

csv_path = r"C:\temp\cleaned_sales_data.csv"

# Load CSV
df = pd.read_csv(csv_path)

# Clean columns
df.columns = (
    df.columns.astype(str)
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

df = df.loc[:, ~df.columns.str.contains("^unnamed", case=False)]
df = df.loc[:, df.columns.notna()]

# Convert NaN → None
df = df.replace({np.nan: None})

print("Final columns:", df.columns.tolist())
print("Total rows to insert:", len(df))

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="sales_pipeline"
)

cursor = conn.cursor()

# Drop table if it exists (IMPORTANT)
cursor.execute("DROP TABLE IF EXISTS sales_data")

# Create table
columns_sql = ", ".join([f"`{col}` TEXT" for col in df.columns])

cursor.execute(f"""
CREATE TABLE sales_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    {columns_sql}
)
""")

# Insert in batches
placeholders = ", ".join(["%s"] * len(df.columns))
cols = ", ".join([f"`{c}`" for c in df.columns])

insert_sql = f"""
INSERT INTO sales_data ({cols})
VALUES ({placeholders})
"""

batch_size = 1000
for i in range(0, len(df), batch_size):
    batch = df.iloc[i:i+batch_size].values.tolist()
    cursor.executemany(insert_sql, batch)
    conn.commit()
    print(f"Inserted rows: {i + len(batch)}")

cursor.close()
conn.close()

print("✅ FULL INSERT COMPLETED SUCCESSFULLY")
