import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import json
import hashlib
import qrcode
from io import BytesIO
import base64

# Konfigurasi halaman
st.set_page_config(
    page_title="Monitoring Makan Bergizi Gratis",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS untuk styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .success-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .warning-box {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .stSelectbox > div > div {
        background-color: #f8f9fa;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Inisialisasi session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# Data dummy untuk demo
if 'lembaga_data' not in st.session_state:
    st.session_state.lembaga_data = [
        {"id": "LP001", "nama": "SDN Bandung 1", "alamat": "Jl. Merdeka No. 1", "kontak": "022-1234567"},
        {"id": "LP002", "nama": "SMP Negeri 5", "alamat": "Jl. Sudirman No. 25", "kontak": "022-7654321"},
        {"id": "LP003", "nama": "SMA Negeri 3", "alamat": "Jl. Asia Afrika No. 10", "kontak": "022-9876543"}
    ]

if 'penerima_data' not in st.session_state:
    st.session_state.penerima_data = [
        {"nama": "Ahmad Rizki", "ttl": "Bandung, 15 Mei 2010", "jenis_kelamin": "Laki-laki", "bb": 35, "tb": 140, "lembaga": "SDN Bandung 1"},
        {"nama": "Siti Nurhaliza", "ttl": "Bandung, 22 Juli 2009", "jenis_kelamin": "Perempuan", "bb": 32, "tb": 135, "lembaga": "SDN Bandung 1"},
        {"nama": "Budi Santoso", "ttl": "Bandung, 8 Maret 2011", "jenis_kelamin": "Laki-laki", "bb": 28, "tb": 125, "lembaga": "SDN Bandung 1"}
    ]

if 'menu_makanan' not in st.session_state:
    st.session_state.menu_makanan = [
        {"nama": "Nasi + Ayam Bakar + Sayur", "kalori": 650, "protein": 35, "karbohidrat": 75, "lemak": 18},
        {"nama": "Nasi + Ikan Gurame + Tahu", "kalori": 580, "protein": 32, "karbohidrat": 70, "lemak": 15},
        {"nama": "Nasi + Rendang + Kangkung", "kalori": 720, "protein": 38, "karbohidrat": 80, "lemak": 22},
        {"nama": "Nasi + Tempe Goreng + Gado-gado", "kalori": 520, "protein": 25, "karbohidrat": 68, "lemak": 12}
    ]

if 'kuota_makanan' not in st.session_state:
    st.session_state.kuota_makanan = [
        {"lembaga": "SDN Bandung 1", "tanggal": "2025-01-31", "menu": "Nasi + Ayam Bakar + Sayur", "kuota": 150, "terpakai": 120},
        {"lembaga": "SMP Negeri 5", "tanggal": "2025-01-31", "menu": "Nasi + Ikan Gurame + Tahu", "kuota": 200, "terpakai": 180},
        {"lembaga": "SMA Negeri 3", "tanggal": "2025-01-31", "menu": "Nasi + Rendang + Kangkung", "kuota": 180, "terpakai": 160}
    ]

if 'pesanan_logistik' not in st.session_state:
    st.session_state.pesanan_logistik = []

if 'pengaduan' not in st.session_state:
    st.session_state.pengaduan = []

def generate_qr_code(data):
    """Generate QR Code"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return base64.b64encode(buffer.getvalue()).decode()

def hash_password(password):
    """Hash password sederhana"""
    return hashlib.sha256(password.encode()).hexdigest()

def login_page():
    """Halaman Login"""
    st.markdown('<div class="main-header"><h1>🍽️ Sistem Monitoring Makan Bergizi Gratis</h1><p>Memastikan Nutrisi Terbaik untuk Generasi Masa Depan</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login Sistem")
        
        role = st.selectbox(
            "Pilih Role:",
            ["Admin", "Lembaga Pendidikan", "Logistik", "Produsen Makanan"]
        )
        
        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")
        
        if st.button("🚀 Login", use_container_width=True):
            # Demo login - dalam implementasi nyata, gunakan database
            if username and password:
                st.session_state.logged_in = True
                st.session_state.user_role = role
                st.session_state.user_data = {"username": username, "role": role}
                st.rerun()
            else:
                st.error("Please enter username and password!")

def admin_dashboard():
    """Dashboard Admin"""
    st.markdown('<div class="main-header"><h1>👨‍💼 Dashboard Admin</h1></div>', unsafe_allow_html=True)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-container"><h3>🏫 Lembaga</h3><h2>3</h2></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container"><h3>👥 Penerima</h3><h2>850</h2></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container"><h3>🍽️ Makanan Hari Ini</h3><h2>460</h2></div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-container"><h3>📊 Efisiensi</h3><h2>92%</h2></div>', unsafe_allow_html=True)
    
    # Tabs untuk berbagai fungsi admin
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Data Input", "🍽️ Data AKG", "🏭 Data Produsen", "📍 Data Kuota", "🏫 Data Lembaga"])
    
    with tab1:
        st.subheader("📊 Analisis & Peta Logistik")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Chart distribusi makanan
            data = pd.DataFrame({
                'Lembaga': ['SDN Bandung 1', 'SMP Negeri 5', 'SMA Negeri 3'],
                'Makanan Terdistribusi': [120, 180, 160],
                'Target': [150, 200, 180]
            })
            
            fig = px.bar(data, x='Lembaga', y=['Makanan Terdistribusi', 'Target'], 
                        title="📈 Distribusi Makanan vs Target", barmode='group')
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Pie chart ketercapaian AKG
            akg_data = pd.DataFrame({
                'Status': ['Tercukupi', 'Kurang', 'Berlebih'],
                'Jumlah': [65, 25, 10]
            })
            
            fig = px.pie(akg_data, values='Jumlah', names='Status', 
                        title="🥗 Ketercapaian AKG Penerima")
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("🍽️ Data Angka Kecukupan Gizi (AKG)")
        
        akg_data = pd.DataFrame({
            'Kelompok Umur': ['4-6 tahun', '7-9 tahun', '10-12 tahun', '13-15 tahun', '16-18 tahun'],
            'Kalori (kkal)': [1600, 1850, 2100, 2400, 2650],
            'Protein (g)': [35, 49, 56, 70, 75],
            'Karbohidrat (g)': [220, 254, 289, 330, 364],
            'Lemak (g)': [53, 62, 70, 80, 88]
        })
        
        st.dataframe(akg_data, use_container_width=True)
        
        if st.button("📝 Tambah Data AKG"):
            st.success("Fitur tambah data AKG akan ditambahkan!")
    
    with tab3:
        st.subheader("🏭 Data Produsen Makanan")
        
        produsen_data = pd.DataFrame({
            'Nama Produsen': ['Katering Sehat Bandung', 'Nutrisi Prima', 'Makanan Bergizi Nusantara'],
            'Alamat': ['Jl. Setiabudi No. 15', 'Jl. Dago No. 88', 'Jl. Cihampelas No. 45'],
            'Kapasitas/Hari': [500, 750, 600],
            'Rating': [4.8, 4.6, 4.7],
            'Status': ['Aktif', 'Aktif', 'Aktif']
        })
        
        st.dataframe(produsen_data, use_container_width=True)
        
        if st.button("➕ Tambah Produsen"):
            st.success("Fitur tambah produsen akan ditambahkan!")
    
    with tab4:
        st.subheader("📍 Data Kuota Makanan")
        
        kuota_df = pd.DataFrame(st.session_state.kuota_makanan)
        st.dataframe(kuota_df, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Edit Kuota"):
                st.info("Fitur edit kuota akan ditambahkan!")
        with col2:
            if st.button("📊 Laporan Kuota"):
                st.info("Generating laporan kuota...")
    
    with tab5:
        st.subheader("🏫 Data Lembaga Pendidikan")
        
        lembaga_df = pd.DataFrame(st.session_state.lembaga_data)
        st.dataframe(lembaga_df, use_container_width=True)
        
        if st.button("➕ Tambah Lembaga"):
            st.success("Fitur tambah lembaga akan ditambahkan!")

def lembaga_dashboard():
    """Dashboard Lembaga Pendidikan"""
    st.markdown('<div class="main-header"><h1>🏫 Dashboard Lembaga Pendidikan</h1></div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Data Penerima", "🔍 Biometrik", "🍽️ Penerimaan Makanan", "📞 Pengaduan", "📊 Catatan Penyimpangan"])
    
    with tab1:
        st.subheader("👥 Data Penerima MBG")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            penerima_df = pd.DataFrame(st.session_state.penerima_data)
            st.dataframe(penerima_df, use_container_width=True)
        
        with col2:
            st.markdown("### ➕ Tambah Penerima Baru")
            nama = st.text_input("Nama Lengkap")
            ttl = st.text_input("Tempat, Tanggal Lahir")
            jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
            bb = st.number_input("Berat Badan (kg)", min_value=0.0, max_value=200.0, step=0.1)
            tb = st.number_input("Tinggi Badan (cm)", min_value=0.0, max_value=250.0, step=0.1)
            
            if st.button("💾 Simpan Data"):
                new_data = {
                    "nama": nama,
                    "ttl": ttl,
                    "jenis_kelamin": jk,
                    "bb": bb,
                    "tb": tb,
                    "lembaga": "SDN Bandung 1"
                }
                st.session_state.penerima_data.append(new_data)
                st.success(f"✅ Data {nama} berhasil ditambahkan!")
                st.rerun()
    
    with tab2:
        st.subheader("🔍 Sistem Biometrik")
        st.info("📸 Fitur pengambilan foto dan sidik jari akan diintegrasikan dengan perangkat biometrik")
        
        selected_person = st.selectbox("Pilih Penerima untuk Registrasi Biometrik:", 
                                     [p["nama"] for p in st.session_state.penerima_data])
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📷 Ambil Foto"):
                st.success(f"✅ Foto {selected_person} berhasil diambil!")
        
        with col2:
            if st.button("👆 Scan Sidik Jari"):
                st.success(f"✅ Sidik jari {selected_person} berhasil discan!")
    
    with tab3:
        st.subheader("🍽️ Penerimaan Makanan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📋 Scan QR Code")
            qr_data = f"verification_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            qr_img = generate_qr_code(qr_data)
            st.markdown(f'<img src="data:image/png;base64,{qr_img}" width="200">', unsafe_allow_html=True)
            
            if st.button("🔍 Verifikasi QR"):
                st.success("✅ QR Code berhasil diverifikasi!")
        
        with col2:
            st.markdown("### 📊 Verifikasi Kuota Makanan")
            today_quota = [k for k in st.session_state.kuota_makanan if k["tanggal"] == "2025-01-31"]
            
            for quota in today_quota:
                remaining = quota["kuota"] - quota["terpakai"]
                st.markdown(f"""
                <div class="success-box">
                    <h4>{quota["menu"]}</h4>
                    <p>📍 {quota["lembaga"]}</p>
                    <p>✅ Terpakai: {quota["terpakai"]} | 📦 Sisa: {remaining}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("### 🍽️ Jumlah Makanan")
        jumlah = st.number_input("Masukkan jumlah makanan yang diterima:", min_value=1, max_value=500, value=1)
        
        if st.button("✅ Konfirmasi Penerimaan"):
            st.success(f"✅ Penerimaan {jumlah} porsi makanan berhasil dikonfirmasi!")
        
        st.markdown("### ✔️ Verifikasi Kualitas Makanan")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            rasa = st.selectbox("Rasa:", ["Baik", "Cukup", "Kurang"])
        with col2:
            tampilan = st.selectbox("Tampilan:", ["Baik", "Cukup", "Kurang"])
        with col3:
            porsi = st.selectbox("Porsi:", ["Sesuai", "Kurang", "Berlebih"])
        
        if st.button("📝 Simpan Evaluasi"):
            st.success("✅ Evaluasi kualitas makanan berhasil disimpan!")
    
    with tab4:
        st.subheader("📞 Pengaduan")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📝 Form Pengaduan")
            jenis_pengaduan = st.selectbox("Jenis Pengaduan:", 
                                         ["Kualitas Makanan", "Keterlambatan", "Kuantitas", "Lainnya"])
            deskripsi = st.text_area("Deskripsi Pengaduan:", height=100)
            
            if st.button("📤 Kirim Pengaduan"):
                pengaduan_baru = {
                    "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "jenis": jenis_pengaduan,
                    "deskripsi": deskripsi,
                    "status": "Pending",
                    "lembaga": "SDN Bandung 1"
                }
                st.session_state.pengaduan.append(pengaduan_baru)
                st.success("✅ Pengaduan berhasil dikirim!")
        
        with col2:
            st.markdown("### 📋 Riwayat Pengaduan")
            if st.session_state.pengaduan:
                for i, p in enumerate(st.session_state.pengaduan[-5:]):  # Show last 5
                    status_color = "success-box" if p["status"] == "Resolved" else "warning-box"
                    st.markdown(f"""
                    <div class="{status_color}">
                        <small>{p["tanggal"]}</small>
                        <h5>{p["jenis"]}</h5>
                        <p>Status: {p["status"]}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Belum ada pengaduan")
    
    with tab5:
        st.subheader("📊 Catatan Penyimpangan")
        
        # Chart penyimpangan
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat'],
            y=[2, 1, 3, 0, 1],
            mode='lines+markers',
            name='Jumlah Penyimpangan',
            line=dict(color='#ff6b6b', width=3)
        ))
        
        fig.update_layout(
            title="📈 Trend Penyimpangan Mingguan",
            xaxis_title="Hari",
            yaxis_title="Jumlah Penyimpangan",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)

def logistik_dashboard():
    """Dashboard Logistik"""
    st.markdown('<div class="main-header"><h1>🚚 Dashboard Logistik</h1></div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📦 Order Makanan", "📍 Lokasi & Terima", "🛣️ Perjalanan Logistik", "✅ Verifikasi Makanan"])
    
    with tab1:
        st.subheader("📦 Order Makanan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📋 Terima Pesanan")
            lembaga_tujuan = st.selectbox("Lembaga Tujuan:", [l["nama"] for l in st.session_state.lembaga_data])
            menu_pesanan = st.selectbox("Menu Makanan:", [m["nama"] for m in st.session_state.menu_makanan])
            jumlah_pesanan = st.number_input("Jumlah Pesanan:", min_value=1, max_value=1000, value=100)
            tanggal_kirim = st.date_input("Tanggal Pengiriman:", value=date.today())
            
            if st.button("✅ Konfirmasi Pesanan"):
                pesanan_baru = {
                    "id": f"ORD_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "lembaga": lembaga_tujuan,
                    "menu": menu_pesanan,
                    "jumlah": jumlah_pesanan,
                    "tanggal": str(tanggal_kirim),
                    "status": "Diproses"
                }
                st.session_state.pesanan_logistik.append(pesanan_baru)
                st.success("✅ Pesanan berhasil dikonfirmasi!")
        
        with col2:
            st.markdown("### 🚫 Tolak Pesanan")
            if st.session_state.pesanan_logistik:
                pesanan_id = st.selectbox("Pilih Pesanan untuk Ditolak:", 
                                        [p["id"] for p in st.session_state.pesanan_logistik])
                alasan = st.text_area("Alasan Penolakan:")
                
                if st.button("❌ Tolak Pesanan"):
                    st.warning("⚠️ Pesanan ditolak dengan alasan: " + alasan)
            else:
                st.info("Tidak ada pesanan untuk ditolak")
        
        st.markdown("### 📋 Catatan Penolakan")
        st.info("📝 Riwayat penolakan pesanan akan ditampilkan di sini")
    
    with tab2:
        st.subheader("📍 Lokasi Kirim & Terima")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🗺️ Rute Lokasi Terima Makanan")
            for i, lembaga in enumerate(st.session_state.lembaga_data):
                st.markdown(f"""
                <div class="success-box">
                    <h4>📍 {lembaga['nama']}</h4>
                    <p>🏠 {lembaga['alamat']}</p>
                    <p>📞 {lembaga['kontak']}</p>
                    <p>⏰ Estimasi: 30 menit</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🚛 Rute Lokasi Kirim Makanan")
            rute_options = ["Rute A (Optimal)", "Rute B (Alternatif)", "Rute C (Darurat)"]
            selected_route = st.selectbox("Pilih Rute:", rute_options)
            
            st.markdown(f"""
            <div class="warning-box">
                <h4>🛣️ {selected_route}</h4>
                <p>📏 Jarak: 15.5 km</p>
                <p>⏱️ Estimasi Waktu: 45 menit</p>
                <p>⛽ Estimasi BBM: 2.5 L</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 Mulai Perjalanan"):
                st.success("✅ Perjalanan dimulai! GPS tracking aktif.")
    
    with tab3:
        st.subheader("🛣️ Perjalanan Logistik")
        
        tab3_1, tab3_2, tab3_3, tab3_4, tab3_5 = st.tabs(["🚨 Panic Button", "🚗 Kondisi Mobil", "💥 Kecelakaan", "🛣️ Jalanan Macet", "🚨 Bencana Alam"])
        
        with tab3_1:
            st.markdown("### 🚨 Panic Button")
            st.markdown('<div class="warning-box"><h3>⚠️ EMERGENCY ALERT</h3><p>Tekan tombol ini hanya dalam keadaan darurat!</p></div>', unsafe_allow_html=True)
            
            if st.button("🚨 PANIC BUTTON", type="primary"):
                st.error("🚨 EMERGENCY ALERT SENT! Tim rescue sedang dalam perjalanan!")
                st.balloons()
        
        with tab3_2:
            st.markdown("### 🚗 Kondisi Mobil")
            col1, col2 = st.columns(2)
            
            with col1:
                mesin = st.selectbox("Status Mesin:", ["Normal", "Bermasalah", "Rusak"])
                ban = st.selectbox("Kondisi Ban:", ["Baik", "Perlu Diganti", "Bocor"])
            
            with col2:
                bbm = st.selectbox("Level BBM:", ["Penuh", "Setengah", "Hampir Habis"])
                ac = st.selectbox("Sistem Pendingin:", ["Normal", "Kurang Dingin", "Rusak"])
            
            if st.button("📊 Update Status Kendaraan"):
                st.success("✅ Status kendaraan berhasil diupdate!")
        
        with tab3_3:
            st.markdown("### 💥 Lapor Kecelakaan")
            tingkat = st.selectbox("Tingkat Kecelakaan:", ["Ringan", "Sedang", "Berat"])
            deskripsi = st.text_area("Deskripsi Kecelakaan:")
            
            if st.button("📞 Lapor Kecelakaan"):
                st.error("🚨 Laporan kecelakaan dikirim! Tim medis & asuransi telah dihubungi.")
        
        with tab3_4:
            st.markdown("### 🛣️ Jalanan Macet")
            lokasi_macet = st.text_input("Lokasi Kemacetan:")
            tingkat_macet = st.selectbox("Tingkat Kemacetan:", ["Lancar", "Padat Merayap", "Macet Total"])
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📍 Lapor Kemacetan"):
                    st.warning(f"⚠️ Kemacetan {tingkat_macet} dilaporkan di {lokasi_macet}")
            
            with col2:
                if st.button("🔄 Update Rute"):
                    st.info("🗺️ Mencari rute alternatif...")
        
        with tab3_5:
            st.markdown("### 🚨 Bencana Alam")
            jenis_bencana = st.selectbox("Jenis Bencana:", ["Banjir", "Gempa", "Longsor", "Angin Kencang"])
            dampak = st.text_area("Dampak terhadap Perjalanan:")
            
            if st.button("🚨 Lapor Bencana"):
                st.error("🚨 ALERT BENCANA ALAM! Semua unit logistik dihentikan sementara.")
    
    with tab4:
        st.subheader("✅ Verifikasi Makanan")
        
        st.markdown("### 📱 Generate QR Code")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Form untuk generate QR
            batch_id = st.text_input("Batch ID:", value=f"BATCH_{datetime.now().strftime('%Y%m%d_%H%M')}")
            produsen = st.selectbox("Produsen:", ["Katering Sehat Bandung", "Nutrisi Prima", "Makanan Bergizi Nusantara"])
            menu_qr = st.selectbox("Menu:", [m["nama"] for m in st.session_state.menu_makanan])
            jumlah_qr = st.number_input("Jumlah Makanan:", min_value=1, max_value=1000, value=100)
            
            if st.button("🔗 Generate QR Code"):
                qr_data = {
                    "batch_id": batch_id,
                    "produsen": produsen,
                    "menu": menu_qr,
                    "jumlah": jumlah_qr,
                    "timestamp": datetime.now().isoformat()
                }
                qr_string = json.dumps(qr_data)
                qr_img = generate_qr_code(qr_string)
                
                st.session_state.current_qr = qr_img
                st.session_state.current_qr_data = qr_data
                st.success("✅ QR Code berhasil di-generate!")
        
        with col2:
            # Display QR Code
            if hasattr(st.session_state, 'current_qr'):
                st.markdown("### 📱 QR Code")
                st.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{st.session_state.current_qr}" width="200"></div>', unsafe_allow_html=True)
                
                if hasattr(st.session_state, 'current_qr_data'):
                    st.json(st.session_state.current_qr_data)

def produsen_dashboard():
    """Dashboard Produsen Makanan"""
    st.markdown('<div class="main-header"><h1>🏭 Dashboard Produsen Makanan</h1></div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🍽️ Input Menu", "📊 Kuota Makanan", "📦 Order Logistik", "📈 Monitoring Logistik"])
    
    with tab1:
        st.subheader("🍽️ Input Menu Makanan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ➕ Pilih Menu Makanan")
            for i, menu in enumerate(st.session_state.menu_makanan):
                with st.expander(f"🍽️ {menu['nama']}"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("🔥 Kalori", f"{menu['kalori']} kkal")
                        st.metric("🥩 Protein", f"{menu['protein']} g")
                    with col_b:
                        st.metric("🍚 Karbohidrat", f"{menu['karbohidrat']} g")
                        st.metric("🥑 Lemak", f"{menu['lemak']} g")
        
        with col2:
            st.markdown("### 🔢 Hasil Kalori/AKG")
            selected_menu = st.selectbox("Pilih Menu untuk Analisis:", [m["nama"] for m in st.session_state.menu_makanan])
            
            # Find selected menu data
            menu_data = next((m for m in st.session_state.menu_makanan if m["nama"] == selected_menu), None)
            
            if menu_data:
                # AKG reference for school age (7-12 years)
                akg_reference = {"kalori": 2000, "protein": 50, "karbohidrat": 280, "lemak": 65}
                
                st.markdown("### 📊 Persentase AKG")
                
                for nutrisi in ['kalori', 'protein', 'karbohidrat', 'lemak']:
                    percentage = (menu_data[nutrisi] / akg_reference[nutrisi]) * 100
                    st.progress(min(percentage/100, 1.0))
                    st.write(f"{nutrisi.title()}: {percentage:.1f}% dari AKG")
    
    with tab2:
        st.subheader("📊 Kuota Makanan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏫 Pilih Lembaga Pendidikan")
            lembaga_pilihan = st.selectbox("Lembaga:", [l["nama"] for l in st.session_state.lembaga_data])
            
            st.markdown("### 📅 Input Kuota Makanan")
            tanggal_kuota = st.date_input("Tanggal:", value=date.today())
            menu_kuota = st.selectbox("Menu:", [m["nama"] for m in st.session_state.menu_makanan])
            jumlah_kuota = st.number_input("Jumlah Kuota:", min_value=1, max_value=1000, value=100)
            
            if st.button("💾 Simpan Kuota"):
                kuota_baru = {
                    "lembaga": lembaga_pilihan,
                    "tanggal": str(tanggal_kuota),
                    "menu": menu_kuota,
                    "kuota": jumlah_kuota,
                    "terpakai": 0
                }
                st.session_state.kuota_makanan.append(kuota_baru)
                st.success("✅ Kuota makanan berhasil disimpan!")
        
        with col2:
            st.markdown("### 📊 Kuota Hari Ini")
            today_str = str(date.today())
            today_quotas = [k for k in st.session_state.kuota_makanan if k["tanggal"] == today_str]
            
            if today_quotas:
                for quota in today_quotas:
                    remaining = quota["kuota"] - quota["terpakai"]
                    usage_percentage = (quota["terpakai"] / quota["kuota"]) * 100
                    
                    st.markdown(f"""
                    <div class="success-box">
                        <h4>🏫 {quota["lembaga"]}</h4>
                        <p>🍽️ {quota["menu"]}</p>
                        <p>📊 {quota["terpakai"]}/{quota["kuota"]} ({usage_percentage:.1f}%)</p>
                        <p>📦 Sisa: {remaining}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Belum ada kuota untuk hari ini")
    
    with tab3:
        st.subheader("📦 Order Logistik")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏫 Pilih Lembaga Pendidikan")
            target_lembaga = st.selectbox("Lembaga Tujuan:", [l["nama"] for l in st.session_state.lembaga_data], key="target_lembaga")
            
            st.markdown("### 🚚 Pilih Logistik")
            logistik_options = ["Logistik A - Truck Besar", "Logistik B - Van Sedang", "Logistik C - Motor Box"]
            selected_logistik = st.selectbox("Provider Logistik:", logistik_options)
            
            menu_order = st.selectbox("Menu Pesanan:", [m["nama"] for m in st.session_state.menu_makanan], key="menu_order")
            jumlah_order = st.number_input("Jumlah Pesanan:", min_value=1, max_value=1000, value=100, key="jumlah_order")
            waktu_kirim = st.time_input("Waktu Pengiriman:", value=datetime.now().time())
            
            if st.button("📋 Buat Pesanan Logistik"):
                pesanan_baru = {
                    "id": f"PROD_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "lembaga": target_lembaga,
                    "logistik": selected_logistik,
                    "menu": menu_order,
                    "jumlah": jumlah_order,
                    "waktu": str(waktu_kirim),
                    "status": "Menunggu Konfirmasi"
                }
                st.session_state.pesanan_logistik.append(pesanan_baru)
                st.success("✅ Pesanan logistik berhasil dibuat!")
        
        with col2:
            st.markdown("### 📋 Status Pesanan")
            if st.session_state.pesanan_logistik:
                for pesanan in st.session_state.pesanan_logistik[-5:]:  # Show last 5 orders
                    status_color = "success-box" if "Konfirmasi" in pesanan["status"] else "warning-box"
                    st.markdown(f"""
                    <div class="{status_color}">
                        <h5>📦 {pesanan["id"]}</h5>
                        <p>🏫 {pesanan["lembaga"]}</p>
                        <p>🍽️ {pesanan["menu"]} ({pesanan["jumlah"]} porsi)</p>
                        <p>📊 Status: {pesanan["status"]}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Belum ada pesanan logistik")
    
    with tab4:
        st.subheader("📈 Monitoring Logistik")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🛣️ Perjalanan Logistik")
            
            # Dummy tracking data
            tracking_data = [
                {"waktu": "08:00", "lokasi": "Dapur Produksi", "status": "Makanan disiapkan"},
                {"waktu": "08:30", "lokasi": "Loading Area", "status": "Makanan dimuat ke kendaraan"},
                {"waktu": "09:00", "lokasi": "Jl. Sudirman", "status": "Dalam perjalanan"},
                {"waktu": "09:15", "lokasi": "SDN Bandung 1", "status": "Sampai di tujuan"}
            ]
            
            for track in tracking_data:
                st.markdown(f"""
                <div class="success-box">
                    <h5>⏰ {track["waktu"]}</h5>
                    <p>📍 {track["lokasi"]}</p>
                    <p>📊 {track["status"]}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 📞 Notifikasi Logistik")
            
            notifications = [
                {"type": "success", "message": "✅ Pengiriman ke SDN Bandung 1 berhasil"},
                {"type": "warning", "message": "⚠️ Keterlambatan 15 menit di SMP Negeri 5"},
                {"type": "info", "message": "ℹ️ Persiapan pengiriman batch berikutnya"},
                {"type": "error", "message": "❌ Kendala cuaca di rute SMA Negeri 3"}
            ]
            
            for notif in notifications:
                box_class = "success-box" if notif["type"] == "success" else "warning-box"
                st.markdown(f'<div class="{box_class}"><p>{notif["message"]}</p></div>', unsafe_allow_html=True)

def main():
    """Fungsi utama aplikasi"""
    
    # Sidebar untuk logout dan info user
    with st.sidebar:
        if st.session_state.logged_in:
            st.markdown("### 👤 Info Pengguna")
            st.success(f"🟢 Login sebagai: **{st.session_state.user_data['role']}**")
            st.info(f"👤 Username: {st.session_state.user_data['username']}")
            
            if st.button("🚪 Logout"):
                st.session_state.logged_in = False
                st.session_state.user_role = None
                st.session_state.user_data = {}
                st.rerun()
            
            st.markdown("---")
            st.markdown("### 📊 Quick Stats")
            st.metric("🍽️ Makanan Hari Ini", "460 porsi")
            st.metric("🏫 Lembaga Aktif", "3 sekolah")
            st.metric("📈 Efisiensi", "92%")
            
            st.markdown("---")
            st.markdown("### 🔗 Quick Links")
            st.markdown("- 📞 Emergency: **119**")
            st.markdown("- 🏥 Kesehatan: **118**")
            st.markdown("- 🚨 Polisi: **110**")
        else:
            st.markdown("### 🏠 Selamat Datang")
            st.info("Silakan login untuk mengakses sistem")
            
            st.markdown("### 📋 Demo Accounts")
            st.code("""
Admin: admin / admin123
Lembaga: lembaga / lembaga123
Logistik: logistik / logistik123  
Produsen: produsen / produsen123
            """)
    
    # Main content
    if not st.session_state.logged_in:
        login_page()
    else:
        # Route berdasarkan role
        if st.session_state.user_role == "Admin":
            admin_dashboard()
        elif st.session_state.user_role == "Lembaga Pendidikan":
            lembaga_dashboard()
        elif st.session_state.user_role == "Logistik":
            logistik_dashboard()
        elif st.session_state.user_role == "Produsen Makanan":
            produsen_dashboard()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>🍽️ <b>Sistem Monitoring Makan Bergizi Gratis</b> 🍽️</p>
        <p>Memastikan Nutrisi Terbaik untuk Generasi Masa Depan Indonesia</p>
        <small>© 2025 - Dikembangkan dengan ❤️ untuk Indonesia</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()