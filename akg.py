import streamlit as st
import pandas as pd

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Kalkulator AKG Anak Sekolah",
    page_icon="🍎",
    layout="wide"
)

# --- Judul dan Deskripsi ---
st.title("🍎 Kalkulator Angka Kecukupan Gizi (AKG)")
st.write(
    "Aplikasi ini membantu memperkirakan kebutuhan kalori dan gizi harian untuk anak usia sekolah "
    "berdasarkan rumus Harris-Benedict serta menampilkan tabel referensi AKG dari Kemenkes RI."
)
st.markdown("---")


# --- Bagian Tabel Referensi AKG Kemenkes ---
st.header("Tabel Referensi AKG (Kemenkes, PMK No. 28/2019)")

# Data untuk tabel AKG
data_akg = {
    'Kelompok Umur (Tahun)': ['7–9', '10–12', '10–12', '13–15', '13–15', '16–18', '16–18'],
    'Jenis Kelamin': ['L/P', 'Laki-laki', 'Perempuan', 'Laki-laki', 'Perempuan', 'Laki-laki', 'Perempuan'],
    'Energi (kkal)': [1650, 2000, 1900, 2400, 2050, 2650, 2100],
    'Protein (g)': [40, 50, 55, 70, 65, 75, 60],
    'Lemak (g)': [55, 65, 65, 80, 70, 85, 70],
    'Karbohidrat (g)': [250, 300, 280, 350, 300, 400, 300],
    'Serat (g)': [23, 28, 27, 34, 29, 37, 29],
    'Air (ml)': [1650, 1850, 1850, 2100, 2150, 2300, 2100]
}
df_akg = pd.DataFrame(data_akg)

# Menampilkan tabel
st.dataframe(df_akg, use_container_width=True)
st.info("Gunakan tabel di atas sebagai acuan utama standar gizi untuk populasi.")
st.markdown("---")


# --- Bagian Kalkulator Personal ---
st.header("Kalkulator Kebutuhan Kalori Personal")

# Fungsi untuk menghitung BMR (AMB)
def hitung_bmr(jenis_kelamin, berat, tinggi, usia):
    if jenis_kelamin == "Laki-laki":
        bmr = 66.5 + (13.75 * berat) + (5.003 * tinggi) - (6.75 * usia)
    else: # Perempuan
        bmr = 655.1 + (9.563 * berat) + (1.850 * tinggi) - (4.676 * usia)
    return bmr

# Membuat form untuk input
with st.form("kalkulator_akg_form"):
    col1, col2 = st.columns(2)

    with col1:
        jenis_kelamin = st.radio("Pilih Jenis Kelamin:", ("Laki-laki", "Perempuan"))
        usia = st.number_input("Usia (tahun)", min_value=7, max_value=18, value=10, step=1)
        
    with col2:
        berat = st.number_input("Berat Badan (kg)", min_value=10.0, max_value=150.0, value=30.0, step=0.5)
        tinggi = st.number_input("Tinggi Badan (cm)", min_value=100.0, max_value=220.0, value=130.0, step=0.5)

    aktivitas_options = {
        "Sangat Jarang (Sedentari)": 1.2,
        "Jarang (Olahraga 1-3x/minggu)": 1.375,
        "Cukup Aktif (Olahraga 3-5x/minggu)": 1.55,
        "Sangat Aktif (Olahraga 6-7x/minggu)": 1.725
    }
    aktivitas_label = st.selectbox("Pilih Tingkat Aktivitas Fisik:", aktivitas_options.keys())
    
    # Tombol submit form
    submitted = st.form_submit_button("Hitung Kebutuhan Gizi")

# Logika setelah tombol ditekan
if submitted:
    if berat > 0 and tinggi > 0 and usia > 0:
        faktor_aktivitas = aktivitas_options[aktivitas_label]
        
        # Hitung BMR
        bmr_value = hitung_bmr(jenis_kelamin, berat, tinggi, usia)
        
        # Hitung TDEE (Total Daily Energy Expenditure) / Total Kebutuhan Kalori
        tdee = bmr_value * faktor_aktivitas
        
        # Hitung Kebutuhan Gizi Makro (Protein, Lemak, Karbohidrat)
        protein_gram = (0.15 * tdee) / 4  # 15% dari total kalori, 1g protein = 4 kkal
        lemak_gram = (0.25 * tdee) / 9      # 25% dari total kalori, 1g lemak = 9 kkal
        karbo_gram = (0.60 * tdee) / 4      # 60% dari total kalori, 1g karbo = 4 kkal
        
        st.subheader("✅ Hasil Perhitungan Kebutuhan Gizi Harian Anda:")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Kebutuhan Energi", f"{tdee:.0f} kkal")
        col2.metric("Angka Metabolisme Basal (AMB)", f"{bmr_value:.0f} kkal")
        
        st.markdown("---")
        st.write("Rekomendasi Asupan Zat Gizi Makro:")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Karbohidrat (60%)", f"{karbo_gram:.0f} gram")
        col2.metric("Protein (15%)", f"{protein_gram:.0f} gram")
        col3.metric("Lemak (25%)", f"{lemak_gram:.0f} gram")
        
        st.success(
            f"Berdasarkan data yang dimasukkan, perkiraan kebutuhan energi harian anak adalah **{tdee:.0f} kkal**."
        )
        st.warning(
            "**Disclaimer:** Hasil ini adalah perkiraan berdasarkan rumus. Untuk kebutuhan gizi yang akurat dan "
            "penanganan kondisi medis tertentu, harap berkonsultasi dengan dokter atau ahli gizi profesional."
        )

    else:
        st.error("Mohon masukkan nilai Usia, Berat Badan, dan Tinggi Badan yang valid.")

# --- Footer ---
st.markdown("---")
st.markdown("Dibuat dengan Python & Streamlit")