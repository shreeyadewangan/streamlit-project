import pandas as pd
import streamlit as st

st.set_page_config(page_title="E-commerce Clickstream Analysis", layout="wide")

st.title("🛒 E-commerce Clickstream Analysis")
st.write("User behavior, sessions, and conversion insights")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("ecommerce_clickstream_transactions.csv")

df = load_data()

# Dataset overview
st.header("📊 Dataset Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Unique Users", df['UserID'].nunique())

st.dataframe(df.head())

# Event distribution
st.header("📌 Event Distribution")
event_counts = df['EventType'].value_counts()
st.bar_chart(event_counts)

# Conversion metrics
df['is_purchase'] = df['EventType'] == 'purchase'
total_sessions = df['SessionID'].nunique()
purchase_sessions = df[df['is_purchase']]['SessionID'].nunique()
conversion_rate = purchase_sessions / total_sessions

st.header("💰 Conversion Metrics")
st.metric("Session Conversion Rate", f"{conversion_rate:.2%}")

# Repeated product views
st.header("🔁 Repeated Product Views")

product_views = df[
    (df['EventType'] == 'product_view') &
    (df['ProductID'].notna())
]

user_product_views = (
    product_views
    .groupby(['UserID', 'ProductID'])
    .size()
    .reset_index(name='view_count')
)

repeated_views = user_product_views[user_product_views['view_count'] > 1]

st.dataframe(repeated_views.head(20))