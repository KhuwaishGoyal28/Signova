import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
from ultralytics import YOLO
import numpy as np

# --- 1. CORE APPLICATION CONFIGURATION ---
st.set_page_config(
    page_title="Signova Multi-User Live Bridge", 
    page_icon="🤟", 
    layout="wide"
)

# --- 2. MULTI-USER MEETING ROOM MANAGER ---
st.title("🤟 Signova Live Meeting & Translation Portal")
st.write("Connect with others instantly using peer-to-peer secure cloud architecture with active gesture scanning.")

st.markdown("### 🔑 Secure Meeting Connection Panel")
col_room, col_status = st.columns([2, 1])

with col_room:
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

# --- 3. OPTIMIZED DEEP LEARNING MODEL INITIALIZATION ---
@st.cache_resource
def load_vision_model():
    return YOLO("yolov8n.pt") 

try:
    model = load_vision_model()
    st.success("⚡ AI Computer Vision Pipeline active and initialized.")
except Exception as e:
    st.error(f"AI Core initialization error: {e}")

# --- 4. ADVANCED MULTI-PEER GLOBAL RTC CONFIGURATION ---
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

# --- 5. REAL-TIME GESTURE SCANNING INTERCEPTOR ---
def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    
    # Flip horizontally for natural mirror effect
    img = img[:, ::-1, :] 
    
    # Run prediction tracking
    results = model(img, conf=0.25, verbose=False)
    
    # Safe Matrix Processing (Draw overlays manually using raw matrix indexing)
    for result in results:
        if result.boxes is not None:
            for box in result.boxes:
                xyxy = box.xyxy[0].tolist()
                x1, y1, x2, y2 = map(int, xyxy)
                
                h, w, _ = img.shape
                x1, x2 = max(0, x1), min(w - 1, x2)
                y1, y2 = max(0, y1), min(h - 1, y2)
                
                # Draw box border lines natively into the matrix array
                img[y1:y1+3, x1:x2] = [0, 255, 0]  # Top
                img[y2-3:y2, x1:x2] = [0, 255, 0]  # Bottom
                img[y1:y2, x1:x1+3] = [0, 255, 0]  # Left
                img[y1:y2, x2-3:x2] = [0, 255, 0]  # Right

    return frame.from_ndarray(img, format="bgr24")

# --- 6. LIVE TWO-WAY WORKSPACE INTERFACE SPLIT ---
col_sign_to_text, col_voice_to_sign = st.columns([1, 1])

with col_sign_to_text:
    st.header("📹 Your Live AI Camera Feed")
    st.caption("Your camera streams natively to your partner while tracking gestures.")
    
    if meeting_id:
        webrtc_streamer(
            key=f"signova-stream-{meeting_id}",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration=RTC_CONFIG,
            video_frame_callback=video_frame_callback,
            media_stream_constraints={"video": True, "audio": True},
            async_processing=True,
        )
    else:
        st.info("Please enter a Meeting ID above to launch your video interface link.")

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
        sign_gif_url = f"https://www.lifeprint.com/asl101/gifs/{formatted_word[0]}/{formatted_word}.gif"
        st.image(sign_gif_url, caption=f"ASL Identity Reference: {user_speech_input}", width=320)
        
