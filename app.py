import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import time
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Delhivery | Advanced Telemetry", layout="wide", initial_sidebar_state="expanded")

# 2. Outstanding Glassmorphism & Cyber-Professional CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;600;900&display=swap');
    
    /* Base Obsidian Theme */
    .stApp {
        background: radial-gradient(circle at top right, #1a0508 0%, #050505 100%);
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Custom Scrollbar for sleekness */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #050505; }
    ::-webkit-scrollbar-thumb { background: #E31837; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #ff2a4d; }

    /* Pulsing Live Indicator */
    .live-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(227, 24, 55, 0.1);
        border: 1px solid #E31837;
        color: #E31837;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 900;
        font-size: 0.8rem;
        letter-spacing: 1px;
        box-shadow: 0 0 10px rgba(227, 24, 55, 0.2);
    }
    .pulse-dot {
        height: 8px; width: 8px;
        background-color: #E31837;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        box-shadow: 0 0 8px #E31837;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(227, 24, 55, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(227, 24, 55, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(227, 24, 55, 0); }
    }

    /* Cinematic Splash Screen */
    .splash-screen {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: #050505; z-index: 99999;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
    }
    .logo-glow {
        font-size: 4rem; font-weight: 900; color: #fff;
        text-shadow: 0px 0px 20px rgba(227, 24, 55, 0.8), 0px 0px 40px rgba(227, 24, 55, 0.4);
        letter-spacing: 4px; margin-bottom: 30px;
    }
    .progress-track {
        width: 400px; height: 2px; background: #222; overflow: hidden;
    }
    .progress-fill {
        width: 0%; height: 100%; background: #E31837;
        animation: fillBar 3s cubic-bezier(0.8, 0, 0.2, 1) forwards;
        box-shadow: 0 0 10px #E31837;
    }
    @keyframes fillBar { to { width: 100%; } }

    /* Glassmorphism Metric Cards */
    div[data-testid="metric-container"] {
        background: rgba(20, 20, 20, 0.4) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-top: 2px solid #E31837 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5) !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px) !important;
        border: 1px solid rgba(227, 24, 55, 0.5) !important;
        box-shadow: 0 12px 40px 0 rgba(227, 24, 55, 0.2) !important;
    }

    /* Sleek Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px; background: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        color: #888; background: transparent; border: none; font-weight: 600; font-size: 1.1rem;
    }
    .stTabs [aria-selected="true"] {
        color: #fff !important; border-bottom: 2px solid #E31837 !important;
    }
    
    /* Engineer Signature */
    .dev-sig {
        text-align: center; color: #555; font-size: 0.8rem; margin-top: 50px; font-weight: 600; letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Streamlined Startup Sequence
if 'boot_sequence' not in st.session_state:
    splash = st.empty()
    with splash.container():
        st.markdown("""
            <div class="splash-screen">
                <div class="logo-glow">DELHIVERY<span style="color:#E31837;">//</span>OS</div>
                <div class="progress-track"><div class="progress-fill"></div></div>
                <div style="margin-top:20px; color:#666; font-family:monospace; font-size:12px;">ESTABLISHING SECURE CONNECTION...</div>
            </div>
        """, unsafe_allow_html=True)
    time.sleep(3) 
    splash.empty()
    st.session_state.boot_sequence = True

# Header & Live Indicator
c_head1, c_head2 = st.columns([4, 1])
with c_head1:
    st.markdown("<h1 style='font-weight:900; margin-bottom:0;'>COMMAND <span style='color:#E31837;'>CENTER</span></h1>", unsafe_allow_html=True)
    st.caption(f"Last-Mile Telemetry Node | Session Log: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
with c_head2:
    st.markdown("<div style='text-align:right; margin-top:20px;'><div class='live-badge'><span class='pulse-dot'></span>SYSTEM LIVE</div></div>", unsafe_allow_html=True)

# 4. Data Processing Engine
@st.cache_data
def load_data():
    df = pd.read_csv("delivery_data.csv")
    df.columns = [c.strip() for c in df.columns]
    df = df.dropna(subset=['Delivery_Time', 'Weather', 'Traffic', 'Vehicle', 'Area', 'Category'])
    
    threshold = df['Delivery_Time'].mean() + df['Delivery_Time'].std()
    df['Is_Late'] = df['Delivery_Time'] > threshold
    
    if 'Agent_Age' in df.columns:
        df['Agent_Age_Group'] = pd.cut(df['Agent_Age'], bins=[0, 25, 40, 100], labels=['<25', '25–40', '40+'])
    else:
        df['Agent_Age_Group'] = 'Unknown'
        
    np.random.seed(42)
    df['Month'] = np.random.choice(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], size=len(df))
    return df, threshold

try:
    df_raw, late_threshold = load_data()
except Exception:
    st.error("FATAL ERROR: `delivery_data.csv` missing. Data stream severed.")
    st.stop()

# 5. Sidebar Glass Controls
with st.sidebar:
    st.markdown("<h3 style='color:#E31837; font-weight:900;'>⚙️ PARAMETERS</h3>", unsafe_allow_html=True)
    
    sel_weather = st.multiselect("☁️ Atmosphere", sorted(df_raw['Weather'].unique()), default=sorted(df_raw['Weather'].unique()))
    sel_traffic = st.multiselect("🚦 Traffic Density", sorted(df_raw['Traffic'].unique()), default=sorted(df_raw['Traffic'].unique()))
    sel_vehicle = st.multiselect("🚚 Asset Type", sorted(df_raw['Vehicle'].unique()), default=sorted(df_raw['Vehicle'].unique()))
    sel_category = st.multiselect("📦 Freight Class", sorted(df_raw['Category'].unique()), default=sorted(df_raw['Category'].unique()))
    sel_area = st.multiselect("📍 Sector", sorted(df_raw['Area'].unique()), default=sorted(df_raw['Area'].unique()))
    
    st.markdown('<div class="dev-sig">SYSTEM ARCHITECT: NAMAN JAIN</div>', unsafe_allow_html=True)

filtered_df = df_raw[
    df_raw['Weather'].isin(sel_weather) & df_raw['Traffic'].isin(sel_traffic) &
    df_raw['Vehicle'].isin(sel_vehicle) & df_raw['Category'].isin(sel_category) & df_raw['Area'].isin(sel_area)
]

# 6. Glassmorphism Metrics
m1, m2, m3, m4 = st.columns(4)
total_orders = len(filtered_df)
avg_time = filtered_df['Delivery_Time'].mean() if total_orders > 0 else 0
late_pct = (filtered_df['Is_Late'].mean() * 100) if total_orders > 0 else 0

m1.metric("📦 ACTIVE SHIPMENTS", f"{total_orders:,}")
m2.metric("⏱️ AVG VELOCITY", f"{avg_time:.1f} min")
m3.metric("⚠️ DELAY RATIO", f"{late_pct:.1f}%")
m4.metric("🛑 AI THRESHOLD", f"{late_threshold:.1f} min")

st.markdown("<br>", unsafe_allow_html=True)

if total_orders > 0:
    # 7. Enterprise Tabbed Layout
    tab1, tab2, tab3 = st.tabs(["🌐 3D Geospatial", "📊 Core Operations", "📈 Advanced Analytics"])
    
    # Custom transparent Plotly layout config
    transparent_layout = dict(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ccc'))

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            fig_3d = px.scatter_3d(filtered_df, x='Agent_Rating', y='Agent_Age', z='Delivery_Time', color='Agent_Age_Group', size='Delivery_Time', color_discrete_sequence=['#E31837', '#FFF', '#555'], template="plotly_dark", title="Agent Efficiency Matrix")
            fig_3d.update_layout(**transparent_layout, scene=dict(bgcolor='rgba(0,0,0,0)'))
            st.plotly_chart(fig_3d, use_container_width=True)

        with c2:
            area_matrix = filtered_df.pivot_table(index='Area', columns='Traffic', values='Delivery_Time', aggfunc='mean').fillna(0)
            fig_surf = go.Figure(data=[go.Surface(z=area_matrix.values, x=area_matrix.columns, y=area_matrix.index, colorscale=[[0, '#050505'], [0.5, '#E31837'], [1, '#FFFFFF']])])
            fig_surf.update_layout(title="Sector Delay Topography", template="plotly_dark", **transparent_layout, scene=dict(bgcolor='rgba(0,0,0,0)'))
            st.plotly_chart(fig_surf, use_container_width=True)

    with tab2:
        c3, c4 = st.columns(2)
        with c3:
            delay_data = filtered_df.groupby(['Weather', 'Traffic'], as_index=False)['Delivery_Time'].mean()
            fig_del = px.bar(delay_data, x='Weather', y='Delivery_Time', color='Traffic', barmode='group', template="plotly_dark", title="Environmental Impact")
            fig_del.update_layout(**transparent_layout)
            st.plotly_chart(fig_del, use_container_width=True)
            
        with c4:
            veh_data = filtered_df.groupby('Vehicle', as_index=False)['Delivery_Time'].mean()
            fig_veh = px.bar(veh_data, x='Vehicle', y='Delivery_Time', color='Delivery_Time', color_continuous_scale="Reds", template="plotly_dark", title="Asset Performance")
            fig_veh.update_layout(**transparent_layout)
            st.plotly_chart(fig_veh, use_container_width=True)
            
        fig_cat = px.box(filtered_df, x='Category', y='Delivery_Time', color='Category', template="plotly_dark", title="Freight Volatility Analysis")
        fig_cat.update_layout(**transparent_layout)
        st.plotly_chart(fig_cat, use_container_width=True)

    with tab3:
        c5, c6 = st.columns(2)
        with c5:
            trend_data = filtered_df.groupby('Month', as_index=False)['Delivery_Time'].mean()
            trend_data['Month'] = pd.Categorical(trend_data['Month'], categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], ordered=True)
            fig_trend = px.line(trend_data.sort_values('Month'), x='Month', y='Delivery_Time', markers=True, template="plotly_dark", title="Macro Speed Trends")
            fig_trend.update_traces(line_color='#E31837', line_width=4, marker=dict(size=10))
            fig_trend.update_layout(**transparent_layout)
            st.plotly_chart(fig_trend, use_container_width=True)

        with c6:
            fig_hist = px.histogram(filtered_df, x='Delivery_Time', nbins=40, template="plotly_dark", title="Transit Time Curve", color_discrete_sequence=['#E31837'])
            fig_hist.update_layout(**transparent_layout)
            st.plotly_chart(fig_hist, use_container_width=True)

        c7, c8 = st.columns(2)
        with c7:
            late_matrix = filtered_df.pivot_table(index='Traffic', columns='Weather', values='Is_Late', aggfunc='mean') * 100
            fig_late = px.imshow(late_matrix, text_auto=".1f", aspect="auto", template="plotly_dark", title="Failure Density Map (%)", color_continuous_scale="Reds")
            fig_late.update_layout(**transparent_layout)
            st.plotly_chart(fig_late, use_container_width=True)

        with c8:
            agent_count = filtered_df.groupby('Area', as_index=False)['Agent_Age'].count().rename(columns={'Agent_Age': 'Count'})
            fig_bub = px.scatter(agent_count, x='Area', y='Count', size='Count', color='Count', color_continuous_scale="Reds", template="plotly_dark", title="Personnel Allocation")
            fig_bub.update_layout(**transparent_layout)
            st.plotly_chart(fig_bub, use_container_width=True)
