# 🔴 DELHIVERY // AI TELEMETRY COMMAND CENTER

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Enterprise-FF4B4B.svg)
![Plotly](https://img.shields.io/badge/Plotly-3D_Engine-3F4F75.svg)
![Status](https://img.shields.io/badge/Status-System_Live-success.svg)

An advanced, enterprise-grade Last-Mile Delivery Analytics Dashboard built with Python and Streamlit. Designed for real-time logistics tracking, bottleneck detection, and AI-driven delay risk prediction. 

This system features a custom glassmorphism UI, a cinematic 3D startup sequence, and hardware-accelerated 3D data visualizations to provide a Silicon Valley-tier command center experience.

---

## ⚡ CORE FEATURES

### 🌐 3D Geospatial & Visual Intelligence
* **Cinematic Boot Sequence:** Custom CSS keyframe-animated 5-second splash screen featuring a 3D driving transport vehicle.
* **Agent Efficiency Matrix:** 3D interactive scatter plot mapping personnel age, rating, and delivery speed.
* **Geographic Topography:** 3D surface rendering of area-based traffic bottlenecks.
* **Transparent UI Engine:** Custom Plotly layouts seamlessly blended into a frosted glassmorphism dashboard.

### 🤖 Neural AI & Analytics
* **AI Delay-Risk Prediction:** Real-time scoring engine that calculates the probability of cascading network delays based on active environmental filters.
* **Automated Insights:** Dynamic text generation recommending operational rerouting when risk thresholds are exceeded.
* **Advanced Distributions:** Monthly macro-speed trends, failure density heatmaps, and transit time curves.

### ⚙️ Operational Controls
* **Live System Telemetry:** Top-level KPI cards tracking Active Shipments, Transit Velocity, Delay Ratios, and standard deviation thresholds.
* **Elite Roster Rankings:** Automated sorting of the top 10 fastest agents and best-performing operating zones.
* **Database Integrity:** Live data-quality reporting showing dropped rows and clean data percentages.
* **Hardware Export:** One-click CSV engine to export filtered matrix data for external processing.

---

## 🚀 HOW TO USE THIS DASHBOARD

This application operates as an interactive, real-time command center for last-mile delivery analytics. 

1. **Initialization:** Upon launching the app, allow the 5.5-second cinematic 3D startup sequence to complete. This establishes the neural telemetry interface and loads the dataset.
2. **Applying Filters:** Use the left-hand **⚙️ PARAMETERS** sidebar to filter the live data. You can select specific conditions for Atmosphere (Weather), Traffic Density, Asset Type (Vehicle), Freight Class (Category), and Sector (Area). The entire dashboard, including all charts and AI insights, recalculates instantly based on your selections.
3. **Interacting with 3D Graphics:** The charts in the "3D Geospatial & Core" tab are fully interactive. Click and drag to rotate the 3D Agent Matrix and Sector Topography maps. Scroll to zoom in and out to pinpoint specific data clusters.
4. **Exporting Data:** Once you have isolated a specific scenario using the sidebar filters (e.g., viewing only Heavy Traffic in Rainy weather), scroll to the bottom of the sidebar and click **DOWNLOAD FILTERED CSV** to export the exact dataset for external reporting.

---

## 📊 UNDERSTANDING THE VISUALIZATIONS

The dashboard is divided into four main tabs, housing 12 distinct analytical engines.

### 🌐 Tab 1: 3D Geospatial & Core
| Visualization | Type | Operational Meaning |
| :--- | :--- | :--- |
| **Personnel Efficiency Matrix** | 3D Scatter | Maps *Agent Rating* (X), *Agent Age* (Y), and *Delivery Time* (Z). Rotating this allows you to see if older or higher-rated agents consistently deliver faster than newer personnel. |
| **Sector Delay Topography** | 3D Surface | Maps *Operating Zone* (X), *Traffic Density* (Y), and *Avg Delivery Time* (Z). Peaks (white/red) indicate severe geographic bottlenecks under specific traffic conditions. |
| **Environmental Impact** | Grouped Bar | Compares *Delivery Time* across different *Weather* conditions, separated by *Traffic Density*. Identifies exactly how much weather multiplies traffic delays. |
| **Asset Performance** | Bar Chart | Ranks average *Delivery Time* by *Fleet Type* (e.g., Bike vs. Van). Identifies which vehicles navigate the current filtered conditions most efficiently. |
| **Freight Volatility Analysis** | Boxplot | Shows the statistical distribution of *Delivery Time* across *Product Categories*. Identifies which freight types suffer from the most unpredictable delivery windows. |

### 📈 Tab 2: Advanced Distributions
| Visualization | Type | Operational Meaning |
| :--- | :--- | :--- |
| **Macro Speed Trends** | Line Chart | Tracks average *Delivery Time* across simulated *Months*. Used to identify long-term seasonal performance degradation or improvement. |
| **Transit Time Curve** | Histogram | Displays the frequency volume of all *Delivery Times*. A curve skewed heavily to the right indicates systemic delays across the network. |
| **Late % by Weather** | Bar Chart | Shows the exact percentage of deliveries that breached the AI threshold (mean + 1 standard deviation) under each atmospheric condition. |
| **Late Ratio by Traffic** | Pie Chart | Breaks down the total volume of late deliveries by traffic density, visualizing the primary cause of network failure. |

### 🤖 Tab 3: AI Predictions & Insights
| Visualization | Type | Operational Meaning |
| :--- | :--- | :--- |
| **Live Network Risk Index** | Radial Gauge | An algorithmic score (0-100) combining current weather, traffic, and late-percentage metrics to predict the likelihood of cascading network failure. |
| **Automated Insights** | Text Output | Dynamic neural recommendations that instruct operations managers to reroute fleets or maintain current allocation based on the Risk Index. |

### 📋 Tab 4: Operations Rankings
| Visualization | Type | Operational Meaning |
| :--- | :--- | :--- |
| **Area Performance Ranking** | Data Table | Ranks all geographic sectors from fastest to slowest average delivery time, color-coded for quick triage. |
| **Elite Agent Roster** | Data Table | Highlights the top 10 fastest delivery personnel in the filtered dataset, rewarding high performance. |

---

**SYSTEM ARCHITECT:** Naman Jain 
**FRAMEWORK:** Streamlit | Plotly | Pandas | Custom CSS
