import streamlit as st

# ----------------------------
# PAGE CONFIG
# ----------------------------

st.set_page_config(
    page_title="CricStats Dashboard",
    layout="wide"
)

# ----------------------------
# STYLE
# ----------------------------

st.markdown("""
<style>

.main-title{
    font-size:40px;
    font-weight:700;
}

.subtitle{
    font-size:18px;
    color:#9aa4b2;
}

.card{
    padding:25px;
    border-radius:10px;
    background-color:#1f2937;
    border:1px solid #374151;
    color:white;
}

.card h3{
    color:white;
}

.card p{
    color:#d1d5db;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# HERO SECTION
# ----------------------------

st.markdown('<p class="main-title">CricStats Analytics Platform</p>', unsafe_allow_html=True)

st.markdown(
"""
<p class="subtitle">
A cricket analytics dashboard combining live match data, player performance insights,
SQL-based analysis, and database management in one platform.
</p>
""",
unsafe_allow_html=True
)

st.markdown("---")

# ----------------------------
# FEATURE CARDS
# ----------------------------

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
    <div class="card">
    <h3>Live Match Tracking</h3>
    <p>
    View real-time cricket matches including scores,
    venue information, and match progress.
    </p>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class="card">
    <h3>Player Statistics</h3>
    <p>
    Search players and analyze batting and bowling
    performance across different formats.
    </p>
    </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:

    st.markdown("""
    <div class="card">
    <h3>SQL Analytics</h3>
    <p>
    Run advanced SQL queries to explore trends,
    player rankings, and match insights.
    </p>
    </div>
    """, unsafe_allow_html=True)

with col4:

    st.markdown("""
    <div class="card">
    <h3>Database Management</h3>
    <p>
    Manage cricket data using CRUD operations
    including create, update, and delete.
    </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ----------------------------
# FOOTER
# ----------------------------

st.write(
"""
This project integrates **RapidAPI**, **SQLite**, and **Streamlit**
to build an interactive cricket analytics dashboard.
"""
)
