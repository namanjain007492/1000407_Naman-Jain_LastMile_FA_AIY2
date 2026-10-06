import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# 1. Page Config & Gen-Z/Cyberpunk UI Setup
st.set_page_config(page_title="LogiSight 3D Matrix", layout="wide", initial_sidebar_state="expanded")

# Inject Custom 3D CSS, Glassmorphism, and Hover Effects
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&display=swap');
    
    .stApp {
        background-color: #09090b;
        color: #e4e4e7;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* Glassmorphism Metric Cards */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        border: 1px solid #ff00ff;
    }

    /* 3D Floating Action Button Styling */
    div.stButton > button {
        background: linear-gradient(45deg, #FF00FF, #00FFFF);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 30px;
        box-shadow: 0 4px 15px rgba(255, 0, 255, 0.4);
        transition: all 0.2s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0, 255, 255, 0.6);
    }
    
    /* Gradient Title */
    .hero-title {
        background: -webkit-linear-gradient(45deg, #00FFFF, #FF00FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5em;
        font-weight: 800;
        margin-bottom: -10px;
    }
    </style>
""", unsafe_allow_html=True)

# Gamified interactions
if "loaded" not in st.session_state:
    st.toast('🚀 Initializing 3D Matrix...', icon='👾')
    time.sleep(1)
    st.toast('Data connection established!', icon='⚡')
    st.session_state.loaded = True

st.markdown('<p class="hero-title">LogiSight // OS_v2</p>', unsafe_allow_html=True)
st.caption("Live Last-Mile Delivery Telemetry & 3D Bottleneck Detection.")

# 2. Data Logic (Stage 4 Requirements)
@st.cache_data
def load_data():
    df = pd.read_csv("delivery_data.csv")
    df.columns = [c.strip() for c in df.columns]
    df = df.dropna(subset=['Delivery_Time', 'Weather', 'Traffic', 'Vehicle', 'Area', 'Category'])
    
    # Calculate Late Threshold (mean + 1 std)
    mean_time = df['Delivery_Time'].mean()
    std_time = df['Delivery_Time'].std()
    threshold = mean_time + std_time
    df['Is_Late'] = df['Delivery_Time'] > threshold
    
    # Age brackets for scatter plot requirement
    if 'Agent_Age' in df.columns:
        df['Agent_Age_Group'] = pd.cut(df['Agent_Age'], bins=[0, 25, 40, 100], labels=['<25', '25–40', '40+'])
    else:
        df['Agent_Age_Group'] = 'Unknown'
        
    return df, threshold

df_raw, late_threshold = load_data()

# 3. Sidebar Interactive Controls
with st.sidebar:
    st.markdown("### 🎛️ SYSTEM CONTROLS")
    
    # Use form to delay updates until user clicks button for a snappy app feel
    with st.form("filter_form"):
        sel_weather = st.multiselect("☁️ Weather", sorted(df_raw['Weather'].unique()), default=sorted(df_raw['Weather'].unique()))
        sel_traffic = st.multiselect("🚦 Traffic", sorted(df_raw['Traffic'].unique()), default=sorted(df_raw['Traffic'].unique()))
        sel_vehicle = st.multiselect("🚚 Vehicle", sorted(df_raw['Vehicle'].unique()), default=sorted(df_raw['Vehicle'].unique()))
        sel_category = st.multiselect("📦 Category", sorted(df_raw['Category'].unique()), default=sorted(df_raw['Category'].unique()))
        sel_area = st.multiselect("📍 Area", sorted(df_raw['Area'].unique()), default=sorted(df_raw['Area'].unique()))
        
        submitted = st.form_submit_button("⚡ SYNC DATA")
        if submitted:
            st.balloons()
            st.toast("Filters applied successfully!", icon="✅")

filtered_df = df_raw[
    df_raw['Weather'].isin(sel_weather) &
    df_raw['Traffic'].isin(sel_traffic) &
    df_raw['Vehicle'].isin(sel_vehicle) &
    df_raw['Category'].isin(sel_category) &
    df_raw['Area'].isin(sel_area)
]

# 4. KPI Array
col1, col2, col3, col4 = st.columns(4)
total_orders = len(filtered_df)
avg_time = filtered_df['Delivery_Time'].mean() if total_orders > 0 else 0
late_pct = (filtered_df['Is_Late'].mean() * 100) if total_orders > 0 else 0

col1.metric("📦 Active Packages", f"{total_orders:,}")
col2.metric("⏱️ Avg Transit Time", f"{avg_time:.1f} min")
col3.metric("⚠️ Late Ratio", f"{late_pct:.1f}%")
col4.metric("🛑 System Threshold", f"{late_threshold:.1f} min")

st.divider()

if total_orders > 0:
    # 5. Interactive Tabs for cleaner UI
    tab1, tab2, tab3 = st.tabs(["🌐 3D Data Matrix", "📊 Operational Core", "📦 Freight Categories"])
    
    with tab1:
        st.markdown("### 3D Spatial Intelligence")
        t1_col1, t1_col2 = st.columns(2)
        
        with t1_col1:
            # Compulsory Visual 3: Agent Performance (Upgraded to 3D Scatter)
            with st.expander("ℹ️ About Agent Scatter", expanded=True):
                st.caption("Rotate to view Agent Rating vs. Age vs. Speed in 3-dimensional space.")
            fig_3d_scatter = px.scatter_3d(
                filtered_df, x='Agent_Rating', y='Agent_Age', z='Delivery_Time',
                color='Agent_Age_Group', size='Delivery_Time',
                color_discrete_sequence=['#00FFFF', '#FF00FF', '#00FF00'],
                template="plotly_dark", opacity=0.8
            )
            fig_3d_scatter.update_layout(scene=dict(bgcolor='#09090b'), margin=dict(l=0, r=0, b=0, t=0))
            st.plotly_chart(fig_3d_scatter, use_container_width=True)

        with t1_col2:
            # Compulsory Visual 4: Area Heatmap (Upgraded to 3D Topographical Surface)
            with st.expander("ℹ️ About Area Surface Map", expanded=True):
                st.caption("Peaks represent heavy delivery delays across geographical zones.")
            area_matrix = filtered_df.pivot_table(index='Area', columns='Traffic', values='Delivery_Time', aggfunc='mean').fillna(0)
            fig_surface = go.Figure(data=[go.Surface(
                z=area_matrix.values,
                x=area_matrix.columns,
                y=area_matrix.index,
                colorscale='Plasma'
            )])
            fig_surface.update_layout(template="plotly_dark", scene=dict(bgcolor='#09090b'), margin=dict(l=0, r=0, b=0, t=0))
            st.plotly_chart(fig_surface, use_container_width=True)

    with tab2:
        st.markdown("### Core Analytics")
        t2_col1, t2_col2 = st.columns(2)
        
        with t2_col1:
            # Compulsory Visual 1: Delay Analyzer (Bar Chart)
            delay_data = filtered_df.groupby(['Weather', 'Traffic'], as_index=False)['Delivery_Time'].mean()
            fig_delay = px.bar(
                delay_data, x='Weather', y='Delivery_Time', color='Traffic', 
                barmode='group', template="plotly_dark",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_delay.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_delay, use_container_width=True)

        with t2_col2:
            # Compulsory Visual 2: Vehicle Comparison (Bar Chart)
            veh_data = filtered_df.groupby('Vehicle', as_index=False)['Delivery_Time'].mean().sort_values(by='Delivery_Time')
            fig_veh = px.bar(
                veh_data, x='Vehicle', y='Delivery_Time', color='Delivery_Time', 
                color_continuous_scale="Sunsetdark", template="plotly_dark"
            )
            fig_veh.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_veh, use_container_width=True)

    with tab3:
        st.markdown("### Category Volatility")
        # Compulsory Visual 5: Category Visualizer (Boxplot)
        fig_cat = px.box(
            filtered_df, x='Category', y='Delivery_Time', color='Category', 
            template="plotly_dark", points="all"
        )
        fig_cat.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_cat, use_container_width=True)
else:
    st.error("No data matches current filters. Please re-adjust parameters.")
