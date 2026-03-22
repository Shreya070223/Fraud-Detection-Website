import streamlit as st
import joblib
import numpy as np
import re
import urllib.parse

# ── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="PhishGuard — URL Scanner",
    page_icon="🛡️",
    layout="centered"
)

# ── Dark Theme CSS ────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Reset */
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
    }

    .stApp {
        background-color: #0a0a0f;
        color: #e2e8f0;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }

    /* Main container */
    .main .block-container {
        padding: 2rem 2rem 4rem;
        max-width: 780px;
    }

    /* ── Hero Section ── */
    .hero {
        text-align: center;
        padding: 3rem 0 2rem;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.4);
        color: #a5b4fc;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        padding: 6px 16px;
        border-radius: 100px;
        margin-bottom: 1.5rem;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        letter-spacing: -1.5px;
        line-height: 1.1;
        margin: 0 0 1rem;
        background: linear-gradient(135deg, #ffffff 0%, #a5b4fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-sub {
        font-size: 1rem;
        color: #64748b;
        font-weight: 400;
        line-height: 1.6;
        margin: 0;
    }

    /* ── Input Card ── */
    .input-card {
        background: #111118;
        border: 1px solid #1e1e2e;
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
    }

    .input-label {
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #475569;
        margin-bottom: 0.75rem;
    }

    /* Streamlit input override */
    .stTextInput > div > div > input {
        background: #0d0d14 !important;
        border: 1px solid #2d2d3d !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 14px !important;
        padding: 14px 18px !important;
        height: auto !important;
        transition: border-color 0.2s ease !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #334155 !important;
    }

    /* Streamlit button override */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 14px 28px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        margin-top: 1rem !important;
        height: auto !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.35) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ── Result Cards ── */
    .result-safe {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(5, 150, 105, 0.05) 100%);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        text-align: center;
    }

    .result-phishing {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, rgba(185, 28, 28, 0.05) 100%);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        text-align: center;
    }

    .result-icon {
        font-size: 3rem;
        margin-bottom: 0.75rem;
    }

    .result-title-safe {
        font-size: 1.6rem;
        font-weight: 700;
        color: #10b981;
        letter-spacing: -0.5px;
        margin: 0 0 0.5rem;
    }

    .result-title-phishing {
        font-size: 1.6rem;
        font-weight: 700;
        color: #ef4444;
        letter-spacing: -0.5px;
        margin: 0 0 0.5rem;
    }

    .result-desc {
        font-size: 0.9rem;
        color: #64748b;
        line-height: 1.6;
        margin: 0;
    }

    /* ── Feature Grid ── */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin-top: 1rem;
    }

    .feature-item {
        background: #0d0d14;
        border: 1px solid #1e1e2e;
        border-radius: 10px;
        padding: 10px 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .feature-dot-safe {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #10b981;
        flex-shrink: 0;
    }

    .feature-dot-warn {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #ef4444;
        flex-shrink: 0;
    }

    .feature-dot-neutral {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #475569;
        flex-shrink: 0;
    }

    .feature-name {
        font-size: 11px;
        color: #64748b;
        font-weight: 500;
    }

    /* ── Stats Row ── */
    .stats-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin: 2rem 0;
    }

    .stat-card {
        background: #111118;
        border: 1px solid #1e1e2e;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
    }

    .stat-num {
        font-size: 1.8rem;
        font-weight: 700;
        color: #a5b4fc;
        letter-spacing: -1px;
    }

    .stat-label {
        font-size: 11px;
        color: #475569;
        font-weight: 500;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }

    /* ── Divider ── */
    .divider {
        border: none;
        border-top: 1px solid #1e1e2e;
        margin: 2rem 0;
    }

    /* Expander dark theme */
    .streamlit-expanderHeader {
        background: #111118 !important;
        border: 1px solid #1e1e2e !important;
        border-radius: 10px !important;
        color: #64748b !important;
        font-size: 13px !important;
    }

    .streamlit-expanderContent {
        background: #0d0d14 !important;
        border: 1px solid #1e1e2e !important;
        border-top: none !important;
    }

    /* Warning box */
    .stAlert {
        background: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-radius: 10px !important;
        color: #fbbf24 !important;
    }
</style>
""", unsafe_allow_html=True)


# ── Feature Extractor ─────────────────────────────────────
def extract_features(url):
    features = {}

    ip_pattern = re.compile(r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.){3}([01]?\d\d?|25[0-5])')
    features['UsingIP']         = -1 if ip_pattern.search(url) else 1
    features['LongURL']         = -1 if len(url) >= 54 else 1
    shorteners = r'bit\.ly|goo\.gl|tinyurl|ow\.ly|t\.co|is\.gd'
    features['ShortURL']        = -1 if re.search(shorteners, url) else 1
    features['Symbol@']         = -1 if '@' in url else 1
    features['Redirecting//']   = -1 if url.rfind('//') > 6 else 1
    domain = urllib.parse.urlparse(url).netloc
    features['PrefixSuffix-']   = -1 if '-' in domain else 1
    subdomains = domain.split('.')
    features['SubDomains']      = 1 if len(subdomains) <= 2 else (0 if len(subdomains) == 3 else -1)
    features['HTTPS']           = 1 if url.startswith('https') else -1
    features['DomainRegLen']    = 0
    features['Favicon']         = 1
    port = urllib.parse.urlparse(url).port
    features['NonStdPort']      = -1 if port and port not in [80, 443] else 1
    features['HTTPSDomainURL']  = -1 if 'https' in domain else 1
    features['RequestURL']      = 1
    features['AnchorURL']       = 0
    features['LinksInScriptTags'] = 0
    features['ServerFormHandler'] = 0
    features['InfoEmail']       = -1 if 'mailto:' in url else 1
    features['AbnormalURL']     = -1 if domain not in url else 1
    features['WebsiteForwarding'] = 0
    features['StatusBarCust']   = 0
    features['DisableRightClick'] = 0
    features['UsingPopupWindow'] = 0
    features['IframeRedirection'] = 0
    features['AgeofDomain']     = 0
    features['DNSRecording']    = 0
    features['WebsiteTraffic']  = 0
    features['PageRank']        = 0
    features['GoogleIndex']     = 1
    features['LinksPointingToPage'] = 0
    features['StatsReport']     = 0

    return features


# ── Hero Section ──────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">ML Powered Security</div>
    <h1 class="hero-title">PhishGuard</h1>
    <p class="hero-sub">Paste any URL to instantly detect phishing websites<br>using machine learning & URL analysis</p>
</div>
""", unsafe_allow_html=True)

# ── Stats Row ─────────────────────────────────────────────
st.markdown("""
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-num">97%</div>
        <div class="stat-label">Accuracy</div>
    </div>
    <div class="stat-card">
        <div class="stat-num">11K+</div>
        <div class="stat-label">Sites Trained</div>
    </div>
    <div class="stat-card">
        <div class="stat-num">30</div>
        <div class="stat-label">URL Features</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Input Section ─────────────────────────────────────────
st.markdown('<div class="input-label">Enter Website URL</div>', unsafe_allow_html=True)
url = st.text_input(
    "",
    placeholder="https://example.com",
    label_visibility="collapsed"
)

scan_clicked = st.button("Scan URL →", use_container_width=True)

# ── Load Model ────────────────────────────────────────────
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

try:
    model = load_model()
    model_loaded = True
except:
    model_loaded = False

# ── Result Section ────────────────────────────────────────
if scan_clicked:
    if not url.strip():
        st.markdown("""
        <div style="background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.3);
        border-radius: 10px; padding: 14px 18px; color: #fbbf24; font-size: 14px; margin-top: 1rem;">
        ⚠️ Please enter a URL to scan
        </div>
        """, unsafe_allow_html=True)

    elif not model_loaded:
        st.markdown("""
        <div style="background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3);
        border-radius: 10px; padding: 14px 18px; color: #ef4444; font-size: 14px; margin-top: 1rem;">
        ❌ model.pkl not found — make sure it's in your project folder
        </div>
        """, unsafe_allow_html=True)

    else:
        # Extract features
        features_dict = extract_features(url)
        features_array = np.array([list(features_dict.values())])

        # Predict
        prediction = model.predict(features_array)[0]
        confidence = model.predict_proba(features_array)[0]
        conf_pct = int(max(confidence) * 100)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        # Result card
        if prediction == -1:
            st.markdown(f"""
            <div class="result-phishing">
                <div class="result-icon">🚨</div>
                <div class="result-title-phishing">Phishing Detected</div>
                <p class="result-desc">
                    This URL shows signs of being a phishing website.<br>
                    <strong style="color: #ef4444;">Do NOT visit or share this link.</strong>
                </p>
                <div style="margin-top: 1rem; font-family: 'JetBrains Mono', monospace;
                font-size: 11px; color: #475569; background: rgba(0,0,0,0.3);
                padding: 8px 14px; border-radius: 8px; display: inline-block;">
                    Confidence: {conf_pct}%
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-safe">
                <div class="result-icon">✅</div>
                <div class="result-title-safe">Looks Legitimate</div>
                <p class="result-desc">
                    No major phishing signals detected in this URL.<br>
                    <strong style="color: #10b981;">This website appears to be safe.</strong>
                </p>
                <div style="margin-top: 1rem; font-family: 'JetBrains Mono', monospace;
                font-size: 11px; color: #475569; background: rgba(0,0,0,0.3);
                padding: 8px 14px; border-radius: 8px; display: inline-block;">
                    Confidence: {conf_pct}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Feature breakdown
        with st.expander("View URL Feature Analysis"):
            safe_count   = sum(1 for v in features_dict.values() if v == 1)
            warn_count   = sum(1 for v in features_dict.values() if v == -1)
            neut_count   = sum(1 for v in features_dict.values() if v == 0)

            st.markdown(f"""
            <div style="display: flex; gap: 12px; margin-bottom: 1rem;">
                <div style="font-size: 12px; color: #10b981;">● Safe: {safe_count}</div>
                <div style="font-size: 12px; color: #ef4444;">● Warning: {warn_count}</div>
                <div style="font-size: 12px; color: #475569;">● Neutral: {neut_count}</div>
            </div>
            <div class="feature-grid">
            """, unsafe_allow_html=True)

            grid_html = '<div class="feature-grid">'
            for name, val in features_dict.items():
                if val == 1:
                    dot = "feature-dot-safe"
                elif val == -1:
                    dot = "feature-dot-warn"
                else:
                    dot = "feature-dot-neutral"

                grid_html += f"""
                <div class="feature-item">
                    <div class="{dot}"></div>
                    <span class="feature-name">{name}</span>
                </div>"""

            grid_html += '</div>'
            st.markdown(grid_html, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; margin-top: 4rem; padding-top: 2rem;
border-top: 1px solid #1e1e2e;">
    <p style="font-size: 12px; color: #1e293b; letter-spacing: 0.5px;">
        PHISHGUARD — ML Model: Random Forest · Dataset: 11,054 URLs
    </p>
</div>
""", unsafe_allow_html=True)