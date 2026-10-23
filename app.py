from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_PATH = Path(__file__).parent / "data" / "scores.csv"

st.set_page_config(page_title="Score distribution", layout="wide")
st.title("Score distribution by group")


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


df = load_data(DATA_PATH)

# Sidebar controls
groups = sorted(df["group"].unique())
selected = st.sidebar.multiselect("Groups", groups, default=groups)
points = st.sidebar.selectbox("Points", ["outliers", "all", False])

filtered = df[df["group"].isin(selected)]

fig = px.box(filtered, x="group", y="score", color="group", points=points)
fig.update_layout(showlegend=False)

st.plotly_chart(fig, use_container_width=True)
st.dataframe(filtered.groupby("group")["score"].describe().round(1))