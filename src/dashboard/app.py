import streamlit as st

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="N100 Financial Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# Pages
# --------------------------------------------------
pg = st.navigation(
    [
        st.Page(
            "pages/home.py",
            title="Home",
            icon="🏠",
            default=True,
        ),
        st.Page(
            "pages/profile.py",
            title="Profile",
            icon="👤",
        ),
        st.Page(
            "pages/screener.py",
            title="Screener",
            icon="🔎",
        ),
        st.Page(
            "pages/peers.py",
            title="Peers",
            icon="👥",
        ),
        st.Page(
            "pages/trends.py",
            title="Trends",
            icon="📈",
        ),
        st.Page(
            "pages/sectors.py",
            title="Sectors",
            icon="🏭",
        ),
        st.Page(
            "pages/capital.py",
            title="Capital",
            icon="🏦",
        ),
        st.Page(
            "pages/reports.py",
            title="Reports",
            icon="📄",
        ),
    ]
)

# --------------------------------------------------
# Run Selected Page
# --------------------------------------------------
pg.run()
