import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Score distribution", layout="wide")
st.title("Score distribution by group")


@st.cache_data
def load_data():
    rng = np.random.default_rng(42)
    groups = {
        "Group A": rng.normal(70, 8, 100),
        "Group B": rng.normal(75, 12, 100),
        "Group C": rng.normal(65, 5, 100),
        "Group D": np.concatenate([rng.normal(80, 6, 95), [40, 45, 120]]),
    }
    return pd.DataFrame(
        [(g, v) for g, vals in groups.items() for v in vals],
        columns=["group", "score"],
    )


df = load_data()

# Sidebar controls
selected = st.sidebar.multiselect(
    "Groups", df["group"].unique(), default=list(df["group"].unique())
)
points = st.sidebar.selectbox("Points", ["outliers", "all", False])

filtered = df[df["group"].isin(selected)]

fig = px.box(filtered, x="group", y="score", color="group", points=points)
fig.update_layout(showlegend=False)

st.plotly_chart(fig, use_container_width=True)
st.dataframe(filtered.groupby("group")["score"].describe().round(1))