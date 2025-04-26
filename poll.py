import streamlit as st
from supabase import create_client, Client
import time

# Your Supabase URL and API Key
url = "https://ywikpplsoviaonplwagr.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl3aWtwcGxzb3ZpYW9ucGx3YWdyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU2NTAwNDQsImV4cCI6MjA2MTIyNjA0NH0.yk7K8XgARwovwqKwlqwvE-c3rrJmp_MkEvniNarb8BE"  # Replace with your Supabase key

# Create a Supabase client
supabase = create_client(url, key)

# Initialize count in session state if it doesn't exist
if 'count' not in st.session_state:
    st.session_state.count = 0

# Button and counter logic
if st.button("Hello"):
    # Increment count locally
    st.session_state.count += 1

    try:
        # Update count in Supabase
        supabase.table('click').upsert(
            {'id': 1, 'count': st.session_state.count},
            on_conflict=['id']  # Assuming 'id' is a unique key in your table
        ).execute()
        st.success("Count updated in the database.")
    except Exception as e:
        st.error(f"Failed to update count: {e}")

# Display the count
st.write(f"Button Clicked {st.session_state.count} times.")

# Poll for changes in the database and rerun the app
while True:
    time.sleep(5)  # Check every 5 seconds

    try:
        result = supabase.table('click').select('count').eq('id', 1).execute()
        if result.data:
            new_count = result.data[0]['count']
            if new_count != st.session_state.count:
                st.session_state.count = new_count  # Update local count with the value from DB
                st.experimental_rerun()  # Rerun the app to reflect the change
    except Exception as e:
        st.error(f"Failed to fetch count from database: {e}")
