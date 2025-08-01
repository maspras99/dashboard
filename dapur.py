import streamlit as st
import pandas as pd

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Perencana Menu Dapur MBG",
    page_icon="🍲",
    layout="wide"
)

# --- DATABASE ---
data_bahan_makanan = {
    "Nama Bahan": [
        "Nasi Putih", "Dada Ayam", "Paha Ayam", "Telur Ayam", "Tahu", "Tempe", 
        "Ikan Lele", "Susu Sapi", "Wortel", "Bayam", "Kentang", "Minyak Goreng"
    ],
    "Energi (kkal)": [
        130, 165, 209, 155, 80, 193, 105, 61, 41, 23, 77, 884
    ],
    "Protein (g)": [
        2.7, 31.0, 26.0, 13.0, 8.0, 19.0, 18.0, 3.4, 0.9, 2.9, 2.0, 0.0
    ],
    "Lemak (g)": [
        0.3, 3.6, 11.0, 11.0, 5.0, 11.0, 2.7, 3.3, 0.2, 0.4, 0.1, 100.0
    ],
    "Karbohidrat (g)": [
        28.0, 0.0, 0.0, 1.1, 1.9, 9.0, 0.0, 5.0, 10.0, 3.6, 17.0, 0.0
    ]
}
df_bahan = pd.DataFrame(data_bahan_makanan)

data_akg = {
    'Kelompok Umur': [
        '7–9 tahun', '10–12 tahun (L)', '10–12 tahun (P)', 
        '13–15 tahun (L)', '13–15 tahun (P)', '16–18 tahun (L)', '16–18 tahun (P)'
    ],
    'Energi (kkal)': [1650, 2000, 1900, 2400, 2050, 2650, 2100],
    'Protein (g)': [40, 50, 55, 70, 65, 75, 60],
    'Lemak (g)': [55, 65, 65, 80, 70, 85, 70],
    'Karbohidrat (g)': [250, 300, 280, 350, 300, 400, 300]
}
df_akg = pd.DataFrame(data_akg).set_index('Kelompok Umur')

# --- Inisialisasi Session State ---
if 'menu_items' not in st.session_state:
    st.session_state.menu_items = []

# --- Fungsi ---
def calculate_nutrition(bahan_nama, berat_gram):
    bahan_data = df_bahan[df_bahan['Nama Bahan'] == bahan_nama].iloc[0]
    faktor = berat_gram / 100.0
    return {
        'Nama Bahan': bahan_nama,
        'Berat (g)': berat_gram,
        'Energi (kkal)': bahan_data['Energi (kkal)'] * faktor,
        'Protein (g)': bahan_data['Protein (g)'] * faktor,
        'Lemak (g)': bahan_data['Lemak (g)'] * faktor,
        'Karbohidrat (g)': bahan_data['Karbohidrat (g)'] * faktor
    }

# --- TAMPILAN APLIKASI ---
with st.sidebar:
    st.header("⚙️ Perencana Menu")
    
    st.subheader("1. Pilih Target Sasaran")
    target_kelompok_umur = st.selectbox(
        "Kelompok Umur Anak Sekolah",
        options=df_akg.index.tolist()
    )
    
    st.markdown("---")

    st.subheader("2. Tambah Bahan ke Menu")
    bahan_terpilih = st.selectbox(
        "Pilih Bahan Makanan",
        options=df_bahan['Nama Bahan'].tolist()
    )
    berat_terpilih = st.number_input("Berat (gram)", min_value=1, value=100)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Tambah Bahan", use_container_width=True):
            nutrisi_bahan = calculate_nutrition(bahan_terpilih, berat_terpilih)
            st.session_state.menu_items.append(nutrisi_bahan)
            st.success(f"{bahan_terpilih} ({berat_terpilih}g) ditambahkan!")
            
    with col2:
        if st.button("🔄 Reset Menu", use_container_width=True, type="primary"):
            st.session_state.menu_items = []
            st.rerun()

st.title("🍲 Aplikasi Perencanaan Menu Dapur MBG")

st.header("🎯 Target Kebutuhan Gizi (AKG)")
target_gizi = df_akg.loc[target_kelompok_umur]
st.write(f"Target untuk kelompok umur **{target_kelompok_umur}** adalah:")
st.table(target_gizi)

st.markdown("---")

st.header("📝 Menu yang Direncanakan")
if not st.session_state.menu_items:
    st.info("Menu masih kosong. Silakan tambah bahan makanan melalui panel di sebelah kiri.")
else:
    df_menu = pd.DataFrame(st.session_state.menu_items)
    
    format_dict = {
        'Berat (g)': '{:.0f}',
        'Energi (kkal)': '{:.1f}',
        'Protein (g)': '{:.1f}',
        'Lemak (g)': '{:.1f}',
        'Karbohidrat (g)': '{:.1f}'
    }
    st.dataframe(df_menu.style.format(format_dict))

    st.markdown("---")
    
    st.header("📊 Analisis Pemenuhan Gizi")

    total_gizi = df_menu[['Energi (kkal)', 'Protein (g)', 'Lemak (g)', 'Karbohidrat (g)']].sum()

    persen_energi = (total_gizi['Energi (kkal)'] / target_gizi['Energi (kkal)'])
    persen_protein = (total_gizi['Protein (g)'] / target_gizi['Protein (g)'])
    persen_lemak = (total_gizi['Lemak (g)'] / target_gizi['Lemak (g)'])
    persen_karbo = (total_gizi['Karbohidrat (g)'] / target_gizi['Karbohidrat (g)'])
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Energi**")
        st.text(f"{total_gizi['Energi (kkal)']:.1f} / {target_gizi['Energi (kkal)']} kkal ({persen_energi:.1%})")
        # --- PERBAIKAN DI SINI ---
        st.progress(min(persen_energi, 1.0))

        st.write("**Protein**")
        st.text(f"{total_gizi['Protein (g)']:.1f} / {target_gizi['Protein (g)']} g ({persen_protein:.1%})")
        # --- PERBAIKAN DI SINI ---
        st.progress(min(persen_protein, 1.0))

    with col2:
        st.write("**Lemak**")
        st.text(f"{total_gizi['Lemak (g)']:.1f} / {target_gizi['Lemak (g)']} g ({persen_lemak:.1%})")
        # --- PERBAIKAN DI SINI ---
        st.progress(min(persen_lemak, 1.0))

        st.write("**Karbohidrat**")
        st.text(f"{total_gizi['Karbohidrat (g)']:.1f} / {target_gizi['Karbohidrat (g)']} g ({persen_karbo:.1%})")
        # --- PERBAIKAN DI SINI ---
        st.progress(min(persen_karbo, 1.0))
        
    if persen_energi >= 0.9 and persen_protein >= 0.9:
        st.success("👍 Menu ini sudah baik dan mendekati target pemenuhan energi dan protein!")
    else:
        st.warning("⚠️ Perhatian: Kandungan gizi menu belum mencapai target. Coba tambahkan atau sesuaikan bahan makanan.")