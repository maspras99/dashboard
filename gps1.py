import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation
from datetime import datetime
import os

# --- Konfigurasi dan Fungsi Database ---
DB_FILE = "database_lokasi.xlsx"

# Fungsi untuk memuat data dari file Excel
def load_data(file_path):
    if os.path.exists(file_path):
        try:
            return pd.read_excel(file_path)
        except Exception as e:
            st.error(f"Gagal memuat file Excel: {e}")
            return pd.DataFrame(columns=["timestamp", "keterangan", "latitude", "longitude"])
    else:
        return pd.DataFrame(columns=["timestamp", "keterangan", "latitude", "longitude"])

# Fungsi untuk menyimpan data ke file Excel
def save_data(df, file_path):
    df.to_excel(file_path, index=False)

# --- Aplikasi Streamlit ---

# Konfigurasi halaman
st.set_page_config(
    page_title="GPS Tracker (Database Excel)",
    page_icon="🗺️",
    layout="wide"
)

# Judul aplikasi
st.title("🗺️ Pelacak Lokasi GPS dengan Database Excel")
st.markdown("Semua data lokasi disimpan di file `database_lokasi.xlsx`. Jika file ini dihapus, semua rekaman akan hilang.")

# Muat data dari Excel saat aplikasi dimulai
df_history = load_data(DB_FILE)
history_list = df_history.to_dict('records')

# Buat dua kolom
col1, col2 = st.columns([1, 2])

with col1:
    st.header("Kontrol")
    
    location = streamlit_geolocation()
    
    keterangan = st.text_input("Tambahkan Keterangan", placeholder="Contoh: Kantor Pusat, Gudang A, dll.")

    if st.button("📍 Submit Lokasi dan Keterangan"):
        if location and location['latitude'] is not None:
            now = datetime.now()
            timestamp = now.strftime("%d %B %Y, %H:%M:%S")

            new_data = pd.DataFrame([{
                "timestamp": timestamp,
                "keterangan": keterangan or "Tanpa Keterangan",
                "latitude": location['latitude'],
                "longitude": location['longitude']
            }])

            df_history = pd.concat([df_history, new_data], ignore_index=True)
            
            save_data(df_history, DB_FILE)
            
            st.success(f"Lokasi berhasil disimpan ke Excel: '{keterangan}'")
            
            # Gunakan st.rerun() yang merupakan versi baru
            st.rerun()
            
        else:
            st.error("Gagal mendapatkan lokasi. Pastikan Anda memberikan izin lokasi.")

    st.subheader("Data Lokasi Mentah")
    st.write(location)

with col2:
    st.header("Peta Lokasi")

    if not df_history.empty:
        map_center = [df_history.iloc[-1]['latitude'], df_history.iloc[-1]['longitude']]
        zoom_start = 15
    else:
        map_center = [-6.9175, 107.6191] # Default: Bandung
        zoom_start = 12

    m = folium.Map(location=map_center, zoom_start=zoom_start)

    for record in history_list:
        popup_text = f"""
            <b>Keterangan:</b> {record['keterangan']}<br>
            <b>Direkam pada:</b><br>{record['timestamp']}
        """
        folium.Marker(
            location=[record['latitude'], record['longitude']],
            popup=popup_text,
            tooltip=record['keterangan'],
            icon=folium.Icon(color='green', icon='home')
        ).add_to(m)

    st_folium(m, width=700, height=500)

st.subheader("Riwayat Lokasi dari File Excel")
if not df_history.empty:
    st.dataframe(df_history)
else:
    st.info("Belum ada data yang direkam di file Excel.")
