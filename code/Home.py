import streamlit as st
import base64

st.set_page_config(page_title="NBA Compatibility Model", layout="wide")

st.title("🏀 Dynamic Duos")
st.subheader("Evaluating NBA Player Compatibility on Team Success")

st.markdown("""
Welcome to the interactive demo of my NBA player compatibility project! This app lets you explore how well players fit together based on their statistical profiles, using a data science model trained on 2023–24 NBA data.

### 🔍 What You Can Do
- **Duo Compatibility Explorer** – Select any two players and see their compatibility score.
- **PCA Playing Style Landscape** – Visualize players in a 2D space and explore style-based clusters.
- **Durant Trade Scenarios** – Evaluate potential trade destinations based on fit.

### 📊 Methodology
This model uses XGBoost regression to predict minutes played between duos as a proxy for compatibility. It incorporates engineered features and synergy terms, followed by a log-based transformation and MinMax normalization.

### 📅 Data Scope
All results are based on 2023–24 regular season data from Basketball Reference.
""")

st.info("Use the sidebar to navigate to a specific section of the app.")

with open("Sydnee's_paper.pdf", "rb") as f:
    base64_pdf = base64.b64encode(f.read()).decode('utf-8')

pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
st.markdown("### Read the Paper Below 📄")
st.markdown(pdf_display, unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Poster 1 📄")
    st.image("Sydnee's_capstone.png", use_container_width=True)

with col2:
    st.markdown("### Poster 2 🖼️")
    st.image("Sydnee's_design.png", use_container_width=True)


