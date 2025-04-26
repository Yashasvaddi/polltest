import streamlit as st
import psycopg2

# Your Supabase connection string
conn_str = "postgresql://postgres:Yash@2017@db.ywikpplsoviaonplwagr.supabase.co:5432/postgres"

# Connect to Supabase Postgres
conn = psycopg2.connect(conn_str)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS click_counter (
        id SERIAL PRIMARY KEY,
        count INTEGER
    );
""")
conn.commit()

# Check if a count row exists
cursor.execute("SELECT count FROM click_counter WHERE id = 1;")
row = cursor.fetchone()

# If not, insert initial value
if row is None:
    cursor.execute("INSERT INTO click_counter (id, count) VALUES (1, 0);")
    conn.commit()
    count = 0
else:
    count = row[0]

# Display count
st.write(f"Button clicked {count} times.")

# On click, update the count
if st.button("Hello"):
    new_count = count + 1
    cursor.execute("UPDATE click_counter SET count = %s WHERE id = 1;", (new_count,))
    conn.commit()
    st.experimental_rerun()

# Close connection
cursor.close()
conn.close()
