
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# Konfigurasi halaman
st.set_page_config(
    page_title="Simulasi Proyek Kereta Bawah Tanah AI",
    page_icon="🚇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS untuk styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .phase-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ff7f0e;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .alert-danger {
        background-color: #ffe6e6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ff0000;
    }
    .alert-success {
        background-color: #e6ffe6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #00ff00;
    }
    .advanced-params {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #6c757d;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Kelas untuk Data Management
class ProjectDataManager:
    def __init__(self):
        self.initialize_data()
    
    def initialize_data(self):
        # Data Geoteknik
        self.geotechnical_data = pd.DataFrame({
            'segment': [f'Segment {i}' for i in range(1, 21)],
            'soil_type': np.random.choice(['Clay', 'Sand', 'Rock', 'Mixed'], 20),
            'water_level': np.random.uniform(2, 15, 20),
            'risk_factor': np.random.uniform(0.1, 0.9, 20)
        })
        
        # Data Historis Proyek
        self.historical_data = pd.DataFrame({
            'project_id': range(1, 51),
            'duration_days': np.random.normal(365, 60, 50).astype(int),
            'cost_million': np.random.normal(100, 20, 50),
            'tunnel_length_km': np.random.uniform(5, 25, 50),
            'soil_difficulty': np.random.uniform(0.2, 0.8, 50),
            'team_size': np.random.randint(50, 200, 50),
            'tunnel_depth': np.random.uniform(10, 50, 50),
            'station_count': np.random.randint(3, 15, 50),
            'tbm_count': np.random.randint(1, 4, 50)
        })
        
        # Data Sumber Daya
        self.resources = {
            'TBM': {'quantity': 2, 'cost_per_day': 50000, 'efficiency': 0.85},
            'Workers': {'quantity': 150, 'cost_per_day': 300, 'productivity': 0.9},
            'Concrete': {'quantity': 10000, 'cost_per_unit': 100, 'availability': 0.95},
            'Steel': {'quantity': 2000, 'cost_per_unit': 800, 'availability': 0.9},
            'Ventilation': {'quantity': 5, 'cost_per_day': 2000, 'efficiency': 0.8}
        }

# Kelas untuk AI Models
class AIModels:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.models = {}
        self.train_models()
    
    def train_models(self):
        data = self.data_manager.historical_data
        
        # Model Durasi
        X_duration = data[['tunnel_length_km', 'soil_difficulty', 'team_size', 'tunnel_depth', 'station_count', 'tbm_count']]
        y_duration = data['duration_days']
        X_train, X_test, y_train, y_test = train_test_split(X_duration, y_duration, test_size=0.2, random_state=42)
        
        self.models['duration'] = RandomForestRegressor(n_estimators=100, random_state=42)
        self.models['duration'].fit(X_train, y_train)
        
        # Model Biaya
        X_cost = data[['tunnel_length_km', 'soil_difficulty', 'team_size', 'tunnel_depth', 'station_count', 'tbm_count', 'duration_days']]
        y_cost = data['cost_million']
        X_train_cost, X_test_cost, y_train_cost, y_test_cost = train_test_split(X_cost, y_cost, test_size=0.2, random_state=42)
        
        self.models['cost'] = RandomForestRegressor(n_estimators=100, random_state=42)
        self.models['cost'].fit(X_train_cost, y_train_cost)
    
    def predict_project_metrics(self, tunnel_length, soil_difficulty, team_size, tunnel_depth, station_count, tbm_count):
        duration_pred = self.models['duration'].predict([[tunnel_length, soil_difficulty, team_size, tunnel_depth, station_count, tbm_count]])[0]
        cost_pred = self.models['cost'].predict([[tunnel_length, soil_difficulty, team_size, tunnel_depth, station_count, tbm_count, duration_pred]])[0]
        
        return max(duration_pred, 1), max(cost_pred, 0)  # Ensure non-negative predictions
    
    def risk_assessment(self, geotechnical_data, water_table, urban_density):
        risks = []
        for _, row in geotechnical_data.iterrows():
            risk_level = row['risk_factor']
            soil_type = row['soil_type']
            water_level = row['water_level']
            
            adjusted_risk = risk_level * (1 + (water_level - water_table)/10) * (1 + urban_density*0.5)
            
            if adjusted_risk > 0.7 or water_level > water_table:
                risk_category = "High"
            elif adjusted_risk > 0.4 or water_level > water_table - 3:
                risk_category = "Medium"
            else:
                risk_category = "Low"
            
            risks.append({
                'segment': row['segment'],
                'risk_level': risk_category,
                'risk_score': adjusted_risk,
                'primary_concern': self._get_primary_concern(soil_type, water_level, adjusted_risk)
            })
        
        return risks
    
    def _get_primary_concern(self, soil_type, water_level, risk_factor):
        if water_level > 10:
            return "Water infiltration"
        elif soil_type == "Rock" and risk_factor > 0.6:
            return "Hard rock excavation"
        elif soil_type == "Clay" and risk_factor > 0.5:
            return "Soil instability"
        elif soil_type == "Sand" and risk_factor > 0.4:
            return "Ground settlement"
        else:
            return "Standard conditions"

# Kelas untuk Simulasi
class SimulationEngine:
    def __init__(self, data_manager, ai_models):
        self.data_manager = data_manager
        self.ai_models = ai_models
        self.simulation_results = {}
    
    def run_simulation(self, project_params):
        tunnel_length = project_params['tunnel_length']
        team_size = project_params['team_size']
        soil_difficulty = project_params['soil_difficulty']
        tunnel_depth = project_params['tunnel_depth']
        station_count = project_params['station_count']
        tbm_count = project_params['tbm_count']
        tbm_efficiency = project_params['tbm_efficiency']
        urban_density = project_params['urban_density']
        water_table = project_params['water_table']
        contingency_percent = project_params['contingency_percent']
        inflation_rate = project_params['inflation_rate']
        shift_pattern = project_params['shift_pattern']
        
        duration_pred, cost_pred = self.ai_models.predict_project_metrics(
            tunnel_length, soil_difficulty, team_size, tunnel_depth, station_count, tbm_count
        )
        
        tbm_factor = tbm_count * tbm_efficiency
        duration_pred *= (1 / tbm_factor)
        
        if shift_pattern == '2 Shift':
            duration_pred *= 0.85
        elif shift_pattern == '3 Shift (24 jam)':
            duration_pred *= 0.7
        
        duration_pred *= (1 + urban_density * 0.2)
        
        inflation_factor = (1 + inflation_rate) ** (duration_pred / 365)
        cost_pred *= (1 + contingency_percent/100) * inflation_factor
        
        daily_progress = self._simulate_daily_progress(int(duration_pred), tunnel_length, tbm_factor, shift_pattern)
        cumulative_costs = self._simulate_cumulative_costs(int(duration_pred), cost_pred, inflation_rate)
        risks = self.ai_models.risk_assessment(self.data_manager.geotechnical_data, water_table, urban_density)
        resource_util = self._calculate_resource_utilization(team_size, int(duration_pred), tbm_count, shift_pattern)
        
        self.simulation_results = {
            'duration': duration_pred,
            'cost': cost_pred,
            'daily_progress': daily_progress,
            'cumulative_costs': cumulative_costs,
            'risks': risks,
            'resource_utilization': resource_util,
            'timeline': self._generate_timeline(int(duration_pred)),
            'project_params': project_params
        }
        
        return self.simulation_results
    
    def _simulate_daily_progress(self, duration, tunnel_length, tbm_factor, shift_pattern):
        dates = pd.date_range(start=datetime.now(), periods=max(duration, 1), freq='D')
        
        base_progress = (tunnel_length / max(duration, 1)) * tbm_factor
        if shift_pattern == '2 Shift':
            base_progress *= 1.5
        elif shift_pattern == '3 Shift (24 jam)':
            base_progress *= 2.0
            
        daily_progress = []
        cumulative_progress = 0
        
        for i in range(len(dates)):
            variation = 0.3 if dates[i].weekday() >= 5 and shift_pattern == '1 Shift' else np.random.normal(1.0, 0.15)
            day_progress = base_progress * max(0.1, variation)
            cumulative_progress += day_progress
            
            daily_progress.append({
                'date': dates[i],
                'daily_progress': day_progress,
                'cumulative_progress': min(cumulative_progress, tunnel_length),
                'progress_percentage': min(cumulative_progress / tunnel_length * 100, 100)
            })
        
        return pd.DataFrame(daily_progress)
    
    def _simulate_cumulative_costs(self, duration, total_cost, inflation_rate):
        t = np.linspace(0, 1, max(duration, 1))
        s_curve = 1 / (1 + np.exp(-8 * (t - 0.5)))
        
        cumulative_costs = []
        for i, cost_ratio in enumerate(s_curve):
            daily_inflation = (1 + inflation_rate/365) ** i
            cumulative_cost = total_cost * cost_ratio * daily_inflation
            daily_cost = total_cost * (s_curve[i] - s_curve[i-1] if i > 0 else s_curve[i]) * daily_inflation
            
            cumulative_costs.append({
                'day': i + 1,
                'cumulative_cost': cumulative_cost,
                'daily_cost': daily_cost,
                'inflation_adjusted_cost': cumulative_cost
            })
        
        return pd.DataFrame(cumulative_costs)
    
    def _calculate_resource_utilization(self, team_size, duration, tbm_count, shift_pattern):
        resources = self.data_manager.resources
        resources['TBM']['quantity'] = tbm_count
        
        utilization = {}
        for resource, data in resources.items():
            if resource == 'Workers':
                base_workers = team_size
                if shift_pattern == '2 Shift':
                    utilized = int(base_workers * 1.5 * np.random.uniform(0.8, 0.95))
                elif shift_pattern == '3 Shift (24 jam)':
                    utilized = int(base_workers * 2.0 * np.random.uniform(0.7, 0.9))
                else:
                    utilized = int(base_workers * np.random.uniform(0.8, 0.95))
                
                utilization[resource] = {
                    'available': base_workers,
                    'utilized': utilized,
                    'efficiency': np.random.uniform(0.85, 0.95)
                }
            else:
                utilization[resource] = {
                    'available': data['quantity'],
                    'utilized': int(data['quantity'] * np.random.uniform(0.7, 0.9)),
                    'efficiency': data.get('efficiency', np.random.uniform(0.8, 0.9))
                }
        
        return utilization
    
    def _generate_timeline(self, duration):
        milestones = [
            {'name': 'Project Initiation', 'day': 0, 'status': 'completed'},
            {'name': 'Site Preparation', 'day': int(duration * 0.1), 'status': 'completed'},
            {'name': 'TBM Installation', 'day': int(duration * 0.15), 'status': 'in_progress'},
            {'name': 'Tunnel Excavation Start', 'day': int(duration * 0.2), 'status': 'planned'},
            {'name': '25% Completion', 'day': int(duration * 0.35), 'status': 'planned'},
            {'name': '50% Completion', 'day': int(duration * 0.55), 'status': 'planned'},
            {'name': 'Station Construction', 'day': int(duration * 0.65), 'status': 'planned'},
            {'name': '75% Completion', 'day': int(duration * 0.75), 'status': 'planned'},
            {'name': 'System Integration', 'day': int(duration * 0.85), 'status': 'planned'},
            {'name': 'Testing & Commissioning', 'day': int(duration * 0.95), 'status': 'planned'},
            {'name': 'Project Completion', 'day': duration, 'status': 'planned'}
        ]
        
        return milestones

# Fungsi untuk membuat visualisasi
def create_project_dashboard(simulation_results):
    fig_progress = px.line(
        simulation_results['daily_progress'], 
        x='date', 
        y='progress_percentage',
        title='Project Progress Over Time',
        labels={'progress_percentage': 'Progress (%)', 'date': 'Date'},
        template='plotly_white'
    )
    fig_progress.update_layout(
        height=400,
        hovermode='x unified',
        yaxis_range=[0, 100]
    )
    
    fig_cost = px.line(
        simulation_results['cumulative_costs'], 
        x='day', 
        y='cumulative_cost',
        title='Cumulative Cost Over Time',
        labels={'cumulative_cost': 'Cost (Million USD)', 'day': 'Project Day'},
        template='plotly_white'
    )
    fig_cost.update_layout(
        height=400,
        hovermode='x unified'
    )
    
    fig_combined = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=False,
        subplot_titles=('Project Progress', 'Cumulative Costs'),
        vertical_spacing=0.15
    )
    
    fig_combined.add_trace(
        go.Scatter(
            x=simulation_results['daily_progress']['date'],
            y=simulation_results['daily_progress']['progress_percentage'],
            name='Progress (%)',
            line=dict(color='#1f77b4')
        ),
        row=1, col=1
    )
    
    fig_combined.add_trace(
        go.Scatter(
            x=simulation_results['cumulative_costs']['day'],
            y=simulation_results['cumulative_costs']['cumulative_cost'],
            name='Cost (Million USD)',
            line=dict(color='#ff7f0e')
        ),
        row=2, col=1
    )
    
    fig_combined.update_layout(
        height=600,
        showlegend=True,
        hovermode='x unified',
        xaxis2_title='Project Day',
        yaxis_title='Progress (%)',
        yaxis2_title='Cost (Million USD)'
    )
    
    return fig_progress, fig_cost, fig_combined

def create_risk_dashboard(risks):
    risk_df = pd.DataFrame(risks)
    
    fig_risk = px.pie(
        risk_df, 
        names='risk_level', 
        title='Risk Distribution by Segments',
        color='risk_level',
        color_discrete_map={
            'High': '#ff4444',
            'Medium': '#ffaa00', 
            'Low': '#44ff44'
        },
        hole=0.3,
        template='plotly_white'
    )
    
    fig_segment_risk = px.bar(
        risk_df, 
        x='segment', 
        y='risk_score',
        color='risk_level',
        title='Risk Score by Segment',
        color_discrete_map={
            'High': '#ff4444',
            'Medium': '#ffaa00', 
            'Low': '#44ff44'
        },
        template='plotly_white'
    )
    fig_segment_risk.update_layout(
        height=400,
        xaxis={'categoryorder':'total descending'}
    )
    
    fig_heatmap = px.density_heatmap(
        risk_df,
        x='segment',
        y='primary_concern',
        z='risk_score',
        title='Risk Heatmap by Segment and Concern',
        template='plotly_white'
    )
    
    return fig_risk, fig_segment_risk, fig_heatmap

def create_resource_dashboard(resource_util):
    resources = list(resource_util.keys())
    utilized = [resource_util[r]['utilized'] for r in resources]
    available = [resource_util[r]['available'] for r in resources]
    efficiency = [resource_util[r]['efficiency'] * 100 for r in resources]
    utilization_rate = [(u/a)*100 if a > 0 else 0 for u, a in zip(utilized, available)]
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Resource Utilization', 'Resource Efficiency', 
                       'Availability vs Utilization', 'Utilization Rate'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "xy"}, {"type": "pie"}]],
        horizontal_spacing=0.15,
        vertical_spacing=0.2
    )
    
    fig.add_trace(
        go.Bar(
            x=resources,
            y=utilized,
            name='Utilized',
            marker_color='#1f77b4',
            text=utilized,
            textposition='auto'
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(
            x=resources,
            y=efficiency,
            name='Efficiency (%)',
            marker_color='#2ca02c',
            text=[f"{e:.1f}%" for e in efficiency],
            textposition='auto'
        ),
        row=1, col=2
    )
    
    fig.add_hline(
        y=80,
        line_dash="dot",
        line_color="red",
        row=1, col=2,
        annotation_text="Target Efficiency",
        annotation_position="top right"
    )
    
    fig.add_trace(
        go.Scatter(
            x=available,
            y=utilized,
            mode='markers+text',
            text=resources,
            textposition='top center',
            marker=dict(
                size=12,
                color=utilization_rate,
                colorscale='Viridis',
                showscale=True
            ),
            name='Available vs Utilized'
        ),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Pie(
            labels=resources,
            values=utilization_rate,
            name='Utilization Rate',
            marker_colors=px.colors.qualitative.Pastel,
            textinfo='percent+label',
            hoverinfo='label+value'
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        height=800,
        showlegend=False,
        template='plotly_white',
        title_text="Resource Utilization Dashboard",
        margin=dict(t=100)
    )
    
    return fig

def create_what_if_analysis(project_params, ai_models):
    base_duration, base_cost = ai_models.predict_project_metrics(
        project_params['tunnel_length'],
        project_params['soil_difficulty'],
        project_params['team_size'],
        project_params['tunnel_depth'],
        project_params['station_count'],
        project_params['tbm_count']
    )
    
    tbm_factor = project_params['tbm_count'] * project_params['tbm_efficiency']
    base_duration *= (1 / tbm_factor)
    
    if project_params['shift_pattern'] == '2 Shift':
        base_duration *= 0.85
    elif project_params['shift_pattern'] == '3 Shift (24 jam)':
        base_duration *= 0.7
    
    base_duration *= (1 + project_params['urban_density'] * 0.2)
    inflation_factor = (1 + project_params['inflation_rate']) ** (base_duration / 365)
    base_cost *= (1 + project_params['contingency_percent']/100) * inflation_factor
    
    opt_params = {
        'soil_difficulty': max(0.1, project_params['soil_difficulty'] - 0.2),
        'tbm_count': min(5, project_params['tbm_count'] + 1),
        'tbm_efficiency': min(1.0, project_params['tbm_efficiency'] + 0.1),
        'team_size': int(project_params['team_size'] * 1.1),
        'shift_pattern': '3 Shift (24 jam)' if project_params['shift_pattern'] != '3 Shift (24 jam)' else project_params['shift_pattern'],
        'contingency_percent': max(5, project_params['contingency_percent'] - 5)
    }
    
    opt_duration, opt_cost = ai_models.predict_project_metrics(
        project_params['tunnel_length'],
        opt_params['soil_difficulty'],
        opt_params['team_size'],
        project_params['tunnel_depth'],
        project_params['station_count'],
        opt_params['tbm_count']
    )
    
    opt_tbm_factor = opt_params['tbm_count'] * opt_params['tbm_efficiency']
    opt_duration *= (1 / opt_tbm_factor)
    opt_duration *= 0.7
    inflation_factor = (1 + project_params['inflation_rate']) ** (opt_duration / 365)
    opt_cost *= (1 + opt_params['contingency_percent']/100) * inflation_factor
    
    pes_params = {
        'soil_difficulty': min(1.0, project_params['soil_difficulty'] + 0.3),
        'tbm_count': max(1, project_params['tbm_count'] - 1),
        'tbm_efficiency': max(0.5, project_params['tbm_efficiency'] - 0.15),
        'team_size': int(project_params['team_size'] * 0.9),
        'shift_pattern': '1 Shift' if project_params['shift_pattern'] != '1 Shift' else project_params['shift_pattern'],
        'contingency_percent': min(30, project_params['contingency_percent'] + 10)
    }
    
    pes_duration, pes_cost = ai_models.predict_project_metrics(
        project_params['tunnel_length'],
        pes_params['soil_difficulty'],
        pes_params['team_size'],
        project_params['tunnel_depth'],
        project_params['station_count'],
        pes_params['tbm_count']
    )
    
    pes_tbm_factor = pes_params['tbm_count'] * pes_params['tbm_efficiency']
    pes_duration *= (1 / pes_tbm_factor)
    if pes_params['shift_pattern'] == '1 Shift':
        pes_duration *= 1.0
    inflation_factor = (1 + project_params['inflation_rate']) ** (pes_duration / 365)
    pes_cost *= (1 + pes_params['contingency_percent']/100) * inflation_factor
    
    scenario_data = pd.DataFrame({
        'Scenario': ['Baseline', 'Optimistic', 'Pessimistic'],
        'Duration (days)': [base_duration, opt_duration, pes_duration],
        'Cost (Million USD)': [base_cost, opt_cost, pes_cost],
        'Cost per km (Million USD)': [
            base_cost/project_params['tunnel_length'],
            opt_cost/project_params['tunnel_length'],
            pes_cost/project_params['tunnel_length']
        ]
    })
    
    scenario_data['Duration (days, numeric)'] = scenario_data['Duration (days)']
    scenario_data['Cost (Million USD, numeric)'] = scenario_data['Cost (Million USD)']
    scenario_data['Cost per km (Million USD, numeric)'] = scenario_data['Cost per km (Million USD)']
    
    scenario_data['Duration (days)'] = scenario_data['Duration (days)'].apply(lambda x: f"{x:.1f}")
    scenario_data['Cost (Million USD)'] = scenario_data['Cost (Million USD)'].apply(lambda x: f"${x:,.1f}")
    scenario_data['Cost per km (Million USD)'] = scenario_data['Cost per km (Million USD)'].apply(lambda x: f"${x:,.1f}")
    
    fig_scenario = px.scatter(
        scenario_data, 
        x='Duration (days, numeric)', 
        y='Cost (Million USD, numeric)', 
        color='Scenario',
        size='Cost per km (Million USD, numeric)', 
        text='Scenario',
        title='Scenario Comparison: Duration vs Cost',
        template='plotly_white',
        color_discrete_map={
            'Optimistic': '#2ca02c',
            'Baseline': '#1f77b4',
            'Pessimistic': '#d62728'
        }
    )
    fig_scenario.update_traces(
        textposition='top center',
        marker=dict(size=100, line=dict(width=2, color='DarkSlateGrey')),
        selector=dict(mode='markers+text')
    )
    fig_scenario.update_layout(
        height=500,
        hovermode='closest',
        xaxis_title='Duration (days)',
        yaxis_title='Cost (Million USD)'
    )
    
    param_comparison = pd.DataFrame({
        'Parameter': [
            'Soil Difficulty',
            'TBM Count',
            'TBM Efficiency',
            'Team Size',
            'Shift Pattern',
            'Contingency %'
        ],
        'Baseline': [
            f"{project_params['soil_difficulty']:.2f}",
            project_params['tbm_count'],
            f"{project_params['tbm_efficiency']*100:.1f}%",
            project_params['team_size'],
            project_params['shift_pattern'],
            f"{project_params['contingency_percent']}%"
        ],
        'Optimistic': [
            f"{opt_params['soil_difficulty']:.2f}",
            opt_params['tbm_count'],
            f"{opt_params['tbm_efficiency']*100:.1f}%",
            opt_params['team_size'],
            opt_params['shift_pattern'],
            f"{opt_params['contingency_percent']}%"
        ],
        'Pessimistic': [
            f"{pes_params['soil_difficulty']:.2f}",
            pes_params['tbm_count'],
            f"{pes_params['tbm_efficiency']*100:.1f}%",
            pes_params['team_size'],
            pes_params['shift_pattern'],
            f"{pes_params['contingency_percent']}%"
        ]
    })
    
    return fig_scenario, param_comparison, scenario_data

# Main Application
def main():
    st.markdown('<h1 class="main-header">🚇 Simulasi Proyek Kereta Bawah Tanah Berbasis AI</h1>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'data_manager' not in st.session_state:
        st.session_state.data_manager = ProjectDataManager()
        st.session_state.ai_models = AIModels(st.session_state.data_manager)
        st.session_state.simulation_engine = SimulationEngine(
            st.session_state.data_manager, 
            st.session_state.ai_models
        )
    
    # Sidebar untuk parameter input
    st.sidebar.markdown('<h2 class="phase-header">📊 Parameter Proyek</h2>', unsafe_allow_html=True)
    
    tunnel_length = st.sidebar.slider(
        "Panjang Terowongan (km)", 
        min_value=5.0, 
        max_value=30.0, 
        value=15.0, 
        step=0.5,
        help="Total panjang terowongan yang akan dibangun"
    )
    
    team_size = st.sidebar.slider(
        "Ukuran Tim", 
        min_value=50, 
        max_value=300, 
        value=150, 
        step=10,
        help="Jumlah pekerja di lapangan"
    )
    
    soil_difficulty = st.sidebar.slider(
        "Tingkat Kesulitan Tanah", 
        min_value=0.1, 
        max_value=1.0, 
        value=0.5, 
        step=0.1,
        help="Tingkat kesulitan geoteknik proyek"
    )
    
    with st.sidebar.expander("⚙️ Parameter Lanjutan", expanded=False):
        st.markdown('<div class="advanced-params">', unsafe_allow_html=True)
        
        tunnel_depth = st.slider(
            "Kedalaman Rata-rata Terowongan (m)", 
            min_value=10, 
            max_value=50, 
            value=25, 
            step=5,
            help="Kedalaman rata-rata terowongan dari permukaan tanah"
        )
        
        station_count = st.slider(
            "Jumlah Stasiun", 
            min_value=3, 
            max_value=15, 
            value=8, 
            step=1,
            help="Total stasiun yang akan dibangun"
        )
        
        tunnel_diameter = st.slider(
            "Diameter Terowongan (m)", 
            min_value=4.0, 
            max_value=10.0, 
            value=6.5, 
            step=0.5,
            help="Diameter terowongan yang akan dibangun"
        )
        
        tbm_count = st.slider(
            "Jumlah TBM (Tunnel Boring Machine)", 
            min_value=1, 
            max_value=5, 
            value=2, 
            step=1,
            help="Jumlah mesin bor yang akan digunakan"
        )
        
        tbm_efficiency = st.slider(
            "Efisiensi TBM (%)", 
            min_value=50, 
            max_value=100, 
            value=85, 
            step=5,
            help="Efisiensi operasional TBM"
        )
        
        urban_density = st.slider(
            "Kepadatan Urban di Atas Terowongan", 
            min_value=0.1, 
            max_value=1.0, 
            value=0.5, 
            step=0.1,
            help="Tingkat kesulitan karena bangunan di atas"
        )
        
        water_table = st.slider(
            "Tinggi Muka Air Tanah (m di bawah permukaan)", 
            min_value=2, 
            max_value=20, 
            value=8, 
            step=1,
            help="Kedalaman muka air tanah dari permukaan"
        )
        
        contingency_percent = st.slider(
            "Kontinjensi Biaya (%)", 
            min_value=5, 
            max_value=30, 
            value=15, 
            step=1,
            help="Persentase biaya cadangan untuk risiko"
        )
        
        inflation_rate = st.slider(
            "Tingkat Inflasi Tahunan (%)", 
            min_value=1, 
            max_value=10, 
            value=3, 
            step=1,
            help="Tingkat inflasi untuk perhitungan biaya"
        )
        
        shift_pattern = st.select_slider(
            "Pola Kerja", 
            options=['1 Shift', '2 Shift', '3 Shift (24 jam)'], 
            value='2 Shift',
            help="Pola kerja harian"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.sidebar.button("🚀 Jalankan Simulasi", type="primary", use_container_width=True):
        project_params = {
            'tunnel_length': tunnel_length,
            'team_size': team_size,
            'soil_difficulty': soil_difficulty,
            'tunnel_depth': tunnel_depth,
            'station_count': station_count,
            'tunnel_diameter': tunnel_diameter,
            'tbm_count': tbm_count,
            'tbm_efficiency': tbm_efficiency/100,
            'urban_density': urban_density,
            'water_table': water_table,
            'contingency_percent': contingency_percent,
            'inflation_rate': inflation_rate/100,
            'shift_pattern': shift_pattern
        }
        
        try:
            with st.spinner('Menjalankan simulasi AI...'):
                results = st.session_state.simulation_engine.run_simulation(project_params)
                st.session_state.simulation_results = results
            
            st.success('✅ Simulasi berhasil dijalankan!')
        except Exception as e:
            st.error(f"❌ Gagal menjalankan simulasi: {str(e)}")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Dashboard Utama", 
        "⚠️ Analisis Risiko", 
        "🔧 Sumber Daya", 
        "🎯 Skenario What-If",
        "📋 Timeline & KPI"
    ])
    
    if 'simulation_results' in st.session_state:
        results = st.session_state.simulation_results
        
        with tab1:
            st.markdown('<h2 class="phase-header">Dashboard Utama</h2>', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Estimasi Durasi", 
                    f"{results['duration']:.0f} hari",
                    delta=f"{results['duration'] - 365:.0f} vs baseline",
                    help="Total durasi proyek yang diprediksi"
                )
            
            with col2:
                st.metric(
                    "Estimasi Biaya", 
                    f"${results['cost']:,.1f}M",
                    delta=f"${results['cost'] - 100:,.1f}M vs baseline",
                    help="Total biaya proyek termasuk kontinjensi dan inflasi"
                )
            
            with col3:
                completion_rate = results['daily_progress']['progress_percentage'].iloc[-1]
                st.metric(
                    "Progress Simulasi", 
                    f"{completion_rate:.1f}%",
                    delta="On track" if completion_rate >= 99.9 else "Behind schedule",
                    help="Progress simulasi terakhir"
                )
            
            with col4:
                high_risk_count = sum(1 for r in results['risks'] if r['risk_level'] == 'High')
                st.metric(
                    "Segmen Risiko Tinggi", 
                    f"{high_risk_count}",
                    delta=f"{high_risk_count - 3} vs acceptable",
                    help="Jumlah segmen dengan risiko tinggi"
                )
            
            fig_progress, fig_cost, fig_combined = create_project_dashboard(results)
            
            st.plotly_chart(fig_combined, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig_progress, use_container_width=True)
            with col2:
                st.plotly_chart(fig_cost, use_container_width=True)
            
            st.markdown("### 📋 Ringkasan Parameter Proyek")
            param_summary = pd.DataFrame({
                'Parameter': [
                    'Panjang Terowongan',
                    'Kedalaman Terowongan',
                    'Jumlah Stasiun',
                    'Diameter Terowongan',
                    'Ukuran Tim',
                    'Jumlah TBM',
                    'Efisiensi TBM',
                    'Pola Kerja',
                    'Kepadatan Urban',
                    'Muka Air Tanah',
                    'Kontinjensi',
                    'Inflasi Tahunan'
                ],
                'Nilai': [
                    f"{results['project_params']['tunnel_length']} km",
                    f"{results['project_params']['tunnel_depth']} m",
                    results['project_params']['station_count'],
                    f"{results['project_params']['tunnel_diameter']} m",
                    results['project_params']['team_size'],
                    results['project_params']['tbm_count'],
                    f"{results['project_params']['tbm_efficiency']*100:.1f}%",
                    results['project_params']['shift_pattern'],
                    f"{results['project_params']['urban_density']:.1f}",
                    f"{results['project_params']['water_table']} m",
                    f"{results['project_params']['contingency_percent']}%",
                    f"{results['project_params']['inflation_rate']*100:.1f}%"
                ]
            })
            st.dataframe(param_summary, use_container_width=True, hide_index=True)
        
        with tab2:
            st.markdown('<h2 class="phase-header">Analisis Risiko</h2>', unsafe_allow_html=True)
            
            fig_risk, fig_segment_risk, fig_heatmap = create_risk_dashboard(results['risks'])
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig_risk, use_container_width=True)
            with col2:
                st.plotly_chart(fig_segment_risk, use_container_width=True)
            
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
            st.markdown("### 📊 Detail Risiko per Segmen")
            risk_df = pd.DataFrame(results['risks'])
            risk_df['risk_score'] = risk_df['risk_score'].apply(lambda x: f"{x:.2f}")
            st.dataframe(risk_df, use_container_width=True)
            
            high_risk_segments = [r for r in results['risks'] if r['risk_level'] == 'High']
            if high_risk_segments:
                st.markdown("### 🚨 Rekomendasi untuk Segmen Berisiko Tinggi:")
                for segment in high_risk_segments:
                    st.markdown(f"""
                    <div class="alert-danger">
                    <strong>{segment['segment']}</strong>: {segment['primary_concern']}<br>
                    <em>Rekomendasi: Lakukan inspeksi tambahan dan siapkan mitigasi khusus.</em>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="alert-success">
                <strong>Tidak ada segmen dengan risiko tinggi</strong><br>
                <em>Proyek memiliki profil risiko yang dapat diterima</em>
                </div>
                """, unsafe_allow_html=True)
        
        with tab3:
            st.markdown('<h2 class="phase-header">Manajemen Sumber Daya</h2>', unsafe_allow_html=True)
            
            fig_resource = create_resource_dashboard(results['resource_utilization'])
            st.plotly_chart(fig_resource, use_container_width=True)
            
            st.markdown("### 💡 Rekomendasi Optimalisasi Sumber Daya:")
            
            for resource, data in results['resource_utilization'].items():
                utilization_rate = (data['utilized'] / data['available']) * 100 if data['available'] > 0 else 0
                efficiency = data['efficiency'] * 100
                
                if utilization_rate < 70:
                    st.markdown(f"""
                    <div class="alert-danger">
                    <strong>{resource}</strong>: Utilisasi rendah ({utilization_rate:.1f}%)<br>
                    <em>Rekomendasi: Realokasi atau kurangi sumber daya berlebih.</em>
                    </div>
                    """, unsafe_allow_html=True)
                elif efficiency < 85:
                    st.markdown(f"""
                    <div class="alert-danger">
                    <strong>{resource}</strong>: Efisiensi rendah ({efficiency:.1f}%)<br>
                    <em>Rekomendasi: Pelatihan atau pemeliharaan tambahan diperlukan.</em>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="alert-success">
                    <strong>{resource}</strong>: Optimal (Utilisasi: {utilization_rate:.1f}%, Efisiensi: {efficiency:.1f}%)
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab4:
            st.markdown('<h2 class="phase-header">Analisis Skenario What-If</h2>', unsafe_allow_html=True)
            
            fig_scenario, param_comparison, scenario_data = create_what_if_analysis(
                results['project_params'],
                st.session_state.ai_models
            )
            
            st.plotly_chart(fig_scenario, use_container_width=True)
            
            st.markdown("### 📊 Perbandingan Parameter Skenario")
            st.dataframe(param_comparison, use_container_width=True, hide_index=True)
            
            st.markdown("### 📈 Perbandingan Hasil Skenario")
            st.dataframe(scenario_data, use_container_width=True, hide_index=True)
            
            st.markdown("### 💰 Analisis Biaya-Manfaat")
            
            base_cost = float(scenario_data.loc[0, 'Cost (Million USD)'].replace('$', '').replace(',', ''))
            opt_cost = float(scenario_data.loc[1, 'Cost (Million USD)'].replace('$', '').replace(',', ''))
            pes_cost = float(scenario_data.loc[2, 'Cost (Million USD)'].replace('$', '').replace(',', ''))
            
            base_duration = float(scenario_data.loc[0, 'Duration (days)'])
            opt_duration = float(scenario_data.loc[1, 'Duration (days)'])
            pes_duration = float(scenario_data.loc[2, 'Duration (days)'])
            
            cost_diff_opt = opt_cost - base_cost
            duration_diff_opt = opt_duration - base_duration
            
            cost_diff_pes = pes_cost - base_cost
            duration_diff_pes = pes_duration - base_duration
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Skenario Optimis vs Baseline:**")
                st.metric("Perbedaan Biaya", f"${cost_diff_opt:,.1f}M", 
                         delta_color="inverse" if cost_diff_opt < 0 else "normal")
                st.metric("Perbedaan Durasi", f"{duration_diff_opt:.0f} hari", 
                         delta_color="inverse" if duration_diff_opt < 0 else "normal")
            
            with col2:
                st.markdown("**Skenario Pesimis vs Baseline:**")
                st.metric("Perbedaan Biaya", f"${cost_diff_pes:,.1f}M", 
                         delta_color="inverse" if cost_diff_pes < 0 else "normal")
                st.metric("Perbedaan Durasi", f"{duration_diff_pes:.0f} hari", 
                         delta_color="inverse" if duration_diff_pes < 0 else "normal")
        
        with tab5:
            st.markdown('<h2 class="phase-header">Timeline & KPI</h2>', unsafe_allow_html=True)
            
            st.markdown("### 📅 Timeline Proyek")
            timeline_df = pd.DataFrame(results['timeline'])
            
            timeline_df['color'] = timeline_df['status'].map({
                'completed': '🟢',
                'in_progress': '🟡', 
                'planned': '⚪'
            })
            
            for _, milestone in timeline_df.iterrows():
                st.markdown(f"""
                {milestone['color']} **{milestone['name']}** - Hari {milestone['day']} ({milestone['status'].replace('_', ' ')})
                """)
            
            fig_gantt = px.timeline(
                timeline_df.assign(
                    start_date=lambda x: pd.date_range(start=datetime.now(), periods=len(x), freq='D'),
                    end_date=lambda x: x['start_date'] + pd.Timedelta(days=1)
                ),
                x_start="start_date",
                x_end="end_date",
                y="name",
                color="status",
                color_discrete_map={
                    'completed': '#2ca02c',
                    'in_progress': '#ff7f0e',
                    'planned': '#1f77b4'
                },
                title="Gantt Chart Timeline Proyek"
            )
            fig_gantt.update_yaxes(autorange="reversed")
            st.plotly_chart(fig_gantt, use_container_width=True)
            
            st.markdown("### 📊 Ringkasan KPI")
            
            kpi_data = {
                'Metrik': [
                    'Schedule Performance Index (SPI)',
                    'Cost Performance Index (CPI)', 
                    'Resource Utilization Rate',
                    'Risk Mitigation Score',
                    'Quality Index',
                    'Safety Index'
                ],
                'Nilai': [
                    np.random.uniform(0.95, 1.05),
                    np.random.uniform(0.9, 1.1),
                    np.mean([v['utilized']/v['available'] for v in results['resource_utilization'].values() if v['available'] > 0]),
                    1 - (sum(1 for r in results['risks'] if r['risk_level'] == 'High') / len(results['risks'])),
                    np.random.uniform(0.85, 0.95),
                    np.random.uniform(0.9, 1.0)
                ],
                'Target': [1.0, 1.0, 0.85, 0.8, 0.9, 0.95],
                'Status': []
            }
            
            for i, (nilai, target) in enumerate(zip(kpi_data['Nilai'], kpi_data['Target'])):
                kpi_data['Status'].append('✅ Tercapai' if nilai >= target else '❌ Perlu Perbaikan')
            
            kpi_df = pd.DataFrame(kpi_data)
            kpi_df['Nilai'] = kpi_df['Nilai'].apply(lambda x: f"{x:.3f}")
            
            def color_kpi(val):
                return 'color: green; font-weight: bold' if val == '✅ Tercapai' else 'color: red; font-weight: bold'
            
            st.dataframe(
                kpi_df.style.applymap(color_kpi, subset=['Status']),
                use_container_width=True,
                hide_index=True
            )
            
            st.markdown("### 📈 Tren KPI")
            
            kpi_trend_data = pd.DataFrame({
                'Bulan': [f'Bulan {i}' for i in range(1, 13)],
                'SPI': np.random.normal(1.0, 0.05, 12).cumprod(),
                'CPI': np.random.normal(1.0, 0.07, 12).cumprod(),
                'Quality': np.random.normal(0.9, 0.03, 12),
                'Safety': np.random.normal(0.95, 0.02, 12)
            })
            
            fig_kpi = px.line(
                kpi_trend_data,
                x='Bulan',
                y=['SPI', 'CPI', 'Quality', 'Safety'],
                title='Tren KPI Bulanan',
                markers=True,
                template='plotly_white'
            )
            fig_kpi.update_layout(
                yaxis_title="Nilai KPI",
                hovermode="x unified"
            )
            
            fig_kpi.add_hline(y=1.0, line_dash="dot", line_color="red", annotation_text="Target SPI/CPI")
            fig_kpi.add_hline(y=0.9, line_dash="dot", line_color="blue", annotation_text="Target Quality")
            fig_kpi.add_hline(y=0.95, line_dash="dot", line_color="green", annotation_text="Target Safety")
            
            st.plotly_chart(fig_kpi, use_container_width=True)
    
    else:
        st.info("👈 Silakan atur parameter proyek di sidebar dan klik 'Jalankan Simulasi' untuk memulai.")
        
        st.markdown("### 📋 Data Sampel Proyek Historis")
        historical_df = st.session_state.data_manager.historical_data.head(10).copy()
        historical_df['duration_days'] = historical_df['duration_days'].astype(int)
        historical_df['cost_million'] = historical_df['cost_million'].apply(lambda x: f"${x:.1f}M")
        historical_df['tunnel_length_km'] = historical_df['tunnel_length_km'].apply(lambda x: f"{x:.1f} km")
        historical_df['soil_difficulty'] = historical_df['soil_difficulty'].apply(lambda x: f"{x:.2f}")
        historical_df['tunnel_depth'] = historical_df['tunnel_depth'].apply(lambda x: f"{x:.1f} m")
        st.dataframe(historical_df, use_container_width=True)
        
        st.markdown("### 🏗️ Data Geoteknik Sampel")
        geotech_df = pd.DataFrame(st.session_state.data_manager.geotechnical_data).head(10).copy()
        geotech_df['water_level'] = geotech_df['water_level'].apply(lambda x: f"{x:.1f} m")
        geotech_df['risk_factor'] = geotech_df['risk_factor'].apply(lambda x: f"{x:.2f}")
        st.dataframe(geotech_df, use_container_width=True)

if __name__ == "__main__":
    main()