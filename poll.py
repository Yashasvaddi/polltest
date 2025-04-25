import streamlit as st

# Initialize count in session state if it doesn't exist
if 'count' not in st.session_state:
    st.session_state.count = 0

# Button and counter logic
if st.button("Hello"):
    st.session_state.count += 1

# Display the count
st.write(f"Button clicked {st.session_state.count} times.")
