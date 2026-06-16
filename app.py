import streamlit as st
from audio_recorder_streamlit import audio_recorder
from deep_translator import GoogleTranslator
from gtts import gTTS
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import tempfile
import whisper
import os

# ==========================================
# INITIALIZE SESSION STATE
# ==========================================
if "history" not in st.session_state:
    st.session_state.history = []

# ==========================================
# FFMPEG PATH
# ==========================================
os.environ["PATH"] += r";C:\Users\RO\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-essentials_build\bin"

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="VoiceBridge // Real-Time Translation",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed" # Cleanly hide native sidebar mechanics
)

# ==========================================
# ADVANCED GEN-Z DASHBOARD DESIGN SYSTEM
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* 1. Global Page Dark Theme Constraints */
.stApp, [data-testid="stAppViewContainer"], .main {
    background: #020617 !important;
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, h4, h5, h6, p, label, span, div {
    font-family: 'Inter', sans-serif !important;
}

h1, h2, h3, h4, p, label {
    color: #f8fafc !important;
}

/* Fix audio recorder container background white-out bug */
div[data-testid="stMarkdownContainer"] + div {
    background: transparent !important;
}

/* 2. Streamlit Header/Navbar UI Elements Purge */
header, #MainMenu, footer, [data-testid="stToolbar"], [data-testid="stHeader"] {
    visibility: hidden !important;
    display: none !important;
}

.block-container {
    padding-top: 1.5rem !important;
    margin-top: 0rem !important;
}

/* 3. Panel Container Boundaries */
.main-title {
    font-size: 38px;
    font-weight: 700;
    color: #f8fafc;
    letter-spacing: -0.05em;
}
.brand-accent {
    color: #8b5cf6;
}
.subtitle {
    color: #94a3b8;
    font-size: 16px;
    font-weight: 400;
    margin-top: 2px;
}

/* Premium Glassmorphism Overhaul Base */
.card,
.live-caption,
.history-card {
    backdrop-filter: blur(20px);
    background: rgba(15, 23, 42, 0.85) !important;
    border: 1px solid rgba(139, 92, 246, 0.15) !important;
}

.card {
    padding: 24px;
    border-radius: 16px;
    margin-top: 12px;
}

.panel-label {
    font-size: 12px;
    font-weight: 700;
    color: #8b5cf6 !important;
    letter-spacing: 0.15em;
    margin-bottom: 12px;
    text-transform: uppercase;
}

/* SaaS Style Structural App Left Container Panel */
.activity-panel {
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid #1e293b;
    border-radius: 20px;
    padding: 20px;
    min-height: 680px;
}

/* 4. Modern Subtitle Screen Container Card */
.live-caption {
    border-radius: 24px;
    padding: 40px;
    margin-top: 15px;
    min-height: 180px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 40px rgba(139, 92, 246, 0.08);
}

.caption-text {
    font-size: 34px;
    font-weight: 600;
    color: #f8fafc;
    text-align: center;
    line-height: 1.4;
}

/* 5. High Fidelity Recent Session Cards with Modern Flexbox Layout */
.history-card {
    border-left: 4px solid #8b5cf6 !important;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: 0.3s;
    cursor: pointer;
}

.history-card:hover {
    border-color: #8b5cf6 !important;
    transform: translateY(-2px);
}

.history-content {
    flex-grow: 1;
}

.history-arrow {
    color: #8b5cf6 !important;
    font-size: 32px;
    font-weight: 700;
    min-width: 30px;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    user-select: none;
}

/* Startup Clean Gray Footer */
.footer-text {
    color: #475569 !important;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.025em;
    text-align: center;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# APPLICATION HEADER
# ==========================================
col_logo, col_title = st.columns([1, 12])

with col_logo:
    try:
        st.image("images/logo.png", width=75)
    except:
        st.markdown("<h1 style='font-size:45px; margin:0; padding-top:5px;'>🔮</h1>", unsafe_allow_html=True)

with col_title:
    st.markdown("""
    <div class='main-title'>
        Voice<span class='brand-accent'>Bridge</span>
    </div>
    <div class='subtitle'>
        Real-Time Language Conversion Pipeline
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)


# ==========================================
# SPLIT DASHBOARD LAYOUT SYSTEM
# ==========================================
panel_left, panel_right = st.columns([1, 2.5])

# ==========================================
# LEFT APP PANEL — SYSTEM ACTIVITY TIMELINE
# ==========================================
with panel_left:
    st.markdown("<div class='panel-label'>ACTIVITY</div>", unsafe_allow_html=True)
    
    # Open Activity Panel Structural Div Container Box
    st.markdown("<div class='activity-panel'>", unsafe_allow_html=True)
    
    if not st.session_state.history:
        st.markdown("<p style='color: #94a3b8 !important; font-size:13px; padding: 10px;'>No active session records found.</p>", unsafe_allow_html=True)
    else:
        for item in reversed(st.session_state.history):
            st.markdown(f"""
            <div class="history-card">
                <div class="history-content">
                    <div style="color:#64748b; font-size:11px; font-weight:700; letter-spacing:1px;">ORIGINAL</div>
                    <div style="color:white; font-size:14px; margin-top:4px;">{item["english"][:20]}...</div>
                    <div style="color:#8b5cf6; font-size:11px; font-weight:700; margin-top:10px;">{item["lang"].upper()} VERSION</div>
                    <div style="color:#cbd5e1; font-size:14px; margin-top:2px;">{item["translated"][:20]}...</div>
                </div>
                <div class="history-arrow">❯</div>
            </div>
            """, unsafe_allow_html=True)
            
    # Close Activity Panel Structural Div Container Box
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# RIGHT APP PANEL — LIVE WORKSPACE TRANSLATION
# ==========================================
with panel_right:
    
    # Language Matrix Map Selection
    language_map = {
        "Telugu": "te",
        "Hindi": "hi",
        "Tamil": "ta",
        "Kannada": "kn",
        "Malayalam": "ml",
        "Marathi": "mr",
        "Gujarati": "gu",
        "Punjabi": "pa",
        "Bengali": "bn"
    }

    # Configuration Sub-grid Split System
    config_col, recorder_col = st.columns([1.2, 2])
    
    with config_col:
        st.markdown("<div class='panel-label'>LANGUAGE</div>", unsafe_allow_html=True)
        selected_language = st.selectbox(
            "Target Language Configuration",
            list(language_map.keys()),
            label_visibility="collapsed"
        )

    with recorder_col:
        st.markdown("<div class='panel-label'>VOICE CAPTURE</div>", unsafe_allow_html=True)
        audio_bytes = audio_recorder(
            text="Capture Audio Stream",
            recording_color="#ef4444",
            neutral_color="#8b5cf6"
        )

    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='panel-label'>LIVE CAPTIONS</div>", unsafe_allow_html=True)

    if audio_bytes:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio_bytes)
            audio_path = f.name

        with st.spinner("Processing neural calculation layers..."):
            model = whisper.load_model("base")
            result = model.transcribe(audio_path)
            english_text = result["text"]

            translated_text = GoogleTranslator(
                source="en",
                target=language_map[selected_language]
            ).translate(english_text)

        # Update activity array framework
        st.session_state.history.append({
            "english": english_text,
            "translated": translated_text,
            "lang": selected_language
        })

        # Text to speech synthesis processing
        tts = gTTS(
            text=translated_text,
            lang=language_map[selected_language]
        )
        tts.save("translated_audio.mp3")

        # Isolated Telugu processing scripts
        if selected_language == "Telugu":
            roman_subtitle = transliterate(
                translated_text,
                sanscript.TELUGU,
                sanscript.ITRANS
            )

        # Dynamic injection mapping to output container
        st.markdown(
            f"""
            <div class='live-caption'>
                <div class='caption-text'>
                    {translated_text}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)
        metric_left, metric_right = st.columns(2)

        with metric_left:
            st.markdown("<div class='panel-label'>ORIGINAL</div>", unsafe_allow_html=True)
            st.info(english_text)

        with metric_right:
            st.markdown(f"<div class='panel-label'>{selected_language.upper()} VERSION</div>", unsafe_allow_html=True)
            st.success(translated_text)
            
        if selected_language == "Telugu":
            st.markdown("<div class='panel-label'>PHONETIC SUBTITLE</div>", unsafe_allow_html=True)
            st.success(roman_subtitle)

        st.markdown("<br>", unsafe_allow_html=True)
        
        preview_col, download_col = st.columns([2, 1])
        with preview_col:
            st.markdown("<div class='panel-label'>VOICE PREVIEW</div>", unsafe_allow_html=True)
            st.audio("translated_audio.mp3")
        
        with download_col:
            st.markdown("<div class='panel-label'>TRANSCRIPT</div>", unsafe_allow_html=True)
            st.download_button(
                label="Export Session Text",
                data=f"ORIGINAL EN:\n{english_text}\n\nTARGET {selected_language.upper()}:\n{translated_text}\n",
                file_name=f"transcript_{selected_language.lower()}.txt",
                mime="text/plain",
                use_container_width=True
            )

        os.remove(audio_path)

    else:
        st.markdown("""
        <div class='live-caption'>
            <div class='caption-text' style='color:#475569;'>
                System Idle. Awaiting stream interface signal...
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# SYSTEM FOOTER
# ==========================================
st.markdown("<hr style='border-color: #1e293b; margin-top: 40px;'>", unsafe_allow_html=True)
st.markdown(
    """
    <div class='footer-text'>
        VoiceBridge v1.0
    </div>
    """,
    unsafe_allow_html=True
)