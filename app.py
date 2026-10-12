import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Amazon Delivery Dashboard", layout="wide")

st.title("Amazon Delivery Dashboard — Team Alpha")
st.caption("For the Logistics Operations Manager, to support daily delivery exception identification and dispatch decisions.")

@st.cache_data
def load_data():
    df = pd.read_csv("amazon_delivery.csv")


    for col in ['Weather', 'Traffic', 'Area', 'Vehicle', 'Category']:
        df[col] = df[col].astype(str).str.strip()

  
    df['Traffic'] = df['Traffic'].replace('nan', pd.NA)
    df['Weather'] = df['Weather'].replace('nan', pd.NA)

    df = df[df['Agent_Rating'] <= 5]

    return df

df = load_data()

st.sidebar.header("Filters")

area = st.sidebar.selectbox(
    "Area",
    ["All"] + sorted(df['Area'].dropna().unique().tolist())
)
weather = st.sidebar.selectbox(
    "Weather",
    ["All"] + sorted(df['Weather'].dropna().unique().tolist())
)
traffic = st.sidebar.selectbox(
    "Traffic",
    ["All"] + sorted(df['Traffic'].dropna().unique().tolist())
)

df_f = df.copy()
if area != "All":
    df_f = df_f[df_f['Area'] == area]
if weather != "All":
    df_f = df_f[df_f['Weather'] == weather]
if traffic != "All":
    df_f = df_f[df_f['Traffic'] == traffic]

avg_delivery = df_f['Delivery_Time'].mean()
delayed_orders = (df_f['Delivery_Time'] > 180).sum()
avg_rating = df_f['Agent_Rating'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Avg Delivery Time", f"{avg_delivery:.1f} min")
col2.metric("Delayed Orders (>180 min)", f"{delayed_orders}")
col3.metric("Avg Agent Rating", f"{avg_rating:.2f}")

st.subheader("Why and where deliveries are slow")

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

df_f.groupby('Area')['Delivery_Time'].mean().sort_values().plot(
    kind='bar', ax=axes[0], title='Avg Delivery Time by Area'
)
axes[0].set_ylabel("Minutes")
axes[0].tick_params(axis='x', rotation=0)

df_f.groupby('Weather')['Delivery_Time'].mean().sort_values().plot(
    kind='bar', ax=axes[1], title='Avg Delivery Time by Weather'
)
axes[1].set_ylabel("Minutes")
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
st.pyplot(fig)

st.caption("Note: Semi-Urban has only 152 orders; its average delivery time is less reliable.")

st.caption("Data period: Feb 2022 – Apr 2022, Kaggle snapshot. Production refresh: nightly.")
st.caption("Delivery_Time unit: minutes (assumed). Exact definition not specified in the dataset.")
st.caption("Agent_Rating > 5 filtered out as invalid.")

with st.expander("View detail data"):
    st.dataframe(df_f.head(100))