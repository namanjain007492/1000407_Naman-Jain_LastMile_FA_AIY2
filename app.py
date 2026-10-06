import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# 1. Page Config & Amazon-Style 3D UI
st.set_page_config(page_title="Prime Logistics 3D OS", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* Amazon Professional Dark Theme */
    .stApp {
        background-color: #131A22; /* Amazon Navy */
        color: #FFFFFF;
        font-family: 'Amazon Ember', 'Arial', sans-serif;
    }
    
    /* 3D Extruded Logo Text */
    .logo-3d {
        font-size: 3.5rem;
        font-weight: 900;
        color: #FF9900; /* Amazon Orange */
        text-align: center;
        letter-spacing: -1px;
        text-shadow: 
            0 1px 0 #cc7a00, 
            0 2px 0 #b36b00, 
            0 3px 0 #995c00, 
            0 4px 0 #804d00, 
            0 5px 10px rgba(0,0,0,0.5), 
            0 10px 20px rgba(0,0,0,0.4);
        margin-bottom: 5px;
    }

    /* 3D Elevated Metric Cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(145deg, #1f2a36, #1a232d);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #232f3e;
        box-shadow: 5px 5px 15px #0a0e12, -5px -5px 15px #1c2632;
        transition: all 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 8px 8px 20px #080b0f, -8px -8px 20px #1e2935;
        border: 1px solid #FF9900;
    }

    /* 3D Tactile "Pressable" Amazon Buttons */
    div.stButton > button {
        background: linear-gradient(to bottom, #f8e3ad, #EEAF00);
        border: 1px solid #a88734;
        border-radius: 8px;
        box-shadow: 0 5px 0 #b38404, 0 6px 15px rgba(0,0,0,0.4);
        color: #111111 !important;
        font-weight: 800;
        font-size: 16px;
        text-transform: uppercase;
        transition: all 0.1s ease-in-out;
        width: 100%;
    }
    
    /* Button Press Animation */
    div.stButton > button:active {
        transform: translateY(5px);
        box-shadow: 0 0 0 #b38404, 0 2px 5px rgba(0,0,0,0.4);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #232F3E; /* Amazon Header Blue */
        border-right: 2px solid #FF9900;
    }
    </style>
""", unsafe_allow_html=True)

# Gamified Startup
if "system_ready" not in st.session_state:
    with st.spinner('Booting Logistics 3D Engine...'):
        time.sleep(1)
    st.session_state.system_ready = True

# 3D Logo Header
st.markdown('<p class="logo-3d">AMZ: LogiSight 3D</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#879596; font-size:1.2rem; margin-bottom:30px;'>Professional Last-Mile Telemetry & Routing Systems</p>", unsafe_allow_html=True)

# 2. Data Logic (Stage 4)
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
except Exception as e:
    st.error("Error loading delivery_data.csv. Ensure it is not empty and is a valid CSV.")
    st.stop()

# 3. 3D Sidebar Controls (Stage 6)
with st.sidebar:
    st.markdown("### 🎛️ SYSTEM CONTROLS")
    
    with st.form("filter_form"):
        sel_weather = st.multiselect("☁️ Weather", sorted(df_raw['Weather'].unique()), default=sorted(df_raw['Weather'].unique()))
        sel_traffic = st.multiselect("🚦 Traffic Level", sorted(df_raw['Traffic'].unique()), default=sorted(df_raw['Traffic'].unique()))
        sel_vehicle = st.multiselect("🚚 Fleet Type", sorted(df_raw['Vehicle'].unique()), default=sorted(df_raw['Vehicle'].unique()))
        sel_category = st.multiselect("📦 Package Category", sorted(df_raw['Category'].unique()), default=sorted(df_raw['Category'].unique()))
        sel_area = st.multiselect("📍 Delivery Zone", sorted(df_raw['Area'].unique()), default=sorted(df_raw['Area'].unique()))
        
        # This button will use the custom 3D CSS injected above
        submitted = st.form_submit_button("EXECUTE 3D SCAN")

filtered_df = df_raw[
    df_raw['Weather'].isin(sel_weather) &
    df_raw['Traffic'].isin(sel_traffic) &
    df_raw['Vehicle'].isin(sel_vehicle) &
    df_raw['Category'].isin(sel_category) &
    df_raw['Area'].isin(sel_area)
]

# 4. KPI Array (Floating Cards)
col1, col2, col3, col4 = st.columns(4)
total_orders = len(filtered_df)
avg_time = filtered_df['Delivery_Time'].mean() if total_orders > 0 else 0
late_pct = (filtered_df['Is_Late'].mean() * 100) if total_orders > 0 else 0

col1.metric("📦 Active Parcels", f"{total_orders:,}")
col2.metric("⏱️ Average Transit", f"{avg_time:.1f} min")
col3.metric("⚠️ Delay Ratio", f"{late_pct:.1f}%")
col4.metric("🛑 AI Threshold (μ+1σ)", f"{late_threshold:.1f} min")

st.divider()

if total_orders > 0:
    st.markdown("### 🌐 3D Operations Center")
    r1c1, r1c2 = st.columns(2)
    
    with r1c1:
        # Visual 3: 3D Agent Matrix (Stage 5)
        st.caption("TACTICAL VIEW: Rotate to map Agent Speed against Rating & Age")
        fig_3d = px.scatter_3d(
            filtered_df, x='Agent_Rating', y='Agent_Age', z='Delivery_Time',
            color='Agent_Age_Group', size='Delivery_Time',
            color_discrete_sequence=['#FF9900', '#00A8E1', '#FFFFFF'],
            template="plotly_dark", opacity=0.9
        )
        fig_3d.update_layout(scene=dict(bgcolor='#131A22'), margin=dict(l=0, r=0, b=0, t=0), paper_bgcolor='#131A22')
        st.plotly_chart(fig_3d, use_container_width=True)

    with r1c2:
        # Visual 4: 3D Area Heatmap Surface (Stage 5)
        st.caption("TOPOGRAPHICAL VIEW: Delivery zone delay spikes by traffic")
        area_matrix = filtered_df.pivot_table(index='Area', columns='Traffic', values='Delivery_Time', aggfunc='mean').fillna(0)
        fig_surface = go.Figure(data=[go.Surface(
            z=area_matrix.values,
            x=area_matrix.columns,
            y=area_matrix.index,
            colorscale='YlOrRd' # Yellow-Orange-Red (Amazon heat colors)
        )])
        fig_surface.update_layout(template="plotly_dark", scene=dict(bgcolor='#131A22'), margin=dict(l=0, r=0, b=0, t=0), paper_bgcolor='#131A22')
        st.plotly_chart(fig_surface, use_container_width=True)

    st.markdown("### 📊 Standard Telemetry")
    r2c1, r2c2 = st.columns(2)
    
    with r2c1:
        # Visual 1: Delay Analyzer (Stage 5)
        delay_data = filtered_df.groupby(['Weather', 'Traffic'], as_index=False)['Delivery_Time'].mean()
        fig_delay = px.bar(
            delay_data, x='Weather', y='Delivery_Time', color='Traffic', 
            barmode='group', template="plotly_dark", title="Weather & Traffic Impact",
            color_discrete_sequence=['#FF9900', '#00A8E1', '#879596']
        )
        fig_delay.update_layout(plot_bgcolor='#131A22', paper_bgcolor='#131A22')
        st.plotly_chart(fig_delay, use_container_width=True)

    with r2c2:
        # Visual 2: Fleet Comparison (Stage 5)
        veh_data = filtered_df.groupby('Vehicle', as_index=False)['Delivery_Time'].mean().sort_values(by='Delivery_Time')
        fig_veh = px.bar(
            veh_data, x='Vehicle', y='Delivery_Time', color='Delivery_Time', 
            color_continuous_scale="Oranges", template="plotly_dark", title="Fleet Efficiency"
        )
        fig_veh.update_layout(plot_bgcolor='#131A22', paper_bgcolor='#131A22')
        st.plotly_chart(fig_veh, use_container_width=True)

    # Visual 5: Category Boxplot (Stage 5)
    fig_cat = px.box(
        filtered_df, x='Category', y='Delivery_Time', color='Category', 
        template="plotly_dark", title="Package Category Volatility"
    )
    fig_cat.update_layout(plot_bgcolor='#131A22', paper_bgcolor='#131A22')
    st.plotly_chart(fig_cat, use_container_width=True)
else:
    st.warning("SYSTEM ALERT: No routes match current filters. Adjust parameters to scan.")
