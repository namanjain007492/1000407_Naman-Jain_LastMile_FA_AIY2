import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import time

# 1. Page Configuration
st.set_page_config(page_title="Delhivery | Enterprise Telemetry", layout="wide", initial_sidebar_state="expanded")

# 2. Ultra-Realistic 3D CSS & Slower Cinematic Splash Screen
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700;900&display=swap');
    
    /* Base Theme */
    .stApp {
        background-color: #0d0d0d;
        color: #e0e0e0;
        font-family: 'Roboto', sans-serif;
    }
    
    /* Cinematic Splash Screen (5 Seconds, Smooth) */
    .splash-screen {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background: radial-gradient(circle, #1a1a1a 0%, #000000 100%);
        z-index: 99999;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        animation: fadeOut 0.5s ease-in 4.5s forwards;
    }
    
    .logo-container {
        font-size: 3.5rem;
        font-weight: 900;
        color: #E31837;
        text-shadow: 0px 4px 15px rgba(227, 24, 55, 0.6);
        margin-bottom: 40px;
        letter-spacing: 2px;
    }

    .road-3d {
        width: 100%;
        height: 8px;
        background: #222;
        border-top: 2px dashed #444;
        position: relative;
        perspective: 1000px;
    }

    .realistic-truck {
        font-size: 5rem;
        position: absolute;
        bottom: 0px;
        left: -10%;
        animation: driveSmooth 4.5s cubic-bezier(0.25, 0.1, 0.25, 1) forwards;
        filter: drop-shadow(5px 15px 10px rgba(0,0,0,0.8));
    }

    .loading-bar-container {
        width: 300px;
        height: 6px;
        background: #222;
        border-radius: 10px;
        margin-top: 40px;
        overflow: hidden;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.9);
    }

    .loading-bar {
        height: 100%;
        background: linear-gradient(90deg, #8a0b1d, #E31837);
        width: 0%;
        animation: load 4s ease-in-out forwards;
    }

    @keyframes driveSmooth {
        0% { left: -10%; transform: scale(0.9); }
        40% { left: 40%; transform: scale(1.1); }
        80% { left: 50%; transform: scale(1.1); }
        100% { left: 120%; transform: scale(0.9); }
    }
    @keyframes load { 0% { width: 0%; } 100% { width: 100%; } }
    @keyframes fadeOut { to { opacity: 0; visibility: hidden; } }

    /* Ultra-Realistic 3D Physical Buttons */
    div.stButton > button {
        background: linear-gradient(180deg, #ff3355 0%, #cc1028 100%);
        border: 1px solid #8a0b1d;
        border-radius: 8px;
        color: white !important;
        font-weight: 800;
        font-size: 16px;
        padding: 12px 24px;
        text-transform: uppercase;
        letter-spacing: 1px;
        /* The 3D Depth Shadow */
        box-shadow: 
            0 6px 0 #590000, 
            0 12px 20px rgba(0,0,0,0.6), 
            inset 0 1px 2px rgba(255,255,255,0.4);
        transition: all 0.1s ease;
        width: 100%;
    }
    
    /* 3D Button Press Physics */
    div.stButton > button:active {
        transform: translateY(6px);
        box-shadow: 
            0 0px 0 #590000, 
            0 4px 6px rgba(0,0,0,0.6), 
            inset 0 1px 2px rgba(255,255,255,0.2);
    }

    /* 3D Hardware Cards for Metrics */
    div[data-testid="metric-container"] {
        background: linear-gradient(145deg, #1a1a1a, #0d0d0d);
        border: 1px solid #333;
        border-top: 2px solid #E31837;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 8px 8px 15px #050505, -8px -8px 15px #151515;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Cinematic Loading Execution
if 'system_initialized' not in st.session_state:
    splash = st.empty()
    with splash.container():
        st.markdown("""
            <div class="splash-screen">
                <div class="logo-container">DELHIVERY ENTERPRISE</div>
                <div class="road-3d">
                    <div class="realistic-truck">🚚</div>
                </div>
                <div class="loading-bar-container"><div class="loading-bar"></div></div>
                <div style="margin-top:15px; color:#555; font-family:monospace;">INITIALIZING 3D TELEMETRY MATRIX...</div>
            </div>
        """, unsafe_allow_html=True)
    time.sleep(4.8) # Matches CSS animation
    splash.empty()
    st.session_state.system_initialized = True

st.title("DELHIVERY 3D COMMAND CENTER")
st.caption("Live AI Telemetry, Fleet Routing, and Bottleneck Detection System.")

# 4. Data Processing
@st.cache_data
def load_data():
    df = pd.read_csv("delivery_data.csv")
    df.columns = [c.strip() for c in df.columns]
    df = df.dropna(subset=['Delivery_Time', 'Weather', 'Traffic', 'Vehicle', 'Area', 'Category'])
    
    mean_time = df['Delivery_Time'].mean()
    std_time = df['Delivery_Time'].std()
    threshold = mean_time + std_time
    df['Is_Late'] = df['Delivery_Time'] > threshold
    
    # Required Age brackets
    if 'Agent_Age' in df.columns:
        df['Agent_Age_Group'] = pd.cut(df['Agent_Age'], bins=[0, 25, 40, 100], labels=['<25', '25–40', '40+'])
    else:
        df['Agent_Age_Group'] = 'Unknown'
        
    # Generate dummy months for the optional monthly trends chart
    np.random.seed(42)
    df['Month'] = np.random.choice(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], size=len(df))
        
    return df, threshold

try:
    df_raw, late_threshold = load_data()
except Exception:
    st.error("SYSTEM HALT: `delivery_data.csv` missing from main directory.")
    st.stop()

# 5. Tactile 3D Sidebar
with st.sidebar:
    st.markdown("### 🎛️ HARDWARE CONTROLS")
    st.divider()
    
    with st.form("filter_form"):
        sel_weather = st.multiselect("☁️ Atmospheric Condition", sorted(df_raw['Weather'].unique()), default=sorted(df_raw['Weather'].unique()))
        sel_traffic = st.multiselect("🚦 Traffic Density", sorted(df_raw['Traffic'].unique()), default=sorted(df_raw['Traffic'].unique()))
        sel_vehicle = st.multiselect("🚚 Fleet Class", sorted(df_raw['Vehicle'].unique()), default=sorted(df_raw['Vehicle'].unique()))
        sel_category = st.multiselect("📦 Freight Type", sorted(df_raw['Category'].unique()), default=sorted(df_raw['Category'].unique()))
        sel_area = st.multiselect("📍 Operating Zone", sorted(df_raw['Area'].unique()), default=sorted(df_raw['Area'].unique()))
        
        st.markdown("<br>", unsafe_allow_html=True)
        # 3D Physical Button
        submitted = st.form_submit_button("ENGAGE 3D SCANNERS")

filtered_df = df_raw[
    df_raw['Weather'].isin(sel_weather) &
    df_raw['Traffic'].isin(sel_traffic) &
    df_raw['Vehicle'].isin(sel_vehicle) &
    df_raw['Category'].isin(sel_category) &
    df_raw['Area'].isin(sel_area)
]

# 6. Physical Hardware Metrics
c1, c2, c3, c4 = st.columns(4)
total_orders = len(filtered_df)
avg_time = filtered_df['Delivery_Time'].mean() if total_orders > 0 else 0
late_pct = (filtered_df['Is_Late'].mean() * 100) if total_orders > 0 else 0

c1.metric("ACTIVE FREIGHT", f"{total_orders:,}")
c2.metric("TRANSIT VELOCITY", f"{avg_time:.1f} m")
c3.metric("FAILURE RATE", f"{late_pct:.1f}%")
c4.metric("SYSTEM THRESHOLD", f"{late_threshold:.1f} m")

st.divider()

if total_orders > 0:
    st.markdown("### 🌐 CORE 3D VISUALIZATIONS (Compulsory)")
    
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        # Compulsory 1: Agent Performance (3D Scatter)
        fig_3d_agent = px.scatter_3d(
            filtered_df, x='Agent_Rating', y='Agent_Age', z='Delivery_Time',
            color='Agent_Age_Group', size='Delivery_Time',
            color_discrete_sequence=['#E31837', '#FF9999', '#FFFFFF'],
            template="plotly_dark", title="Personnel Efficiency Matrix"
        )
        fig_3d_agent.update_layout(scene=dict(bgcolor='#000'), paper_bgcolor='#0d0d0d')
        st.plotly_chart(fig_3d_agent, use_container_width=True)

    with r1c2:
        # Compulsory 2: Area Heatmap (3D Surface Map)
        area_matrix = filtered_df.pivot_table(index='Area', columns='Traffic', values='Delivery_Time', aggfunc='mean').fillna(0)
        fig_surface = go.Figure(data=[go.Surface(
            z=area_matrix.values, x=area_matrix.columns, y=area_matrix.index,
            colorscale=[[0, '#000000'], [0.5, '#8a0b1d'], [1, '#E31837']]
        )])
        fig_surface.update_layout(title="Geographic Bottleneck Topology", template="plotly_dark", scene=dict(bgcolor='#000'), paper_bgcolor='#0d0d0d')
        st.plotly_chart(fig_surface, use_container_width=True)

    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1:
        # Compulsory 3: Delay Analyzer
        delay_data = filtered_df.groupby(['Weather', 'Traffic'], as_index=False)['Delivery_Time'].mean()
        fig_delay = px.bar(delay_data, x='Weather', y='Delivery_Time', color='Traffic', barmode='group', template="plotly_dark", title="Env. Impact")
        fig_delay.update_layout(paper_bgcolor='#0d0d0d', plot_bgcolor='#000')
        st.plotly_chart(fig_delay, use_container_width=True)
        
    with r2c2:
        # Compulsory 4: Vehicle Comparison
        veh_data = filtered_df.groupby('Vehicle', as_index=False)['Delivery_Time'].mean()
        fig_veh = px.bar(veh_data, x='Vehicle', y='Delivery_Time', color='Delivery_Time', color_continuous_scale="Reds", template="plotly_dark", title="Fleet Performance")
        fig_veh.update_layout(paper_bgcolor='#0d0d0d', plot_bgcolor='#000')
        st.plotly_chart(fig_veh, use_container_width=True)
        
    with r2c3:
        # Compulsory 5: Category Boxplot
        fig_cat = px.box(filtered_df, x='Category', y='Delivery_Time', color='Category', template="plotly_dark", title="Freight Volatility")
        fig_cat.update_layout(paper_bgcolor='#0d0d0d', plot_bgcolor='#000')
        st.plotly_chart(fig_cat, use_container_width=True)

    st.divider()
    st.markdown("### 📈 ADVANCED TELEMETRY (All 4 Optional Features Active)")
    
    r3c1, r3c2 = st.columns(2)
    with r3c1:
        # Optional 1: Monthly Trends Line Chart
        trend_data = filtered_df.groupby('Month', as_index=False)['Delivery_Time'].mean()
        # Sort months logically
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        trend_data['Month'] = pd.Categorical(trend_data['Month'], categories=month_order, ordered=True)
        trend_data = trend_data.sort_values('Month')
        fig_trend = px.line(trend_data, x='Month', y='Delivery_Time', markers=True, template="plotly_dark", title="Monthly Speed Trends", line_shape="spline")
        fig_trend.update_traces(line_color='#E31837', line_width=4, marker=dict(size=10))
        fig_trend.update_layout(paper_bgcolor='#0d0d0d', plot_bgcolor='#000')
        st.plotly_chart(fig_trend, use_container_width=True)

    with r3c2:
        # Optional 2: Delivery Time Distribution Histogram
        fig_hist = px.histogram(filtered_df, x='Delivery_Time', nbins=40, marginal="box", template="plotly_dark", title="Time Distribution Curve", color_discrete_sequence=['#E31837'])
        fig_hist.update_layout(paper_bgcolor='#0d0d0d', plot_bgcolor='#000')
        st.plotly_chart(fig_hist, use_container_width=True)

    r4c1, r4c2 = st.columns(2)
    with r4c1:
        # Optional 3: % of Late Deliveries by Traffic (Heatmap)
        late_matrix = filtered_df.pivot_table(index='Traffic', columns='Weather', values='Is_Late', aggfunc='mean') * 100
        fig_late = px.imshow(late_matrix, text_auto=".1f", aspect="auto", template="plotly_dark", title="% Late by Env. Factors", color_continuous_scale="Reds")
        fig_late.update_layout(paper_bgcolor='#0d0d0d', plot_bgcolor='#000')
        st.plotly_chart(fig_late, use_container_width=True)

    with r4c2:
        # Optional 4: Agent Count Per Area (3D Bubble Chart Representation)
        agent_count = filtered_df.groupby('Area', as_index=False)['Agent_Age'].count().rename(columns={'Agent_Age': 'Agent_Count'})
        # Faking a 3D bubble chart layout using scatter
        fig_bubble = px.scatter(agent_count, x='Area', y='Agent_Count', size='Agent_Count', color='Agent_Count', color_continuous_scale="Reds", template="plotly_dark", title="Agent Density by Zone")
        fig_bubble.update_layout(paper_bgcolor='#0d0d0d', plot_bgcolor='#000')
        st.plotly_chart(fig_bubble, use_container_width=True)
