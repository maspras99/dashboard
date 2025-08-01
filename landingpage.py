import streamlit as st
from streamlit.components.v1 import html

# Konfigurasi halaman
st.set_page_config(
    page_title="Program MBG - Management & Quality Control",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS untuk styling yang menarik
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Reset dan styling umum */
    .main {
        padding: 0 !important;
    }
    
    .stApp {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Header Section */
    .header-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 3rem 2rem;
        margin: 2rem auto;
        max-width: 1200px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    
    .subtitle {
        font-size: 1.3rem;
        color: #666;
        font-weight: 300;
        margin-bottom: 2rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
    }
    
    /* Button Grid */
    .button-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
        max-width: 1000px;
        margin: 3rem auto;
        padding: 0 1rem;
    }
    
    .app-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .app-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .app-card:hover::before {
        transform: scaleX(1);
    }
    
    .app-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.15);
    }
    
    .app-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
        display: block;
    }
    
    .app-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 1rem;
    }
    
    .app-description {
        font-size: 0.95rem;
        color: #666;
        line-height: 1.6;
        margin-bottom: 2rem;
    }
    
    .app-button {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        text-decoration: none;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .app-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        text-decoration: none;
        color: white;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: rgba(255,255,255,0.8);
        font-size: 0.9rem;
    }
    
    /* Animasi */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        
        .subtitle {
            font-size: 1.1rem;
        }
        
        .header-container {
            margin: 1rem;
            padding: 2rem 1.5rem;
        }
        
        .button-grid {
            grid-template-columns: 1fr;
            gap: 1.5rem;
            margin: 2rem auto;
        }
        
        .app-card {
            padding: 2rem 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
<div class="header-container fade-in">
    <h1 class="main-title">🍽️ Program MBG</h1>
    <p class="subtitle">
        Sistem Manajemen Berbasis Gizi dan Kontrol Kualitas Makanan Terintegrasi
        <br>
        Solusi lengkap untuk pengelolaan gizi dan kualitas makanan yang efisien dan modern
    </p>
</div>
""", unsafe_allow_html=True)

# Button Grid dengan aplikasi
applications = [
    {
        "icon": "📱",
        "title": "Aplikasi MBG",
        "description": "Dashboard utama untuk manajemen gizi dan monitoring kesehatan makanan secara komprehensif",
        "url": "https://dashboard-frfnrrgfv5m3e9vlxqlot5.streamlit.app/",
        "color": "#667eea"
    },
    {
        "icon": "👨‍🍳",
        "title": "Aplikasi Dapur",
        "description": "Sistem khusus untuk pengelolaan operasional dapur, inventory, dan workflow memasak",
        "url": "https://dashboard-iudyykcqcusqiexkcf9awk.streamlit.app/",
        "color": "#f093fb"
    },
    {
        "icon": "🧮",
        "title": "Kalkulator AKG",
        "description": "Tool perhitungan Angka Kecukupan Gizi yang akurat berdasarkan profil individu",
        "url": "https://dashboard-9tbuupjzypfqwuuvkyay3w.streamlit.app/",
        "color": "#4facfe"
    },
    {
        "icon": "📊",
        "title": "Dashboard Kualitas",
        "description": "Monitoring dan analisis kualitas makanan dengan visualisasi data yang interaktif",
        "url": "https://dashboard-mykmbv44jd544m9v3wyagn.streamlit.app/",
        "color": "#43e97b"
    }
]

# Membuat grid aplikasi
st.markdown('<div class="button-grid">', unsafe_allow_html=True)

cols = st.columns(2)
for i, app in enumerate(applications):
    with cols[i % 2]:
        st.markdown(f"""
        <div class="app-card fade-in" style="animation-delay: {i * 0.1}s;">
            <span class="app-icon">{app['icon']}</span>
            <h3 class="app-title">{app['title']}</h3>
            <p class="app-description">{app['description']}</p>
            <a href="{app['url']}" target="_blank" class="app-button">
                Buka Aplikasi →
            </a>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Fitur tambahan
st.markdown("""
<div style="max-width: 1000px; margin: 4rem auto; padding: 0 1rem;">
    <div style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 20px; padding: 3rem 2rem; text-align: center; border: 1px solid rgba(255,255,255,0.2);">
        <h2 style="color: white; font-size: 2rem; margin-bottom: 2rem; font-weight: 600;">
            🌟 Keunggulan Program MBG
        </h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-top: 2rem;">
            <div style="color: white; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">⚡</div>
                <h4 style="margin-bottom: 0.5rem;">Efisien & Cepat</h4>
                <p style="font-size: 0.9rem; opacity: 0.9;">Otomatisasi proses untuk menghemat waktu dan tenaga</p>
            </div>
            <div style="color: white; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">🔒</div>
                <h4 style="margin-bottom: 0.5rem;">Aman & Terpercaya</h4>
                <p style="font-size: 0.9rem; opacity: 0.9;">Keamanan data terjamin dengan enkripsi tingkat tinggi</p>
            </div>
            <div style="color: white; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">📈</div>
                <h4 style="margin-bottom: 0.5rem;">Analytics Mendalam</h4>
                <p style="font-size: 0.9rem; opacity: 0.9;">Laporan dan analisis komprehensif untuk pengambilan keputusan</p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>© 2025 Program MBG - Management & Quality Control System</p>
    <p>Dikembangkan dengan ❤️ untuk meningkatkan kualitas gizi dan makanan</p>
</div>
""", unsafe_allow_html=True)

# JavaScript untuk smooth scrolling dan animasi
st.markdown("""
<script>
// Smooth animations on page load
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.app-card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });
    
    cards.forEach(card => {
        observer.observe(card);
    });
});
</script>
""", unsafe_allow_html=True)