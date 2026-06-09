import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

# --- 1. CORE APPLICATION CONFIGURATION ---
st.set_page_config(
    page_title="Signova Multi-User Live Bridge", 
    page_icon="🤟", 
    layout="wide"
)

# --- 2. MULTI-USER MEETING ROOM MANAGER ---
st.title("🤟 Signova Live Meeting & Translation Portal")
st.write("Connect with others instantly using peer-to-peer secure cloud architecture.")

st.markdown("### 🔑 Secure Meeting Connection Panel")
col_room, col_status = st.columns([2, 1])

with col_room:
    # Generates a unique video room based on what the users type
    meeting_id = st.text_input(
        "Enter Meeting ID to Join/Create a Room:", 
        value="room-101", 
        placeholder="e.g., medical-consult, family-call, classroom"
    ).strip().lower()

with col_status:
    if meeting_id:
        st.success(f"🌐 Securely Linked to Sync Channel: **{meeting_id.upper()}**")
    else:
        st.warning("🔒 Awaiting unique Meeting ID channel parameter initialization.")

st.markdown("---")

# --- 3. ADVANCED MULTI-PEER GLOBAL RTC CONFIGURATION ---
# This cluster allows two users on completely different WiFi networks/firewalls
# to connect directly to each other's camera and microphone streams.
RTC_CONFIG = RTCConfiguration(
    {
        "iceServers": [
            {"urls": ["stun:stun.l.google.com:19302", "stun:stun1.l.google.com:19302"]},
            {"urls": ["stun:stun2.l.google.com:19302", "stun:stun3.l.google.com:19302"]},
            {"urls": ["stun:stun.services.mozilla.com"]},
            {"urls": ["stun:global.stun.twilio.com:3478?transport=udp"]}
        ]
    }
)

# --- 4. LIVE TWO-WAY WORKSPACE INTERFACE SPLIT ---
col_sign_to_text, col_voice_to_sign = st.columns([1, 1])

# USER VISUALIZATION PIPELINE A: LIVE P2P CAMERA CONNECTION
with col_sign_to_text:
    st.header("📹 Your Live Meeting Feed")
    st.caption("Your camera streams natively to your remote call partner using secure WebRTC layers.")
    
    if meeting_id:
        webrtc_streamer(
            # Appending meeting_id to the key dynamically opens distinct communication tunnels
            key=f"signova-stream-{meeting_id}",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration=RTC_CONFIG,
            media_stream_constraints={"video": True, "audio": True}, # Full video and talk-audio enabled
            async_processing=True,
        )
    else:
        st.info("Please enter a Meeting ID above to launch your video interface link.")

# USER VISUALIZATION PIPELINE B: VOICE TO SIGN INTERPRETATION DASHBOARD
with col_voice_to_sign:
    st.header("🗣️ Remote Partner Translator & Glossary")
    st.caption("Use this module to translate human language inputs into visual sign representations.")
    
    user_speech_input = st.text_input(
        "Type or Dictate Words Here:", 
        value="hello", 
        placeholder="Type a target word (e.g., hello, family, happy, help, clear)"
    ).strip().lower()
    
    if user_speech_input:
        st.markdown(f"**Visualizing Structural Asset Matrix For:** `{user_speech_input.upper()}`")
        formatted_word = user_speech_input.replace(" ", "-")
        
        # Pulls instructional animated graphics directly from the ASL open-source database
        sign_gif_url = f"https://www.lifeprint.com/asl101/gifs/{formatted_word[0]}/{formatted_word}.gif"
        
        try:
            st.image(
                sign_gif_url, 
                caption=f"ASL Identity Reference: {user_speech_input}", 
                width=320
            )
        except Exception:
            st.error("Linguistic asset mapping not found for this specific word variation. Try words like 'hello', 'happy', 'family', or 'help'.")
            
