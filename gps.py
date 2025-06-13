import streamlit as st
import json
import os
from datetime import datetime
import time
import folium
from streamlit_folium import st_folium
import uuid

# File untuk menyimpan data lokasi sementara
DATA_FILE = "locations.json"

# Fungsi untuk menyimpan lokasi pengguna
def save_location(user_id, lat, lon):
    timestamp = datetime.now().isoformat()
    location_data = {
        "user_id": user_id,
        "latitude": lat,
        "longitude": lon,
        "timestamp": timestamp
    }
    
    # Baca data existing
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    
    # Tambahkan atau update data lokasi
    data = [d for d in data if d['user_id'] != user_id]  # Hapus data lama untuk user ini
    data.append(location_data)
    
    # Simpan ke file
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Fungsi untuk membaca semua lokasi
def get_all_locations():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# Halaman pengguna
def user_page():
    st.title("GPS Tracking - User")
    
    # Generate ID unik untuk pengguna
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
    
    st.write(f"User ID: {st.session_state.user_id}")
    
    # JavaScript untuk mendapatkan lokasi
    st.components.v1.html("""
    <script>
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        // Kirim data ke Streamlit
                        window.parent.postMessage({
                            type: 'STREAMLIT_UPDATE',
                            latitude: position.coords.latitude,
                            longitude: position.coords.longitude
                        }, '*');
                    },
                    (error) => {
                        console.error("Error getting location:", error);
                    }
                );
            }
        }
        
        // Update lokasi setiap 10 detik
        setInterval(getLocation, 10000);
        getLocation();
    </script>
    """, height=0)
    
    # Input manual untuk testing
    lat = st.number_input("Latitude (untuk testing)", value=0.0, format="%.6f")
    lon = st.number_input("Longitude (untuk testing)", value=0.0, format="%.6f")
    
    if st.button("Kirim Lokasi Manual"):
        save_location(st.session_state.user_id, lat, lon)
        st.success("Lokasi dikirim!")

# Halaman admin
def admin_page():
    st.title("GPS Tracking - Admin Dashboard")
    
    # Inisialisasi peta menggunakan Folium
    m = folium.Map(location=[-6.2088, 106.8456], zoom_start=10)  # Default: Jakarta
    
    # Ambil data lokasi
    locations = get_all_locations()
    
    # Tambahkan marker untuk setiap pengguna
    for loc in locations:
        folium.Marker(
            location=[loc['latitude'], loc['longitude']],
            popup=f"User: {loc['user_id']}<br>Time: {loc['timestamp']}",
            icon=folium.Icon(color='blue')
        ).add_to(m)
    
    # Tampilkan peta
    st_folium(m, width=700, height=500)
    
    # Auto-refresh
    st.write("Peta akan refresh otomatis setiap 10 detik...")
    time.sleep(10)
    st.rerun()

# Main app
def main():
    st.sidebar.title("Navigasi")
    page = st.sidebar.radio("Pilih Halaman", ["User", "Admin"])
    
    if page == "User":
        user_page()
    else:
        admin_page()

if __name__ == "__main__":
    main()