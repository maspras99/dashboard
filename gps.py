import streamlit as st
import sqlite3
import folium
from streamlit_folium import st_folium
import uuid
from datetime import datetime
import threading

# SQLite database initialization
DB_FILE = "locations.db"
lock = threading.Lock()  # Lock untuk mencegah konkurensi SQLite

def init_db():
    with lock:
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
    with lock:
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
    with lock:
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
    
    # JavaScript for automatic Geolocation with retry logic
    st.components.v1.html("""
    <script>
        // Cek apakah script sudah di-load
        if (!window.geolocationScriptLoaded) {
            window.geolocationScriptLoaded = true;
            
            function getLocation(retryCount = 3, timeout = 15000) {
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
                            let errorMessage = "Failed to get location: " + error.message + ". ";
                            if (error.code === error.TIMEOUT && retryCount > 0) {
                                console.log("Retrying Geolocation, attempts left:", retryCount - 1);
                                setTimeout(() => getLocation(retryCount - 1, timeout), 1000);
                            } else if (error.code === error.TIMEOUT) {
                                errorMessage += "Try moving to an open area or enabling Wi-Fi/GPS.";
                            } else if (error.code === error.PERMISSION_DENIED) {
                                errorMessage += "Please enable location access in your browser settings.";
                            } else if (error.code === error.POSITION_UNAVAILABLE) {
                                errorMessage += "Ensure GPS is enabled and try again.";
                            }
                            alert(errorMessage + " You can use manual input below as a fallback.");
                        },
                        { timeout: timeout, maximumAge: 60000, enableHighAccuracy: true }
                    );
                } else {
                    console.error("Geolocation not supported");
                    window.parent.postMessage({
                        type: 'STREAMLIT_UPDATE',
                        error: "Geolocation not supported by this browser"
                    }, '*');
                    alert("Geolocation not supported. Please use manual input below.");
                }
            }
            // Panggil sekali saat halaman dimuat
            getLocation();
        }
    </script>
    """, height=0, key="geolocation_script")
    
    # Handle JavaScript messages
    if st.session_state.get('streamlit_update'):
        data = st.session_state.streamlit_update
        if 'latitude' in data and 'longitude' in data:
            save_location(st.session_state.user_id, data['latitude'], data['longitude'])
            st.success(f"Automatic location sent: ({data['latitude']}, {data['longitude']})")
        if 'error' in data:
            st.error(f"Geolocation Error: {data['error']}")
    
    # Manual input for location
    lat = st.number_input("Latitude (for testing)", value=-6.2088, format="%.6f", help="Enter latitude (e.g., -6.2088 for Jakarta)")
    lon = st.number_input("Longitude (for testing)", value=106.8456, format="%.6f", help="Enter longitude (e.g., 106.8456 for Jakarta)")
    
    if st.button("Send Manual Location"):
        save_location(st.session_state.user_id, lat, lon)
        st.success("Manual location sent successfully! Check the admin page to view it.")
    
    # Instructions
    st.info("Your location is automatically sent when the page loads if GPS is enabled. If it fails, ensure GPS/Wi-Fi is enabled, allow location access, and try refreshing. Use manual input as a fallback.")

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
