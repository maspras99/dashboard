import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import sqlite3
import plotly.express as px
import uuid

# Koneksi ke database SQLite
conn = sqlite3.connect('construction_management.db')
cursor = conn.cursor()

# Inisialisasi database
cursor.execute('''
CREATE TABLE IF NOT EXISTS inventory (
    id TEXT PRIMARY KEY,
    item_code TEXT,
    item_name TEXT,
    quantity INTEGER,
    unit TEXT,
    location TEXT,
    last_updated TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS schedule (
    id TEXT PRIMARY KEY,
    activity TEXT,
    duration INTEGER,
    start_date TEXT,
    end_date TEXT,
    dependency TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS usage_history (
    id TEXT PRIMARY KEY,
    item_name TEXT,
    quantity_used INTEGER,
    date_used TEXT
)
''')
conn.commit()

# Fungsi untuk menghasilkan UUID
def generate_uuid():
    return str(uuid.uuid4())

# Fungsi untuk memprediksi kebutuhan material menggunakan AI (Linear Regression)
def predict_material_needed(item_name, historical_data):
    if len(historical_data) < 2:
        return 0  # Tidak cukup data untuk prediksi
    X = np.array(range(len(historical_data))).reshape(-1, 1)
    y = historical_data['quantity_used'].values
    model = LinearRegression()
    model.fit(X, y)
    next_period = len(historical_data)
    prediction = model.predict([[next_period]])
    return max(0, int(prediction[0]))

# Streamlit App
st.title("Sistem Manajemen Proyek Konstruksi")

# Sidebar untuk navigasi
st.sidebar.title("Navigasi")
page = st.sidebar.radio("Pilih Halaman", ["Dashboard", "Manajemen Inventaris", "Jadwal Proyek", "Prediksi Material (AI)"])

# Halaman Dashboard
if page == "Dashboard":
    st.header("Dashboard Proyek")
    st.write("Ringkasan status proyek dan inventaris.")
    
    # Menampilkan jumlah total item di inventaris
    cursor.execute("SELECT SUM(quantity) FROM inventory")
    total_items = cursor.fetchone()[0] or 0
    st.metric("Total Barang di Inventaris", total_items)
    
    # Menampilkan jadwal proyek
    schedule_df = pd.read_sql_query("SELECT activity, start_date, end_date FROM schedule", conn)
    if not schedule_df.empty:
        st.subheader("Jadwal Proyek")
        st.dataframe(schedule_df)
        
        # Visualisasi jadwal dengan Plotly
        fig = px.timeline(schedule_df, x_start="start_date", x_end="end_date", y="activity", title="Jadwal Proyek")
        st.plotly_chart(fig)

# Halaman Manajemen Inventaris
elif page == "Manajemen Inventaris":
    st.header("Manajemen Inventaris")
    
    # Tambah item baru
    st.subheader("Tambah Item Baru")
    with st.form("add_item_form"):
        item_code = st.text_input("Kode Barang")
        item_name = st.text_input("Nama Barang")
        quantity = st.number_input("Jumlah", min_value=0, step=1)
        unit = st.text_input("Satuan (contoh: Buah, Meter)")
        location = st.text_input("Lokasi Penyimpanan")
        submit_item = st.form_submit_button("Tambah Item")
        
        if submit_item:
            cursor.execute('''
            INSERT INTO inventory (id, item_code, item_name, quantity, unit, location, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (generate_uuid(), item_code, item_name, quantity, unit, location, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            st.success("Item berhasil ditambahkan!")
    
    # Tampilkan inventaris
    st.subheader("Daftar Inventaris")
    inventory_df = pd.read_sql_query("SELECT item_code, item_name, quantity, unit, location, last_updated FROM inventory", conn)
    st.dataframe(inventory_df)
    
    # Update stok
    st.subheader("Update Stok")
    selected_item = st.selectbox("Pilih Barang", inventory_df['item_name'] if not inventory_df.empty else [])
    update_quantity = st.number_input("Jumlah Baru", min_value=0, step=1)
    if st.button("Update Stok"):
        cursor.execute("UPDATE inventory SET quantity = ?, last_updated = ? WHERE item_name = ?",
                       (update_quantity, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), selected_item))
        conn.commit()
        st.success("Stok berhasil diperbarui!")
    
    # Catat penggunaan barang
    st.subheader("Catat Penggunaan Barang")
    with st.form("usage_form"):
        usage_item = st.selectbox("Pilih Barang untuk Penggunaan", inventory_df['item_name'] if not inventory_df.empty else [])
        usage_quantity = st.number_input("Jumlah Digunakan", min_value=0, step=1)
        submit_usage = st.form_submit_button("Catat Penggunaan")
        
        if submit_usage:
            cursor.execute("SELECT quantity FROM inventory WHERE item_name = ?", (usage_item,))
            current_quantity = cursor.fetchone()[0]
            if current_quantity >= usage_quantity:
                cursor.execute("UPDATE inventory SET quantity = quantity - ?, last_updated = ? WHERE item_name = ?",
                               (usage_quantity, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), usage_item))
                cursor.execute("INSERT INTO usage_history (id, item_name, quantity_used, date_used) VALUES (?, ?, ?, ?)",
                               (generate_uuid(), usage_item, usage_quantity, datetime.now().strftime("%Y-%m-%d")))
                conn.commit()
                st.success("Penggunaan barang berhasil dicatat!")
            else:
                st.error("Stok tidak cukup!")

# Halaman Jadwal Proyek
elif page == "Jadwal Proyek":
    st.header("Manajemen Jadwal Proyek")
    
    # Tambah aktivitas baru
    st.subheader("Tambah Aktivitas")
    with st.form("add_schedule_form"):
        activity = st.text_input("Nama Aktivitas")
        duration = st.number_input("Durasi (hari)", min_value=1, step=1)
        start_date = st.date_input("Tanggal Mulai")
        dependency = st.text_input("Ketergantungan (opsional)")
        submit_schedule = st.form_submit_button("Tambah Aktivitas")
        
        if submit_schedule:
            end_date = (start_date + timedelta(days=duration)).strftime("%Y-%m-%d")
            start_date = start_date.strftime("%Y-%m-%d")
            cursor.execute('''
            INSERT INTO schedule (id, activity, duration, start_date, end_date, dependency)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (generate_uuid(), activity, duration, start_date, end_date, dependency))
            conn.commit()
            st.success("Aktivitas berhasil ditambahkan!")
    
    # Tampilkan jadwal
    st.subheader("Daftar Jadwal")
    schedule_df = pd.read_sql_query("SELECT activity, duration, start_date, end_date, dependency FROM schedule", conn)
    st.dataframe(schedule_df)

# Halaman Prediksi Material (AI)
elif page == "Prediksi Material (AI)":
    st.header("Prediksi Kebutuhan Material (Berbasis AI)")
    st.write("Gunakan data historis untuk memprediksi kebutuhan material di masa depan.")
    
    # Pilih barang untuk prediksi
    inventory_df = pd.read_sql_query("SELECT item_name FROM inventory", conn)
    selected_item = st.selectbox("Pilih Barang untuk Prediksi", inventory_df['item_name'] if not inventory_df.empty else [])
    
    if selected_item:
        usage_history = pd.read_sql_query("SELECT quantity_used, date_used FROM usage_history WHERE item_name = ?", conn, params=(selected_item,))
        if not usage_history.empty:
            st.subheader(f"Prediksi untuk {selected_item}")
            prediction = predict_material_needed(selected_item, usage_history)
            st.write(f"Prediksi kebutuhan untuk periode berikutnya: **{prediction}** unit")
            
            # Visualisasi data historis
            fig = px.line(usage_history, x="date_used", y="quantity_used", title=f"Riwayat Penggunaan {selected_item}")
            st.plotly_chart(fig)
        else:
            st.warning("Tidak ada data historis untuk barang ini.")

# Tutup koneksi database saat aplikasi selesai
conn.close()
