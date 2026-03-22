import streamlit as st
import joblib
import numpy as np

# ── Load Model ────────────────────────────────────────────
model = joblib.load("model.pkl")

# ── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="Phishing Website Detector",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ Phishing Website Detector")
st.write("Enter website features below to check if it's **Safe or Phishing**")

# ── Sidebar Info ──────────────────────────────────────────
st.sidebar.title("ℹ️ About")
st.sidebar.info("""
This app uses a **Random Forest ML model**
trained on 11,000+ websites to detect
phishing websites.

- `-1` = Phishing / Suspicious
- `1`  = Legitimate / Safe
""")

# ── Input Features ────────────────────────────────────────
st.subheader("📋 Enter Website Features")
st.write("Use `1` = Yes/Safe, `-1` = No/Suspicious, `0` = Neutral")

col1, col2, col3 = st.columns(3)

with col1:
    UsingIP         = st.selectbox("Using IP Address",     [-1, 0, 1])
    LongURL         = st.selectbox("Long URL",             [-1, 0, 1])
    ShortURL        = st.selectbox("Short URL",            [-1, 0, 1])
    Symbol          = st.selectbox("Symbol @",             [-1, 0, 1])
    Redirecting     = st.selectbox("Redirecting //",       [-1, 0, 1])
    PrefixSuffix    = st.selectbox("Prefix Suffix -",      [-1, 0, 1])
    SubDomains      = st.selectbox("Sub Domains",          [-1, 0, 1])
    HTTPS           = st.selectbox("HTTPS",                [-1, 0, 1])
    DomainRegLen    = st.selectbox("Domain Reg Length",    [-1, 0, 1])
    Favicon         = st.selectbox("Favicon",              [-1, 0, 1])

with col2:
    NonStdPort      = st.selectbox("Non Std Port",         [-1, 0, 1])
    HTTPSDomainURL  = st.selectbox("HTTPS Domain URL",     [-1, 0, 1])
    RequestURL      = st.selectbox("Request URL",          [-1, 0, 1])
    AnchorURL       = st.selectbox("Anchor URL",           [-1, 0, 1])
    LinksInTags     = st.selectbox("Links In Tags",        [-1, 0, 1])
    ServerForm      = st.selectbox("Server Form Handler",  [-1, 0, 1])
    InfoEmail       = st.selectbox("Info Email",           [-1, 0, 1])
    AbnormalURL     = st.selectbox("Abnormal URL",         [-1, 0, 1])
    Forwarding      = st.selectbox("Website Forwarding",   [-1, 0, 1])
    StatusBar       = st.selectbox("Status Bar Cust",      [-1, 0, 1])

with col3:
    DisableRight    = st.selectbox("Disable Right Click",  [-1, 0, 1])
    Popup           = st.selectbox("Using Popup Window",   [-1, 0, 1])
    Iframe          = st.selectbox("Iframe Redirection",   [-1, 0, 1])
    AgeDomain       = st.selectbox("Age of Domain",        [-1, 0, 1])
    DNSRecord       = st.selectbox("DNS Recording",        [-1, 0, 1])
    WebTraffic      = st.selectbox("Website Traffic",      [-1, 0, 1])
    PageRank        = st.selectbox("Page Rank",            [-1, 0, 1])
    GoogleIndex     = st.selectbox("Google Index",         [-1, 0, 1])
    LinksPointing   = st.selectbox("Links Pointing To",    [-1, 0, 1])
    StatsReport     = st.selectbox("Stats Report",         [-1, 0, 1])

# ── Predict Button ────────────────────────────────────────
st.markdown("---")
if st.button("🔍 Check Website", use_container_width=True):

    # Collect all inputs
    features = np.array([[
        UsingIP, LongURL, ShortURL, Symbol, Redirecting,
        PrefixSuffix, SubDomains, HTTPS, DomainRegLen, Favicon,
        NonStdPort, HTTPSDomainURL, RequestURL, AnchorURL, LinksInTags,
        ServerForm, InfoEmail, AbnormalURL, Forwarding, StatusBar,
        DisableRight, Popup, Iframe, AgeDomain, DNSRecord,
        WebTraffic, PageRank, GoogleIndex, LinksPointing, StatsReport
    ]])

    prediction = model.predict(features)[0]

    # ── Show Result ───────────────────────────────────────
    if prediction == -1:
        st.error("🚨 WARNING — This website looks like PHISHING!")
        st.markdown("### ❌ Do NOT visit this website")
    else:
        st.success("✅ This website appears to be LEGITIMATE")
        st.markdown("### 🟢 Website looks Safe")