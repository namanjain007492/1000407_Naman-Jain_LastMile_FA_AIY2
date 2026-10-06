import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# 1. Page Configuration
st.set_page_config(page_title="Delhivery Pro Telemetry", layout="wide", initial_sidebar_state="expanded")

# 2. Advanced CSS: Delhivery Corporate Theme & Splash Animation
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    /* Global Theme */
    .stApp {
        background-color: #0A0A0A; /* Deep Onyx */
        color: #F5F5F5;
        font-family: 'Inter', sans-serif;
    }
    
    /* Splash Screen Animation */
    .splash-screen {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: #0A0A0A;
        z-index: 99999;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        overflow: hidden;
    }
    
    .road {
        width: 100%;
        height: 4px;
        background: repeating-linear-gradient(90deg, #333 0, #333 20px, transparent 20px, transparent 40px);
        position: absolute;
        bottom: 40%;
    }

    .truck {
        font-size: 6rem;
        position: absolute;
        bottom: 41%;
        left: -20%;
        animation: drive 2.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
        filter: drop-shadow(0 10px 10px rgba(227, 24, 55, 0.3));
    }
    
    .delhivery-logo {
        font-size: 4rem;
        font-weight: 900;
        color: #E31837; /* Delhivery Red */
        letter-spacing: -2px;
        text-transform: uppercase;
        position: absolute;
        bottom: 55%;
        left: -20%;
        animation: drive 2.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }

    @keyframes drive {
        0% { left: -20%; transform: scale(1); }
        50% { left: 45%; transform: scale(1.1); }
        100% { left: 120%; transform: scale(1); }
    }

    /* Professional Elevated Cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(145deg, #121212, #181818);
        border-left: 4px solid #E31837;
        border-radius: 6px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        transition: transform 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        border-left: 4px solid #FF2A4D;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #121212;
        border-right: 1px solid #333;
    }
    .sidebar-header {
        color: #E31837;
        font-weight: 900;
        font-size: 1.5rem;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Cinematic Splash Screen Execution
if 'booted' not in st.session_state:
    splash = st.empty()
    with splash.container():
        st.markdown("""
            <div class="splash-screen">
                <div class="delhivery-logo">DELHIVERY // OS</div>
                <div class="truck">🚛</div>
                <div class="road"></div>
            </div>
        """, unsafe_allow_html=True)
    time.sleep(2.5) # Wait for animation to finish
    splash.empty()
    st.session_state.booted = True

# Main App Header
st.markdown("<h1 style='color: #E31837; font-weight: 900; letter-spacing:-1px;'>DELHIVERY <span style='color: #FFF;'>TELEMETRY</span></h1>", unsafe_allow_html=True)
st.caption("Enterprise logistics tracking and 3D data visualization matrix.")

# 4. Data Loading (Stage 4)
@st.cache_data
def load_data():
    df = pd.read_csv("delivery_data.csv")
    df.columns = [c.strip() for c in df.columns]
    df = df.dropna(subset=['Delivery_Time', 'Weather', 'Traffic', 'Vehicle', 'Area', 'Category'])
    
    mean_time = df['Delivery_Time'].mean()
    std_time = df['Delivery_Time'].std()
    threshold = mean_time + std_time
    df['Is_Late'] = df['Delivery_Time'] > threshold
    
    if 'Agent_Age' in df.columns:
        df['Agent_Age_Group'] = pd.cut(df['Agent_Age'], bins=[0, 25, 40, 100], labels=['<25', '25–40', '40+'])
    else:
        df['Agent_Age_Group'] = 'Unknown'
        
    return df, threshold

try:
    df_raw, late_threshold = load_data()
except Exception:
    st.error("Data missing. Ensure delivery_data.csv is uploaded.")
    st.stop()

# 5. Professional Sidebar UI
with st.sidebar:
    st.markdown('<div class="sidebar-header">⚙️ OPERATION PARAMETERS</div>', unsafe_allow_html=True)
    
    # Using expanders for a clean, non-cluttered professional UI
    with st.expander("🌍 Environmental Factors", expanded=True):
        sel_weather = st.multiselect("Weather Conditions", sorted(df_raw['Weather'].unique()), default=sorted(df_raw['Weather'].unique()))
        sel_traffic = st.multiselect("Traffic Density", sorted(df_raw['Traffic'].unique()), default=sorted(df_raw['Traffic'].unique()))
        
    with st.expander("🚚 Asset & Logistics", expanded=True):
        sel_vehicle = st.multiselect("Fleet Vehicles", sorted(df_raw['Vehicle'].unique()), default=sorted(df_raw['Vehicle'].unique()))
        sel_category = st.multiselect("Freight Category", sorted(df_raw['Category'].unique()), default=sorted(df_raw['Category'].unique()))
        
    with st.expander("📍 Geographic Routing", expanded=False):
        sel_area = st.multiselect("Operating Zones", sorted(df_raw['Area'].unique()), default=sorted(df_raw['Area'].unique()))

filtered_df = df_raw[
    df_raw['Weather'].isin(sel_weather) &
    df_raw['Traffic'].isin(sel_traffic) &
    df_raw['Vehicle'].isin(sel_vehicle) &
    df_raw['Category'].isin(sel_category) &
    df_raw['Area'].isin(sel_area)
]

# 6. Core KPIs
col1, col2, col3, col4 = st.columns(4)
t_orders = len(filtered_df)
a_time = filtered_df['Delivery_Time'].mean() if t_orders > 0 else 0
l_pct = (filtered_df['Is_Late'].mean() * 100) if t_orders > 0 else 0

col1.metric("Active Shipments", f"{t_orders:,}")
col2.metric("Avg Transit (Min)", f"{a_time:.1f}")
col3.metric("Critical Delay Ratio", f"{l_pct:.1f}%")
col4.metric("Failure Threshold", f"{late_threshold:.1f}m")

st.divider()

if t_orders > 0:
    # 7. Enhanced 3D Visualizations & Bonus Features (Stage 5)
    
    st.markdown("### 🌐 3D Performance Matrix")
    c1, c2 = st.columns(2)
    
    with c1:
        # Visual 1: 3D Agent Scatter (Required)
        fig_3d = px.scatter_3d(
            filtered_df, x='Agent_Rating', y='Agent_Age', z='Delivery_Time',
            color='Agent_Age_Group', size='Delivery_Time',
            color_discrete_sequence=['#E31837', '#FFF', '#555'],
            template="plotly_dark", title="Personnel Efficiency (3D Axis)"
        )
        fig_3d.update_layout(scene=dict(bgcolor='#0A0A0A'), margin=dict(l=0, r=0, b=0, t=30), paper_bgcolor='#0A0A0A')
        st.plotly_chart(fig_3d, use_container_width=True)

    with c2:
        # Visual 2: 3D Area Heatmap (Required)
        area_matrix = filtered_df.pivot_table(index='Area', columns='Traffic', values='Delivery_Time', aggfunc='mean').fillna(0)
        fig_surface = go.Figure(data=[go.Surface(
            z=area_matrix.values, x=area_matrix.columns, y=area_matrix.index,
            colorscale=[[0, '#0A0A0A'], [0.5, '#E31837'], [1, '#FFFFFF']] # Custom Delhivery color scale
        )])
        fig_surface.update_layout(title="Geographic Bottleneck Surface", template="plotly_dark", scene=dict(bgcolor='#0A0A0A'), margin=dict(l=0, r=0, b=0, t=30), paper_bgcolor='#0A0A0A')
        st.plotly_chart(fig_surface, use_container_width=True)

    st.markdown("### 📊 Operational Telemetry")
    c3, c4 = st.columns(2)
    
    with c3:
        # Visual 3: Weather/Traffic Impact (Required)
        delay_data = filtered_df.groupby(['Weather', 'Traffic'], as_index=False)['Delivery_Time'].mean()
        fig_delay = px.bar(delay_data, x='Weather', y='Delivery_Time', color='Traffic', barmode='group', template="plotly_dark", title="Environmental Impact")
        fig_delay.update_layout(plot_bgcolor='#0A0A0A', paper_bgcolor='#0A0A0A')
        st.plotly_chart(fig_delay, use_container_width=True)

    with c4:
        # Visual 4: Vehicle Breakdown (Required)
        veh_data = filtered_df.groupby('Vehicle', as_index=False)['Delivery_Time'].mean()
        fig_veh = px.bar(veh_data, x='Vehicle', y='Delivery_Time', color='Delivery_Time', color_continuous_scale="Reds", template="plotly_dark", title="Fleet Performance")
        fig_veh.update_layout(plot_bgcolor='#0A0A0A', paper_bgcolor='#0A0A0A')
        st.plotly_chart(fig_veh, use_container_width=True)

    c5, c6 = st.columns(2)
    
    with c5:
        # Visual 5: Category Boxplot (Required)
        fig_cat = px.box(filtered_df, x='Category', y='Delivery_Time', color='Category', template="plotly_dark", title="Freight Category Volatility")
        fig_cat.update_layout(plot_bgcolor='#0A0A0A', paper_bgcolor='#0A0A0A')
        st.plotly_chart(fig_cat, use_container_width=True)
        
    with c6:
        # Visual 6: Delivery Time Distribution (Optional Extra Feature from Rubric)
        fig_hist = px.histogram(filtered_df, x='Delivery_Time', nbins=30, template="plotly_dark", title="Global Delivery Time Distribution", color_discrete_sequence=['#E31837'])
        fig_hist.update_layout(plot_bgcolor='#0A0A0A', paper_bgcolor='#0A0A0A')
        st.plotly_chart(fig_hist, use_container_width=True)
