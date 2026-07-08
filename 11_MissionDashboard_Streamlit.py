import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Earth Observation Mission Simulator",
    page_icon="🛰",
    layout="wide"
)

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------

mission = pd.read_excel(
    os.path.join(BASE_DIR, "MissionStatistics.xlsx")
)

satellite = pd.read_excel(
    os.path.join(BASE_DIR, "SatellitePerformance.xlsx")
)

ground = pd.read_excel(
    os.path.join(BASE_DIR, "GroundStationPerformance.xlsx")
)

constellation = pd.read_excel(
    os.path.join(BASE_DIR, "ConstellationPerformance.xlsx")
)

# -------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------

st.success(
"""
🟢 Mission Status : ACTIVE

🛰 Constellation : 48 Satellites

📡 Ground Station : Brisbane

🌎 Coverage : Australia

📶 RF + Optical Links Operational
"""
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Earth Observation Mission Simulator\n\n"
    "48 Satellite Walker Constellation\n"
    "Altitude : 536 km\n"
    "Inclination : 50°"
)

# -------------------------------------------------------
# FUNCTIONS
# -------------------------------------------------------

def get_metric(name):

    return mission.loc[
        mission["Metric"] == name,
        "Value"
    ].values[0]
# -------------------------------------------------------
# MISSION OVERVIEW
# -------------------------------------------------------


page = st.sidebar.radio("Navigation",["Mission Overview","Satellite Performance","Ground Station","Constellation","Charts"])
if page == "Mission Overview":

    logo = os.path.join(BASE_DIR, "assets", "logo.png")

    c1, c2 = st.columns([1,5])

    with c1:
        st.image(logo, width=120)

    with c2:
        st.markdown("""
        # ANSUMI SPACE

        ### Earth Observation Mission Operations Dashboard
        """)

    st.markdown("### Mission Overview")

    total_images = get_metric("Total Images Captured")
    downloaded = get_metric("Downloaded Images")
    remaining = get_metric("Remaining Images")
    peak_memory = get_metric("Peak Memory (MB)")
    rf = get_metric("RF Downloads")
    optical = get_metric("Optical Downloads")

    efficiency = round(downloaded / total_images * 100, 2)

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "📷 Images Captured",
        f"{int(total_images)}"
    )

    c2.metric(
        "📡 Downloaded",
        f"{int(downloaded)}"
    )

    c3.metric(
        "💾 Remaining",
        f"{int(remaining)}"
    )

    c4, c5, c6 = st.columns(3)

    c4.metric(
        "🚀 Downlink Efficiency",
        f"{efficiency}%"
    )

    c5.metric(
        "🧠 Peak Memory",
        f"{int(peak_memory)} MB"
    )

    c6.metric(
        "🛰 RF / Optical",
        f"{int(rf)} / {int(optical)}"
    )

    st.markdown("---")

    st.subheader("Mission Statistics")

    st.dataframe(
        mission,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    st.subheader("Download Reports")

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            "📥 Mission Statistics",
            mission.to_csv(index=False),
            file_name="MissionStatistics.csv",
            mime="text/csv"
        )

    with col2:
        st.download_button(
            "📥 Constellation Performance",
            constellation.to_csv(index=False),
            file_name="ConstellationPerformance.csv",
            mime="text/csv"
        )
# -------------------------------------------------------
# SATELLITE PERFORMANCE
# -------------------------------------------------------

elif page == "Satellite Performance":
    st.title("🛰 Satellite Performance")

    st.markdown("### Complete Constellation Performance")

    st.dataframe(
        satellite,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    sat_name = st.selectbox(

        "Select Satellite",

        satellite["Satellite"]

    )

    sat = satellite[
        satellite["Satellite"] == sat_name
    ].iloc[0]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "📷 Captured",
        int(sat["Images Captured"])
    )

    c2.metric(
        "📡 Downloaded",
        int(sat["Images Downloaded"])
    )

    c3.metric(
        "💾 Remaining",
        int(sat["Images Remaining"])
    )

    c4.metric(
        "🧠 Peak Memory",
        f'{int(sat["Peak Memory (MB)"])} MB'
    )

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:

        fig = go.Figure()

        fig.add_trace(

            go.Bar(

                x=["Captured","Downloaded","Remaining"],

                y=[

                    sat["Images Captured"],

                    sat["Images Downloaded"],

                    sat["Images Remaining"]

                ]

            )

        )

        fig.update_layout(

            title=f"{sat_name} Image Statistics",

            height=450

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with c2:

        fig = go.Figure(

            go.Indicator(

                mode="gauge+number",

                value=sat["Download Efficiency (%)"],

                title={"text":"Download Efficiency (%)"},

                gauge={

                    "axis":{"range":[0,100]},

                    "bar":{"color":"green"}

                }

            )

        )

        fig.update_layout(height=450)

        st.plotly_chart(
            fig,
            use_container_width=True
        )
# -------------------------------------------------------
# GROUND STATION PERFORMANCE
# -------------------------------------------------------

elif page == "Ground Station":

    st.title("📡 Brisbane Ground Station")

    st.markdown("### Ground Station Performance")

    rf_contacts = ground.loc[
        ground["Metric"]=="RF Contacts",
        "Value"
    ].values[0]

    ol_contacts = ground.loc[
        ground["Metric"]=="Optical Contacts",
        "Value"
    ].values[0]

    rf_time = ground.loc[
        ground["Metric"]=="RF Contact Time (s)",
        "Value"
    ].values[0]

    ol_time = ground.loc[
        ground["Metric"]=="Optical Contact Time (s)",
        "Value"
    ].values[0]

    utilization = ground.loc[
        ground["Metric"]=="Ground Station Utilization (%)",
        "Value"
    ].values[0]

    c1,c2,c3 = st.columns(3)

    c1.metric(
        "📡 RF Contacts",
        int(rf_contacts)
    )

    c2.metric(
        "🔭 Optical Contacts",
        int(ol_contacts)
    )

    c3.metric(
        "📈 Utilization",
        f"{utilization}%"
    )

    c4,c5 = st.columns(2)

    c4.metric(
        "⏱ RF Contact Time",
        f"{round(rf_time/3600,2)} hrs"
    )

    c5.metric(
        "⏱ Optical Contact Time",
        f"{round(ol_time/3600,2)} hrs"
    )

    st.markdown("---")

    st.subheader("Ground Station Report")

    st.dataframe(
        ground,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    col1,col2 = st.columns(2)

    with col1:

        fig = px.pie(

            names=["RF","Optical"],

            values=[rf_contacts,ol_contacts],

            title="Contact Distribution"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.bar(

            x=["RF","Optical"],

            y=[rf_time,ol_time],

            labels={"x":"Link","y":"Time (s)"},

            title="Total Contact Time"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
# -------------------------------------------------------
# CONSTELLATION PERFORMANCE
# -------------------------------------------------------

elif page == "Constellation":

    st.title("🌏 Constellation Performance")

    st.markdown("### Overall Mission Performance")

    st.dataframe(
        constellation,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    total_sat = constellation.loc[
        constellation["Metric"]=="Total Satellites",
        "Value"
    ].values[0]

    total_images = constellation.loc[
        constellation["Metric"]=="Images Captured",
        "Value"
    ].values[0]

    downloaded = constellation.loc[
        constellation["Metric"]=="Images Downloaded",
        "Value"
    ].values[0]

    efficiency = constellation.loc[
        constellation["Metric"]=="Downlink Efficiency (%)",
        "Value"
    ].values[0]

    avg_memory = constellation.loc[
        constellation["Metric"]=="Average Peak Memory (MB)",
        "Value"
    ].values[0]

    peak_memory = constellation.loc[
        constellation["Metric"]=="Maximum Peak Memory (MB)",
        "Value"
    ].values[0]

    c1,c2,c3 = st.columns(3)

    c1.metric(
        "🛰 Satellites",
        int(total_sat)
    )

    c2.metric(
        "📷 Images",
        int(total_images)
    )

    c3.metric(
        "📡 Downloaded",
        int(downloaded)
    )

    c4,c5,c6 = st.columns(3)

    c4.metric(
        "🚀 Efficiency",
        f"{efficiency}%"
    )

    c5.metric(
        "💾 Avg Memory",
        f"{avg_memory:.0f} MB"
    )

    c6.metric(
        "🔥 Max Memory",
        f"{peak_memory:.0f} MB"
    )

    st.markdown("---")

    col1,col2 = st.columns(2)

    with col1:

        fig = px.bar(

            satellite,

            x="Satellite",

            y="Download Efficiency (%)",

            title="Download Efficiency by Satellite"

        )

        fig.update_xaxes(tickangle=90)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.bar(

            satellite,

            x="Satellite",

            y="Peak Memory (MB)",

            title="Peak Memory Usage"

        )

        fig.update_xaxes(tickangle=90)

        st.plotly_chart(
            fig,
            use_container_width=True
        )
# -------------------------------------------------------
# CHARTS
# -------------------------------------------------------

elif page == "Charts":

    st.title("📈 Mission Charts")

    col1, col2 = st.columns(2)

    # -------------------------------------------------
    # Images Captured vs Downloaded
    # -------------------------------------------------

    with col1:

        fig = px.bar(

            satellite,

            x="Satellite",

            y=["Images Captured","Images Downloaded"],

            barmode="group",

            title="Images Captured vs Downloaded"

        )

        fig.update_xaxes(tickangle=90)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -------------------------------------------------
    # Remaining Images
    # -------------------------------------------------

    with col2:

        fig = px.bar(

            satellite,

            x="Satellite",

            y="Images Remaining",

            title="Remaining Images"

        )

        fig.update_xaxes(tickangle=90)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("---")

    col3, col4 = st.columns(2)

    # -------------------------------------------------
    # Peak Memory
    # -------------------------------------------------

    with col3:

        fig = px.line(

            satellite,

            x="Satellite",

            y="Peak Memory (MB)",

            markers=True,

            title="Peak Memory Usage"

        )

        fig.update_xaxes(tickangle=90)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -------------------------------------------------
    # RF vs Optical
    # -------------------------------------------------

    with col4:

        rf = mission.loc[
            mission["Metric"]=="RF Downloads",
            "Value"
        ].values[0]

        optical = mission.loc[
            mission["Metric"]=="Optical Downloads",
            "Value"
        ].values[0]

        fig = px.pie(

            names=["RF","Optical"],

            values=[rf,optical],

            title="RF vs Optical Downloads"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("---")

    st.success("✅ Mission Dashboard Generated Successfully!")

# -------------------------------------------------------
# FOOTER
# -------------------------------------------------------

st.markdown("---")

st.markdown(
"""
### 🛰 Earth Observation Mission Simulator (EOMS)

**Mission Configuration**

- Walker Constellation: **6 × 8**
- Satellites: **48**
- Orbit Altitude: **536 km**
- Inclination: **98° (Sun-Synchronous Orbit)**
- Ground Station: **Brisbane**
- Downlink Links: **RF + Optical**

Developed using:

- GMAT
- Python
- Pandas
- Plotly
- Streamlit
"""
)
