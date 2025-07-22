import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation
from datetime import datetime

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="GPS Tracker dengan Keterangan",
    page_icon="🗺️",
    layout="wide"
)

# Judul aplikasi
st.title("🗺️ Pelacak Lokasi GPS dengan Keterangan")
st.markdown("Aplikasi ini melacak lokasi, memungkinkan Anda menambah keterangan, dan menampilkannya di peta.")

# Inisialisasi session_state untuk menyimpan riwayat lokasi
if 'history' not in st.session_state:
    st.session_state.history = []

# Buat dua kolom: satu untuk kontrol, satu untuk peta
col1, col2 = st.columns([1, 2])

with col1:
    st.header("Kontrol")
    
    # Dapatkan lokasi menggunakan streamlit_geolocation
    location = streamlit_geolocation()
    
    # Tambahkan input untuk keterangan
    keterangan = st.text_input("Tambahkan Keterangan", placeholder="Contoh: Kantor Pusat, Gudang A, dll.")

    # Tombol untuk mensubmit lokasi
    if st.button("📍 Submit Lokasi dan Keterangan"):
        if location and location['latitude'] is not None:
            # Dapatkan waktu saat ini
            now = datetime.now()
            timestamp = now.strftime("%d %B %Y, %H:%M:%S")

            # Tambahkan data ke riwayat di session_state
            st.session_state.history.append({
                "latitude": location['latitude'],
                "longitude": location['longitude'],
                "timestamp": timestamp,
                "keterangan": keterangan or "Tanpa Keterangan" # Default value if empty
            })
            st.success(f"Lokasi berhasil direkam: '{keterangan}'")
        else:
            st.error("Gagal mendapatkan lokasi. Pastikan Anda memberikan izin lokasi.")

    # Menampilkan data mentah dari GPS
    st.subheader("Data Lokasi Mentah")
    st.write(location)

with col2:
    st.header("Peta Lokasi")

    # Tentukan lokasi tengah peta
    if st.session_state.history:
        map_center = [st.session_state.history[-1]['latitude'], st.session_state.history[-1]['longitude']]
        zoom_start = 15
    else:
        # Lokasi default (Bandung, Indonesia)
        map_center = [-6.9175, 107.6191]
        zoom_start = 12

    # Buat peta Folium
    m = folium.Map(location=map_center, zoom_start=zoom_start)

    # Tambahkan marker untuk setiap lokasi dalam riwayat
    for record in st.session_state.history:
        # Format teks untuk popup di marker
        popup_text = f"""
            <b>Keterangan:</b> {record['keterangan']}<br>
            <b>Direkam pada:</b><br>{record['timestamp']}
        """
        
        folium.Marker(
            location=[record['latitude'], record['longitude']],
            popup=popup_text,
            tooltip=record['keterangan'], # Teks yang muncul saat mouse hover
            icon=folium.Icon(color='green', icon='home')
        ).add_to(m)

    # Tampilkan peta di Streamlit
    st_folium(m, width=700, height=500)

# Menampilkan riwayat dalam bentuk tabel di bawah
if st.session_state.history:
    st.subheader("Riwayat Lokasi yang Direkam")
    df = pd.DataFrame(st.session_state.history)
    # Atur ulang urutan kolom agar lebih rapi
    st.dataframe(df[['timestamp', 'keterangan', 'latitude', 'longitude']])