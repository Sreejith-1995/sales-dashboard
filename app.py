import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os


# ==========================
# LOGIN CONFIG
# ==========================

USERNAME = "sreejith"
PASSWORD = "teamphoenix@2026"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🔐 Team Phoenix Login")

    username = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid User ID or Password")

    st.stop()

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Team Phoenix CRM Dashboard",
    page_icon="🚀",
    layout="wide"
)

# =====================================================
# LOAD LOGO SAFELY
# =====================================================

logo_path = "assets/logo.png"

if os.path.exists(logo_path):
    logo = Image.open(logo_path)
else:
    logo = None

# =====================================================
# LOAD CSV SAFELY
# =====================================================

data_file = "sales_data.csv"

columns = [
    "Employee",
    "Demos Scheduled",
    "Demos Completed",
    "Won Deals",
    "Revenue",
    "Pipeline",
    "Closed-pipeline",
    "Industry"
]

if not os.path.exists(data_file) or os.path.getsize(data_file) == 0:
    df = pd.DataFrame(columns=columns)
    df.to_csv(data_file, index=False)
else:
    df = pd.read_csv(data_file)

df.columns = df.columns.str.strip()

if df.empty:
    df = pd.DataFrame(columns=columns)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.stApp {
    background-color: #000000;
}

.dashboard-title {
    text-align: left;
    color: white;
    font-size: 38px;
    font-weight: 700;
}

[data-testid="stSidebar"] {
    background-color: #0B1220;
    border-right: 1px solid #1F2937;
}

[data-testid="stSidebar"] * {
    color: #E5E7EB;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("📊 Filters")
st.sidebar.markdown("---")

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

if logo:
    st.sidebar.image(logo, use_container_width=True)

employee_filter = st.sidebar.selectbox(
    "Select Employee",
    ["All"] + list(df["Employee"].unique()) if len(df) > 0 else ["All"]
)

if employee_filter != "All":
    df = df[df["Employee"] == employee_filter]

# =====================================================
# HEADER
# =====================================================

c1, c2 = st.columns([1, 6])

with c1:
    if logo:
        st.image(logo, width=80)

with c2:
    st.markdown(
        "<div class='dashboard-title'>TEAM PHOENIX CRM DASHBOARD</div>",
        unsafe_allow_html=True
    )

st.markdown("---")

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Executive Summary",
    "👥 Team Performance",
    "📈 Pipeline Status",
    "🎯 Action Plan",
    "➕ CRM (Add / Update / Delete)"
])

# =====================================================
# TAB 1 - EXECUTIVE SUMMARY
# =====================================================

with tab1:

    st.subheader("Executive Summary")

    target = 25000

    total_revenue = df["Revenue"].sum() if len(df) else 0
    achievement = (total_revenue / target) * 100 if target else 0

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Demos Scheduled", df["Demos Scheduled"].sum() if len(df) else 0)
    c2.metric("Demos Completed", df["Demos Completed"].sum() if len(df) else 0)
    c3.metric("Won Deals", df["Won Deals"].sum() if len(df) else 0)
    c4.metric("Revenue", f"₹{total_revenue:,.0f}")
    c5.metric("Target Achievement", f"{achievement:.1f}%")

    st.progress(min(achievement / 100, 1.0))

# =====================================================
# TAB 2 - TEAM PERFORMANCE
# =====================================================

with tab2:

    st.subheader("👥 Team Performance")

    if len(df) > 0:

        table = df[[
            "Employee",
            "Demos Scheduled",
            "Demos Completed",
            "Won Deals",
            "Revenue",
            "Industry"
        ]]

        st.dataframe(table, use_container_width=True)

        st.markdown("---")

        fig = px.bar(
            df.sort_values("Revenue", ascending=False),
            x="Employee",
            y="Revenue",
            color="Revenue",
            template="plotly_dark",
            title="Revenue Ranking",
            text="Revenue"
        )

        fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')

        st.plotly_chart(fig, use_container_width=True)

# =====================================================
# TAB 3 - PIPELINE STATUS (RESTORED)
# =====================================================

with tab3:

    st.subheader("📈 Pipeline Status")

    if len(df) > 0:

        total_pipeline = df["Pipeline"].sum()
        total_closed = df["Closed-pipeline"].sum()
        open_pipeline = total_pipeline - total_closed

        c1, c2, c3 = st.columns(3)

        c1.metric("Total Pipeline", f"₹{total_pipeline:,.0f}")
        c2.metric("Closed Pipeline", f"₹{total_closed:,.0f}")
        c3.metric("Open Pipeline", f"₹{open_pipeline:,.0f}")

        st.markdown("---")

        st.subheader("Pipeline vs Closed Pipeline")

        fig = px.bar(
            df,
            x="Employee",
            y=["Pipeline", "Closed-pipeline"],
            barmode="group",
            template="plotly_dark",
            title="Pipeline vs Closed Pipeline"
        )

        fig.update_traces(texttemplate='%{y:,.0f}', textposition='outside')

        st.plotly_chart(fig, use_container_width=True)



# =====================================================
# TAB 4 - ACTION PLAN
# =====================================================

with tab4:

    st.subheader("Weekly Action Plan")

    st.info("""
1. Target ₹28,000 weekly revenue  
2. Improve demo conversion  
3. Focus on Education + Yoga + Sports leads  
4. Daily pipeline tracking  
5. Increase follow-ups  
""")

# =====================================================
# TAB 5 - CRM (ADD / UPDATE / DELETE)
# =====================================================

with tab5:

    st.subheader("➕ CRM Management")

    st.markdown("### Existing Records")

    st.dataframe(df, use_container_width=True)

    st.markdown("---")

    if len(df) > 0:

        index = st.selectbox("Select Record Index", df.index)

        row = df.loc[index]

        st.markdown("### ✏️ Edit Record")

        with st.form("edit_form"):

            employee = st.text_input("Employee", row["Employee"])
            scheduled = st.number_input("Demos Scheduled", value=int(row["Demos Scheduled"]))
            completed = st.number_input("Demos Completed", value=int(row["Demos Completed"]))
            won = st.number_input("Won Deals", value=int(row["Won Deals"]))
            revenue = st.number_input("Revenue", value=int(row["Revenue"]))
            pipeline = st.number_input("Pipeline", value=int(row["Pipeline"]))
            closed = st.number_input("Closed Pipeline", value=int(row["Closed-pipeline"]))
            industry = st.text_input("Industry", row["Industry"])

            update_btn = st.form_submit_button("Update")

        if update_btn:

            df.loc[index] = [
                employee,
                scheduled,
                completed,
                won,
                revenue,
                pipeline,
                closed,
                industry
            ]

            df.to_csv(data_file, index=False)
            st.success("Record updated successfully!")
            st.rerun()

        st.markdown("### 🗑 Delete Record")

        if st.button("Delete Selected Record"):

            df = df.drop(index).reset_index(drop=True)
            df.to_csv(data_file, index=False)

            st.warning("Record deleted successfully!")
            st.rerun()

    else:
        st.info("No records available")

    st.markdown("---")

    st.subheader("➕ Add New Entry")

    with st.form("add_form"):

        employee = st.text_input("Employee Name")
        scheduled = st.number_input("Demos Scheduled", 0)
        completed = st.number_input("Demos Completed", 0)
        won = st.number_input("Won Deals", 0)
        revenue = st.number_input("Revenue", 0)
        pipeline = st.number_input("Pipeline", 0)
        closed = st.number_input("Closed Pipeline", 0)

        industry = st.multiselect(
            "Industry",
            ["Sports & Martial Arts", "Dance/Music/Yoga", "Education", "Others"]
        )

        submit = st.form_submit_button("Add")

    if submit:

        new_row = pd.DataFrame([{
            "Employee": employee,
            "Demos Scheduled": scheduled,
            "Demos Completed": completed,
            "Won Deals": won,
            "Revenue": revenue,
            "Pipeline": pipeline,
            "Closed-pipeline": closed,
            "Industry": ", ".join(industry)
        }])

        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(data_file, index=False)

        st.success("New record added!")
        st.rerun()

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")
st.caption("Team Phoenix CRM Dashboard | Streamlit Powered")