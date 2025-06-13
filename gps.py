import streamlit as st
import sqlite3
import folium
from streamlit_folium import st_folium
import uuid
import time
from datetime import datetime
import os

# SQLite database initialization
DB_FILE = "locations.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
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
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        timestamp = datetime.now().isoformat()
        c.execute('INSERT OR REPLACE INTO locations (user_id, latitude, longitude, timestamp) VALUES (?, ?, ?, ?)',
                  (user_id, lat, lon, timestamp))
        conn.commit()
        st.session_state.debug_log = f"Location saved for user {user_id}: ({lat}, {lon}) at {timestamp}"
    except Exception as e:
        st.session_state.debug_log = f"Error saving location: {str(e)}"
    finally:
        conn.close()

# Retrieve all locations from SQLite
def get_all_locations():
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('SELECT user_id, latitude, longitude, timestamp FROM locations')
        locations = [{"user_id": row[0], "latitude": row[1], "longitude": row[2], "timestamp": row[3]} for row in c.fetchall()]
        conn.close()
        return locations
    except Exception as e:
        st.session_state.debug_log = f"Error retrieving locations: {str(e)}"
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
    
    # JavaScript for Geolocation with error handling
    st.components.v1.html("""
    <script>
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        console.log("Location:", position.coords.latitude, position.coords.longitude);
                        window.parent.postMessage({
                            type: 'STREAMLIT_UPDATE',
                            latitude: position.coords.latitude,
                            longitude: position.coords.longitude
                        }, '*');
                    },
                    (error) => {
                        console.error("Geolocation error:", error.message);
                        window.parent.postMessage({
                            type: 'STREAMLIT_UPDATE',
                            error: error.message
                        }, '*');
                    }
                );
            } else {
                console.error("Geolocation not supported");
                window.parent.postMessage({
                    type: 'STREAMLIT_UPDATE',
                    error: "Geolocation not supported by this browser"
                }, '*');
            }
        }
        setInterval(getLocation, 10000);
        getLocation();
    </script>
    """, height=0)
    
    # Handle JavaScript messages
    if 'latitude' in st.session_state and 'longitude' in st.session_state:
        save_location(st.session_state.user_id, st.session_state.latitude, st.session_state.longitude)
    elif 'error' in st.session_state:
        st.error(f"Geolocation Error: {st.session_state.error}")
    
    # Manual input for testing
    lat = st.number_input("Latitude (for testing)", value=0.0, format="%.6f")
    lon = st.number_input("Longitude (for testing)", value=0.0, format="%.6f")
    if st.button("Send Manual Location"):
        save_location(st.session_state.user_id, lat, lon)
        st.success("Manual location sent!")

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
    
    # Auto-refresh
    st.write("Map refreshes every 10 seconds...")
    time.sleep(10)
    st.rerun()

# Main app
def main():
    # Initialize database
    init_db()
    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Page", ["User", "Admin"])
    
    # Handle JavaScript messages
    if st.session_state.get('streamlit_update'):
        data = st.session_state.streamlit_update
        if 'latitude' in data and 'longitude' in data:
            st.session_state.latitude = data['latitude']
            st.session_state.longitude = data['longitude']
        if 'error' in data:
            st.session_state.error = data['error']
    
    if page == "User":
        user_page()
    else:
        admin_page()

if __name__ == "__main__":
    main()
