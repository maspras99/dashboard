import streamlit as st
import sqlite3
import folium
from streamlit_folium import st_folium
import uuid
from datetime import datetime

# SQLite database initialization
DB_FILE = "locations.db"

def init_db():
    conn = sqlite3.connect(DB_FILE, timeout=10)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS locations (
                 user_id TEXT PRIMARY KEY,
                 latitude REAL,
                 longitude REAL,
                 timestamp TEXT)''')
    conn.commit()
    conn.close()

# Save user location to SQLite
def save_location(user_id, lat, lon):
    try:
        conn = sqlite3.connect(DB_FILE, timeout=10)
        c = conn.cursor()
        timestamp = datetime.now().isoformat()
        c.execute('INSERT OR REPLACE INTO locations (user_id, latitude, longitude, timestamp) VALUES (?, ?, ?, ?)',
                  (user_id, lat, lon, timestamp))
        conn.commit()
        st.session_state.debug_log = f"Success: Location saved for user {user_id}: ({lat}, {lon}) at {timestamp}"
    except Exception as e:
        st.session_state.debug_log = f"Error saving to SQLite: {str(e)}"
    finally:
        conn.close()

# Retrieve all locations from SQLite
def get_all_locations():
    try:
        conn = sqlite3.connect(DB_FILE, timeout=10)
        c = conn.cursor()
        c.execute('SELECT user_id, latitude, longitude, timestamp FROM locations')
        locations = [{"user_id": row[0], "latitude": row[1], "longitude": row[2], "timestamp": row[3]} for row in c.fetchall()]
        conn.close()
        st.session_state.debug_log = f"Success: Retrieved {len(locations)} locations"
        return locations
    except Exception as e:
        st.session_state.debug_log = f"Error retrieving from SQLite: {str(e)}"
        return []

# User page
def user_page():
    st.title("GPS Tracking - User")
    
    # Initialize user ID
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
    
    st.write(f"User ID: {st.session_state.user_id}")
    
    # Debug log display
    if 'debug_log' in st.session_state:
        st.write(f"Debug: {st.session_state.debug_log}")
    
    # Manual input for location
    lat = st.number_input("Latitude", value=-6.2088, format="%.6f", help="Enter latitude (e.g., -6.2088 for Jakarta)")
    lon = st.number_input("Longitude", value=106.8456, format="%.6f", help="Enter longitude (e.g., 106.8456 for Jakarta)")
    
    if st.button("Send Location"):
        save_location(st.session_state.user_id, lat, lon)
        st.success("Location sent successfully! Check the admin page to view it.")
    
    # Instructions
    st.info("Enter your coordinates and click 'Send Location' to share your position with the admin.")

# Admin page
def admin_page():
    st.title("GPS Tracking - Admin Dashboard")
    
    # Debug log display
    if 'debug_log' in st.session_state:
        st.write(f"Debug: {st.session_state.debug_log}")
    
    # Initialize map
    m = folium.Map(location=[-6.2088, 106.8456], zoom_start=10)  # Default: Jakarta
    
    # Get and display locations
    locations = get_all_locations()
    st.write(f"Debug: Found {len(locations)} locations")
    
    for loc in locations:
        folium.Marker(
            location=[loc['latitude'], loc['longitude']],
            popup=f"User: {loc['user_id']}<br>Time: {loc['timestamp']}",
            icon=folium.Icon(color='blue')
        ).add_to(m)
    
    # Render map
    st_folium(m, width=700, height=500)
    
    # Manual refresh button
    if st.button("Refresh Map"):
        st.rerun()
    
    st.info("Click 'Refresh Map' to update the map with the latest locations.")

# Main app
def main():
    # Initialize database
    init_db()
    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Page", ["User", "Admin"])
    
    if page == "User":
        user_page()
    else:
        admin_page()

if __name__ == "__main__":
    main()
