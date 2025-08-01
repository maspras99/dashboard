import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta, date
import random

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Pemangku Kepentingan - Monitoring Kualitas Makanan",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS untuk styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .alert-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.2);
        animation: pulse 2s infinite;
    }
    .success-card {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(78, 205, 196, 0.2);
    }
    .warning-card {
        background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(254, 202, 87, 0.2);
    }
    .info-card {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(116, 185, 255, 0.2);
    }
    @keyframes pulse {
        0% { box-shadow: 0 4px 15px rgba(255, 107, 107, 0.2); }
        50% { box-shadow: 0 4px 25px rgba(255, 107, 107, 0.4); }
        100% { box-shadow: 0 4px 15px rgba(255, 107, 107, 0.2); }
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Inisialisasi data dummy untuk dashboard
@st.cache_data
def generate_sample_data():
    """Generate data sampel untuk dashboard"""
    
    # Data kualitas makanan dalam 30 hari terakhir
    dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
    
    quality_data = []
    for date in dates:
        for producer in ['Katering Sehat Bandung', 'Nutrisi Prima', 'Makanan Bergizi Nusantara']:
            for school in ['SDN Bandung 1', 'SMP Negeri 5', 'SMA Negeri 3']:
                # Simulasi data kualitas
                freshness_score = random.uniform(6, 10)
                delivery_time = random.uniform(30, 180)  # menit
                temperature = random.uniform(15, 45)  # celsius
                
                # Logika untuk menentukan status basi
                is_spoiled = (
                    freshness_score < 7 or 
                    delivery_time > 120 or 
                    temperature > 35
                )
                
                quality_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'producer': producer,
                    'school': school,
                    'freshness_score': freshness_score,
                    'delivery_time_minutes': delivery_time,
                    'temperature_celsius': temperature,
                    'is_spoiled': is_spoiled,
                    'batch_size': random.randint(50, 200),
                    'complaints': random.randint(0, 5) if is_spoiled else random.randint(0, 1)
                })
    
    return pd.DataFrame(quality_data)

@st.cache_data
def generate_delivery_data():
    """Generate data pengiriman detail"""
    
    delivery_stages = [
        'Persiapan di Dapur',
        'Packaging',
        'Loading ke Kendaraan',
        'Perjalanan',
        'Unloading',
        'Distribusi'
    ]
    
    delivery_data = []
    for i in range(100):  # 100 batch pengiriman
        start_time = datetime.now() - timedelta(days=random.randint(1, 30))
        current_time = start_time
        
        batch_id = f"BATCH_{i+1:03d}"
        producer = random.choice(['Katering Sehat Bandung', 'Nutrisi Prima', 'Makanan Bergizi Nusantara'])
        school = random.choice(['SDN Bandung 1', 'SMP Negeri 5', 'SMA Negeri 3'])
        
        total_duration = 0
        for stage in delivery_stages:
            duration = random.uniform(10, 45)  # durasi per tahap dalam menit
            total_duration += duration
            
            delivery_data.append({
                'batch_id': batch_id,
                'producer': producer,
                'school': school,
                'stage': stage,
                'duration_minutes': duration,
                'timestamp': current_time,
                'total_duration_so_far': total_duration,
                'date': start_time.strftime('%Y-%m-%d')
            })
            
            current_time += timedelta(minutes=duration)
    
    return pd.DataFrame(delivery_data)

@st.cache_data
def generate_spoilage_reasons():
    """Generate data alasan makanan basi"""
    
    reasons = [
        'Suhu penyimpanan terlalu tinggi',
        'Waktu pengiriman terlalu lama',
        'Kemasan tidak kedap udara',
        'Kualitas bahan baku rendah',
        'Proses masak tidak optimal',
        'Kontaminasi saat packaging',
        'Kondisi cuaca ekstrem',
        'Kendaraan rusak di perjalanan',
        'Kemacetan lalu lintas',
        'Penanganan tidak higienis'
    ]
    
    spoilage_data = []
    for i in range(50):  # 50 kasus makanan basi
        date = datetime.now() - timedelta(days=random.randint(1, 30))
        reason = random.choice(reasons)
        impact = random.choice(['Rendah', 'Sedang', 'Tinggi'])
        cost = random.uniform(500000, 5000000)  # biaya kerugian
        
        spoilage_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'batch_id': f"BATCH_{random.randint(1, 200):03d}",
            'reason': reason,
            'impact_level': impact,
            'financial_loss': cost,
            'affected_portions': random.randint(10, 100),
            'producer': random.choice(['Katering Sehat Bandung', 'Nutrisi Prima', 'Makanan Bergizi Nusantara']),
            'school': random.choice(['SDN Bandung 1', 'SMP Negeri 5', 'SMA Negeri 3'])
        })
    
    return pd.DataFrame(spoilage_data)

def main_dashboard():
    """Dashboard utama"""
    
    st.markdown('''
    <div class="main-header">
        <h1>📊 Dashboard Pemangku Kepentingan</h1>
        <h3>Monitoring Kualitas & Tracking Makanan Basi</h3>
        <p>Sistem Analisis Komprehensif untuk Menjamin Kualitas Makanan Bergizi Gratis</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Load data
    quality_df = generate_sample_data()
    delivery_df = generate_delivery_data()
    spoilage_df = generate_spoilage_reasons()
    
    # Sidebar filters
    with st.sidebar:
        st.markdown("### 🔍 Filter Dashboard")
        
        date_range = st.date_input(
            "Rentang Tanggal:",
            value=(datetime.now() - timedelta(days=30), datetime.now()),
            max_value=datetime.now()
        )
        
        selected_producers = st.multiselect(
            "Pilih Produsen:",
            quality_df['producer'].unique(),
            default=quality_df['producer'].unique()
        )
        
        selected_schools = st.multiselect(
            "Pilih Sekolah:",
            quality_df['school'].unique(),
            default=quality_df['school'].unique()
        )
        
        st.markdown("---")
        st.markdown("### 📈 Quick Stats")
        
        total_batches = len(quality_df)
        spoiled_batches = len(quality_df[quality_df['is_spoiled'] == True])
        spoilage_rate = (spoiled_batches / total_batches) * 100
        
        st.metric("Total Batch", total_batches)
        st.metric("Makanan Basi", spoiled_batches)
        st.metric("Tingkat Kebusukan", f"{spoilage_rate:.1f}%")
    
    # Filter data berdasarkan sidebar
    filtered_quality = quality_df[
        (quality_df['producer'].isin(selected_producers)) &
        (quality_df['school'].isin(selected_schools))
    ]
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_batches = len(filtered_quality)
        st.markdown(f'''
        <div class="metric-card">
            <h3>📦 Total Batch</h3>
            <h2>{total_batches:,}</h2>
            <p>Batch Makanan</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        spoiled_count = len(filtered_quality[filtered_quality['is_spoiled'] == True])
        st.markdown(f'''
        <div class="metric-card">
            <h3>🦠 Makanan Basi</h3>
            <h2>{spoiled_count:,}</h2>
            <p>Batch Bermasalah</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        avg_delivery = filtered_quality['delivery_time_minutes'].mean()
        st.markdown(f'''
        <div class="metric-card">
            <h3>⏱️ Rata-rata Pengiriman</h3>
            <h2>{avg_delivery:.0f}</h2>
            <p>Menit</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        total_loss = spoilage_df['financial_loss'].sum()
        st.markdown(f'''
        <div class="metric-card">
            <h3>💰 Total Kerugian</h3>
            <h2>Rp {total_loss/1000000:.1f}M</h2>
            <p>Rupiah</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Alert Cards
    if spoilage_rate > 15:
        st.markdown(f'''
        <div class="alert-card">
            <h3>🚨 PERINGATAN TINGGI!</h3>
            <p>Tingkat kebusukan makanan mencapai {spoilage_rate:.1f}% - SEGERA PERLU TINDAKAN!</p>
        </div>
        ''', unsafe_allow_html=True)
    elif spoilage_rate > 10:
        st.markdown(f'''
        <div class="warning-card">
            <h3>⚠️ Peringatan Sedang</h3>
            <p>Tingkat kebusukan makanan {spoilage_rate:.1f}% - Perlu monitoring ketat</p>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="success-card">
            <h3>✅ Status Baik</h3>
            <p>Tingkat kebusukan makanan {spoilage_rate:.1f}% - Dalam batas normal</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Main Charts
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Analisis Kualitas", 
        "🚚 Durasi Pengiriman", 
        "🔍 Root Cause Analysis", 
        "📈 Trend & Prediksi",
        "📋 Laporan Detail"
    ])
    
    with tab1:
        st.subheader("📊 Analisis Kualitas Makanan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Spoilage rate by producer
            spoilage_by_producer = filtered_quality.groupby('producer').agg({
                'is_spoiled': ['count', 'sum']
            }).round(2)
            spoilage_by_producer.columns = ['total_batches', 'spoiled_batches']
            spoilage_by_producer['spoilage_rate'] = (
                spoilage_by_producer['spoiled_batches'] / 
                spoilage_by_producer['total_batches'] * 100
            )
            spoilage_by_producer = spoilage_by_producer.reset_index()
            
            fig1 = px.bar(
                spoilage_by_producer, 
                x='producer', 
                y='spoilage_rate',
                title="🏭 Tingkat Kebusukan per Produsen",
                color='spoilage_rate',
                color_continuous_scale='Reds'
            )
            fig1.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12)
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Temperature vs Spoilage
            fig2 = px.scatter(
                filtered_quality,
                x='temperature_celsius',
                y='freshness_score',
                color='is_spoiled',
                title="🌡️ Suhu vs Kesegaran Makanan",
                hover_data=['delivery_time_minutes', 'producer']
            )
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Heatmap quality by school and producer
        pivot_data = filtered_quality.groupby(['school', 'producer'])['is_spoiled'].mean().reset_index()
        pivot_table = pivot_data.pivot(index='school', columns='producer', values='is_spoiled')
        
        fig3 = px.imshow(
            pivot_table,
            title="🗺️ Heatmap Tingkat Kebusukan: Sekolah vs Produsen",
            color_continuous_scale='Reds',
            aspect='auto'
        )
        fig3.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab2:
        st.subheader("🚚 Analisis Durasi Pengiriman")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Delivery time distribution
            fig4 = px.histogram(
                filtered_quality,
                x='delivery_time_minutes',
                nbins=20,
                title="📊 Distribusi Waktu Pengiriman",
                color_discrete_sequence=['#667eea']
            )
            fig4.add_vline(
                x=120, 
                line_dash="dash", 
                line_color="red",
                annotation_text="Batas Maksimal (120 menit)"
            )
            fig4.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig4, use_container_width=True)
        
        with col2:
            # Box plot delivery time by producer
            fig5 = px.box(
                filtered_quality,
                x='producer',
                y='delivery_time_minutes',
                title="📦 Waktu Pengiriman per Produsen"
            )
            fig5.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig5, use_container_width=True)
        
        # Detailed delivery stages analysis
        st.markdown("### 🔍 Analisis Detail Tahapan Pengiriman")
        
        stage_analysis = delivery_df.groupby('stage')['duration_minutes'].agg(['mean', 'std', 'min', 'max']).round(1)
        stage_analysis = stage_analysis.reset_index()
        
        fig6 = px.bar(
            stage_analysis,
            x='stage',
            y='mean',
            error_y='std',
            title="⏱️ Rata-rata Durasi per Tahapan Pengiriman",
            color='mean',
            color_continuous_scale='Viridis'
        )
        fig6.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig6, use_container_width=True)
        
        # Delivery time trend
        daily_delivery = filtered_quality.groupby('date')['delivery_time_minutes'].mean().reset_index()
        daily_delivery['date'] = pd.to_datetime(daily_delivery['date'])
        
        fig7 = px.line(
            daily_delivery,
            x='date',
            y='delivery_time_minutes',
            title="📈 Trend Waktu Pengiriman Harian",
            markers=True
        )
        fig7.add_hline(
            y=120,
            line_dash="dash",
            line_color="red",
            annotation_text="Target Maksimal"
        )
        fig7.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig7, use_container_width=True)
    
    with tab3:
        st.subheader("🔍 Root Cause Analysis - Penyebab Makanan Basi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top reasons for spoilage
            reason_counts = spoilage_df['reason'].value_counts().head(8)
            
            fig8 = px.bar(
                x=reason_counts.values,
                y=reason_counts.index,
                orientation='h',
                title="🎯 Penyebab Utama Makanan Basi",
                color=reason_counts.values,
                color_continuous_scale='Reds'
            )
            fig8.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            st.plotly_chart(fig8, use_container_width=True)
        
        with col2:
            # Impact level distribution
            impact_dist = spoilage_df['impact_level'].value_counts()
            
            fig9 = px.pie(
                values=impact_dist.values,
                names=impact_dist.index,
                title="📊 Distribusi Tingkat Dampak",
                color_discrete_sequence=['#ff6b6b', '#feca57', '#48dbfb']
            )
            fig9.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig9, use_container_width=True)
        
        # Financial impact analysis
        financial_by_reason = spoilage_df.groupby('reason')['financial_loss'].sum().sort_values(ascending=False).head(8)
        
        fig10 = px.bar(
            x=financial_by_reason.index,
            y=financial_by_reason.values / 1000000,  # Convert to millions
            title="💰 Kerugian Finansial per Penyebab (Juta Rupiah)",
            color=financial_by_reason.values,
            color_continuous_scale='Reds'
        )
        fig10.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig10, use_container_width=True)
        
        # Correlation analysis
        st.markdown("### 🔗 Analisis Korelasi Faktor-Faktor")
        
        correlation_data = filtered_quality[['freshness_score', 'delivery_time_minutes', 'temperature_celsius', 'complaints']].corr()
        
        fig11 = px.imshow(
            correlation_data,
            title="🌡️ Matriks Korelasi Faktor Kualitas",
            color_continuous_scale='RdBu_r',
            aspect='auto'
        )
        fig11.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig11, use_container_width=True)
    
    with tab4:
        st.subheader("📈 Trend Analysis & Prediksi")
        
        # Time series analysis
        daily_spoilage = filtered_quality.groupby('date').agg({
            'is_spoiled': ['count', 'sum']
        }).round(2)
        daily_spoilage.columns = ['total_batches', 'spoiled_batches']
        daily_spoilage['spoilage_rate'] = (daily_spoilage['spoiled_batches'] / daily_spoilage['total_batches'] * 100)
        daily_spoilage = daily_spoilage.reset_index()
        daily_spoilage['date'] = pd.to_datetime(daily_spoilage['date'])
        
        # Add moving average
        daily_spoilage['ma_7'] = daily_spoilage['spoilage_rate'].rolling(window=7).mean()
        
        fig12 = go.Figure()
        fig12.add_trace(go.Scatter(
            x=daily_spoilage['date'],
            y=daily_spoilage['spoilage_rate'],
            mode='lines+markers',
            name='Tingkat Kebusukan Harian',
            line=dict(color='#ff6b6b', width=2)
        ))
        fig12.add_trace(go.Scatter(
            x=daily_spoilage['date'],
            y=daily_spoilage['ma_7'],
            mode='lines',
            name='Moving Average (7 hari)',
            line=dict(color='#667eea', width=3)
        ))
        
        fig12.update_layout(
            title="📈 Trend Tingkat Kebusukan Makanan",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Tanggal",
            yaxis_title="Tingkat Kebusukan (%)"
        )
        st.plotly_chart(fig12, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Monthly comparison
            filtered_quality['month'] = pd.to_datetime(filtered_quality['date']).dt.strftime('%Y-%m')
            monthly_data = filtered_quality.groupby('month').agg({
                'is_spoiled': ['count', 'sum'],
                'delivery_time_minutes': 'mean',
                'temperature_celsius': 'mean'
            }).round(2)
            
            monthly_data.columns = ['total_batches', 'spoiled_batches', 'avg_delivery_time', 'avg_temperature']
            monthly_data['spoilage_rate'] = (monthly_data['spoiled_batches'] / monthly_data['total_batches'] * 100)
            monthly_data = monthly_data.reset_index()
            
            fig13 = px.bar(
                monthly_data,
                x='month',
                y='spoilage_rate',
                title="📅 Perbandingan Bulanan",
                color='spoilage_rate',
                color_continuous_scale='Reds'
            )
            fig13.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig13, use_container_width=True)
        
        with col2:
            # Prediction model (simple linear regression)
            from sklearn.linear_model import LinearRegression
            
            # Prepare data for prediction
            daily_spoilage_numeric = daily_spoilage.dropna()
            if len(daily_spoilage_numeric) > 5:
                X = np.arange(len(daily_spoilage_numeric)).reshape(-1, 1)
                y = daily_spoilage_numeric['spoilage_rate'].values
                
                model = LinearRegression()
                model.fit(X, y)
                
                # Predict next 7 days
                future_X = np.arange(len(daily_spoilage_numeric), len(daily_spoilage_numeric) + 7).reshape(-1, 1)
                future_predictions = model.predict(future_X)
                
                # Create future dates
                last_date = daily_spoilage_numeric['date'].max()
                future_dates = [last_date + timedelta(days=i+1) for i in range(7)]
                
                # Plot prediction
                fig14 = go.Figure()
                fig14.add_trace(go.Scatter(
                    x=daily_spoilage_numeric['date'],
                    y=daily_spoilage_numeric['spoilage_rate'],
                    mode='lines+markers',
                    name='Data Historis',
                    line=dict(color='#667eea')
                ))
                fig14.add_trace(go.Scatter(
                    x=future_dates,
                    y=future_predictions,
                    mode='lines+markers',
                    name='Prediksi 7 Hari',
                    line=dict(color='#ff6b6b', dash='dash')
                ))
                
                fig14.update_layout(
                    title="🔮 Prediksi Tingkat Kebusukan",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig14, use_container_width=True)
        
        # Performance metrics by day of week
        filtered_quality['day_of_week'] = pd.to_datetime(filtered_quality['date']).dt.day_name()
        daily_performance = filtered_quality.groupby('day_of_week').agg({
            'is_spoiled': 'mean',
            'delivery_time_minutes': 'mean',
            'freshness_score': 'mean'
        }).round(2)
        daily_performance = daily_performance.reset_index()
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_performance['day_of_week'] = pd.Categorical(daily_performance['day_of_week'], categories=day_order, ordered=True)
        daily_performance = daily_performance.sort_values('day_of_week')
        
        fig15 = make_subplots(
            rows=1, cols=3,
            subplot_titles=('Tingkat Kebusukan', 'Waktu Pengiriman (menit)', 'Skor Kesegaran'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}, {"secondary_y": False}]]
        )
        
        fig15.add_trace(
            go.Bar(x=daily_performance['day_of_week'], y=daily_performance['is_spoiled']*100, name='Kebusukan (%)', marker_color='#ff6b6b'),
            row=1, col=1
        )
        
        fig15.add_trace(
            go.Bar(x=daily_performance['day_of_week'], y=daily_performance['delivery_time_minutes'], name='Waktu Kirim', marker_color='#feca57'),
            row=1, col=2
        )
        
        fig15.add_trace(
            go.Bar(x=daily_performance['day_of_week'], y=daily_performance['freshness_score'], name='Kesegaran', marker_color='#48dbfb'),
            row=1, col=3
        )
        
        fig15.update_layout(
            title_text="📊 Performa per Hari dalam Seminggu",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        st.plotly_chart(fig15, use_container_width=True)
    
    with tab5:
        st.subheader("📋 Laporan Detail & Rekomendasi")
        
        # Key findings
        st.markdown("### 🎯 Temuan Utama")
        
        col1, col2 = st.columns(2)
        
        with col1:
            worst_producer = spoilage_by_producer.loc[spoilage_by_producer['spoilage_rate'].idxmax(), 'producer']
            worst_rate = spoilage_by_producer.loc[spoilage_by_producer['spoilage_rate'].idxmax(), 'spoilage_rate']
            
            st.markdown(f'''
            <div class="alert-card">
                <h4>🚨 Produsen Terburuk</h4>
                <p><strong>{worst_producer}</strong></p>
                <p>Tingkat kebusukan: {worst_rate:.1f}%</p>
            </div>
            ''', unsafe_allow_html=True)
            
            longest_delivery = filtered_quality['delivery_time_minutes'].max()
            avg_temp = filtered_quality['temperature_celsius'].mean()
            
            st.markdown(f'''
            <div class="warning-card">
                <h4>⏱️ Statistik Pengiriman</h4>
                <p>Pengiriman terlama: {longest_delivery:.0f} menit</p>
                <p>Rata-rata suhu: {avg_temp:.1f}°C</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            top_reason = spoilage_df['reason'].value_counts().index[0]
            top_reason_count = spoilage_df['reason'].value_counts().iloc[0]
            
            st.markdown(f'''
            <div class="info-card">
                <h4>🔍 Penyebab Utama</h4>
                <p><strong>{top_reason}</strong></p>
                <p>Terjadi {top_reason_count} kali</p>
            </div>
            ''', unsafe_allow_html=True)
            
            total_affected = spoilage_df['affected_portions'].sum()
            avg_loss = spoilage_df['financial_loss'].mean()
            
            st.markdown(f'''
            <div class="warning-card">
                <h4>💰 Dampak Kerugian</h4>
                <p>Total porsi terbuang: {total_affected:,}</p>  
                <p>Rata-rata kerugian: Rp {avg_loss/1000000:.1f}M</p>
            </div>
            ''', unsafe_allow_html=True)
        
        # Detailed data tables
        st.markdown("### 📊 Tabel Data Detail")
        
        tab5_1, tab5_2, tab5_3 = st.tabs(["🏭 Per Produsen", "🏫 Per Sekolah", "📅 Per Tanggal"])
        
        with tab5_1:
            producer_summary = filtered_quality.groupby('producer').agg({
                'is_spoiled': ['count', 'sum', 'mean'],
                'delivery_time_minutes': ['mean', 'max'],
                'temperature_celsius': 'mean',
                'freshness_score': 'mean',
                'complaints': 'sum'
            }).round(2)
            
            producer_summary.columns = [
                'Total Batch', 'Batch Basi', 'Tingkat Kebusukan (%)', 
                'Rata-rata Waktu Kirim', 'Waktu Kirim Terlama',
                'Rata-rata Suhu', 'Rata-rata Kesegaran', 'Total Keluhan'
            ]
            producer_summary['Tingkat Kebusukan (%)'] *= 100
            
            st.dataframe(producer_summary, use_container_width=True)
        
        with tab5_2:
            school_summary = filtered_quality.groupby('school').agg({
                'is_spoiled': ['count', 'sum', 'mean'],
                'delivery_time_minutes': ['mean', 'max'],
                'temperature_celsius': 'mean',
                'freshness_score': 'mean',
                'complaints': 'sum'
            }).round(2)
            
            school_summary.columns = [
                'Total Batch', 'Batch Basi', 'Tingkat Kebusukan (%)', 
                'Rata-rata Waktu Kirim', 'Waktu Kirim Terlama',
                'Rata-rata Suhu', 'Rata-rata Kesegaran', 'Total Keluhan'
            ]
            school_summary['Tingkat Kebusukan (%)'] *= 100
            
            st.dataframe(school_summary, use_container_width=True)
        
        with tab5_3:
            daily_summary = filtered_quality.groupby('date').agg({
                'is_spoiled': ['count', 'sum', 'mean'],
                'delivery_time_minutes': 'mean',
                'temperature_celsius': 'mean',
                'freshness_score': 'mean'
            }).round(2)
            
            daily_summary.columns = [
                'Total Batch', 'Batch Basi', 'Tingkat Kebusukan (%)',
                'Rata-rata Waktu Kirim', 'Rata-rata Suhu', 'Rata-rata Kesegaran'
            ]
            daily_summary['Tingkat Kebusukan (%)'] *= 100
            daily_summary = daily_summary.sort_values('date', ascending=False)
            
            st.dataframe(daily_summary, use_container_width=True)
        
        # Recommendations
        st.markdown("### 💡 Rekomendasi Strategis")
        
        recommendations = []
        
        if spoilage_rate > 15:
            recommendations.append("🚨 **URGENT**: Tingkat kebusukan sangat tinggi! Segera audit menyeluruh terhadap seluruh rantai pasokan.")
        
        if avg_delivery > 120:
            recommendations.append("⏰ **Optimasi Logistik**: Waktu pengiriman melebihi standar. Perlukan rute dan jadwal pengiriman.")
        
        if avg_temp > 30:
            recommendations.append("🌡️ **Kontrol Suhu**: Suhu rata-rata terlalu tinggi. Tingkatkan sistem pendinginan.")
        
        recommendations.extend([
            f"🏭 **Fokus pada {worst_producer}**: Produsen dengan tingkat kebusukan tertinggi ({worst_rate:.1f}%)",
            f"🔍 **Atasi {top_reason}**: Penyebab utama kebusukan yang perlu penanganan prioritas",
            "📊 **Monitoring Real-time**: Implementasikan sensor IoT untuk monitoring suhu dan kelembaban",
            "🚚 **Optimasi Rute**: Gunakan AI untuk optimasi rute pengiriman berdasarkan kondisi lalu lintas",
            "📱 **Mobile Alert**: Sistem notifikasi mobile untuk alert cepat jika ada masalah kualitas",
            "🔄 **Continuous Improvement**: Review bulanan SOP dan training untuk semua stakeholder"
        ])
        
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"{i}. {rec}")
        
        # Export functionality
        st.markdown("### 📥 Export Laporan")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Export Data Kualitas"):
                csv = filtered_quality.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"quality_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📈 Export Data Pengiriman"):
                csv = delivery_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"delivery_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col3:
            if st.button("🔍 Export Analisis Kebusukan"):
                csv = spoilage_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"spoilage_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

def realtime_monitoring():
    """Dashboard monitoring real-time"""
    
    st.markdown('''
    <div class="main-header">
        <h1>⚡ Real-time Monitoring</h1>
        <p>Monitoring Live Status Kualitas Makanan</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Auto-refresh
    if st.button("🔄 Refresh Data"):
        st.rerun()
    
    # Real-time metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_batches = random.randint(15, 25)
        st.markdown(f'''
        <div class="metric-card">
            <h3>📦 Batch Aktif</h3>
            <h2>{current_batches}</h2>
            <p>Sedang Dikirim</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        alerts = random.randint(0, 3)
        color = "alert-card" if alerts > 0 else "success-card"
        st.markdown(f'''
        <div class="{color}">
            <h3>🚨 Alert Aktif</h3>
            <h2>{alerts}</h2>
            <p>Perlu Perhatian</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        avg_temp_now = random.uniform(20, 35)
        color = "alert-card" if avg_temp_now > 30 else "success-card"
        st.markdown(f'''
        <div class="{color}">
            <h3>🌡️ Suhu Rata-rata</h3>
            <h2>{avg_temp_now:.1f}°C</h2>
            <p>Real-time</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        on_time = random.randint(85, 98)
        color = "success-card" if on_time > 90 else "warning-card"
        st.markdown(f'''
        <div class="{color}">
            <h3>⏰ Ketepatan Waktu</h3>
            <h2>{on_time}%</h2>
            <p>Hari Ini</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Live tracking map (simulated)
    st.markdown("### 🗺️ Live Tracking Pengiriman")
    
    # Simulated delivery locations
    map_data = pd.DataFrame({
        'lat': [-6.9175, -6.8951, -6.9147, -6.9355],
        'lon': [107.6191, 107.6081, 107.6098, 107.6200],
        'name': ['SDN Bandung 1', 'SMP Negeri 5', 'SMA Negeri 3', 'Dapur Pusat'],
        'status': ['Delivered', 'In Transit', 'Delayed', 'Ready'],
        'temp': [25.5, 28.2, 32.1, 22.0]
    })
    
    st.map(map_data[['lat', 'lon']], use_container_width=True)
    
    # Current deliveries table
    st.markdown("### 🚚 Status Pengiriman Saat Ini")
    
    current_deliveries = pd.DataFrame({
        'Batch ID': [f'BATCH_{i:03d}' for i in range(1, 11)],
        'Produsen': [random.choice(['Katering Sehat', 'Nutrisi Prima', 'Makanan Bergizi']) for _ in range(10)],
        'Tujuan': [random.choice(['SDN Bandung 1', 'SMP Negeri 5', 'SMA Negeri 3']) for _ in range(10)],
        'Status': [random.choice(['Loading', 'In Transit', 'Delivered', 'Delayed']) for _ in range(10)],
        'Suhu (°C)': [round(random.uniform(20, 35), 1) for _ in range(10)],
        'ETA': [f'{random.randint(10, 60)} menit' for _ in range(10)]
    })
    
    # Color code the status
    def highlight_status(val):
        if val == 'Delivered':
            return 'background-color: #4ecdc4'
        elif val == 'In Transit':
            return 'background-color: #74b9ff'
        elif val == 'Delayed':
            return 'background-color: #ff6b6b'
        else:
            return 'background-color: #feca57'
    
    styled_df = current_deliveries.style.applymap(highlight_status, subset=['Status'])
    st.dataframe(styled_df, use_container_width=True)

def main():
    """Fungsi utama aplikasi"""
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        
        page = st.selectbox(
            "Pilih Dashboard:",
            ["📊 Dashboard Utama", "⚡ Real-time Monitoring"]
        )
        
        st.markdown("---")
        st.markdown("### ℹ️ Info Dashboard")
        st.info("""
        Dashboard ini menyediakan analisis komprehensif untuk:
        
        🔍 **Root Cause Analysis**
        - Identifikasi penyebab makanan basi
        - Analisis korelasi faktor-faktor
        
        📊 **Monitoring Kualitas**
        - Tracking tingkat kebusukan
        - Evaluasi performa produsen
        
        🚚 **Analisis Pengiriman**
        - Durasi per tahapan
        - Optimasi rute dan waktu
        
        📈 **Prediksi & Trend**
        - Forecasting tingkat kebusukan
        - Pattern analysis
        """)
        
        st.markdown("---")
        st.markdown("### 📞 Emergency Contact")
        st.error("🚨 Hotline: **0800-1234-5678**")
    
    # Route berdasarkan pilihan
    if page == "📊 Dashboard Utama":
        main_dashboard()
    elif page == "⚡ Real-time Monitoring":
        realtime_monitoring()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <h4>📊 Dashboard Pemangku Kepentingan</h4>
        <p><strong>Sistem Monitoring Kualitas Makanan Bergizi Gratis</strong></p>
        <p>Developed with ❤️ for Better Food Quality Management</p>
        <small>© 2025 - Advanced Analytics & Real-time Monitoring System</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()