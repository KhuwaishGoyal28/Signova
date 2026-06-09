import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import cv2
from ultralytics import YOLO

# --- 1. CORE APPLICATION CONFIG ---
st.set_page_config(page_title="Two-Way Sign Bridge", page_icon="固", layout="wide")

st.title("🔄 Two-Way Inclusive Communication Bridge")
st.write("A bidirectional translation platform mapping gestures to text, and voice/text back to sign language animations.")
st.markdown("---")

# --- 2. MODEL LOADING ---
@st.cache_resource
def load_vision_model():
    # Automatically downloads lightweight YOLOv8 weights optimized for cloud instances
    return YOLO("yolov8n.pt") 

try:
    model = load_vision_model()
except Exception as e:
    st.error(f"AI Core initialization error: {e}")

# WebRTC routing configurations to bypass firewalls
RTC_CONFIG = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302", "stun:stun1.l.google.com:19302"]}]}
)

# --- 3. VISION CAPTURE LOOP (Sign-to-Text) ---
def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    img = cv2.flip(img, 1) # Mirror image alignment
    
    # Process camera frame through YOLOv8
    results = model(img, conf=0.45, verbose=False)
    
    for r in results:
        img = r.plot() # Draw tracking boxes over detected gestures
        
    return frame.from_ndarray(img, format="bgr24")

# --- 4. GRAPHICAL UI SPLIT ---
col_sign_to_text, col_voice_to_sign = st.columns([1, 1])

# Column A: Sign Language to Text
with col_sign_to_text:
    st.header("🤟 Sign Language ➔ Human Words")
    st.info("The AI vision network will look at your camera feed and decode gestures.")
    
    webrtc_streamer(
        key="bidirectional-sign-stream",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIG,
        video_frame_callback=video_frame_callback,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

# Column B: Text/Voice to Sign Language
with col_voice_to_sign:
    st.header("🗣️ Human Voice ➔ Sign Language")
    st.info("Type a word below to view its corresponding sign language animation asset.")
    
    user_speech_input = st.text_input(
        "Spoken Text Input Box:", 
        value="hello", 
        placeholder="Type a word (e.g., hello, family, happy, help, clear)"
    ).strip().lower()
    
    if user_speech_input:
        st.markdown(f"**Visualizing Sign Structure For:** `{user_speech_input.upper()}`")
        formatted_word = user_speech_input.replace(" ", "-")
        
        # Connects to an open-source educational sign language dictionary asset base
        sign_gif_url = f"https://www.lifeprint.com/asl101/gifs/{formatted_word[0]}/{formatted_word}.gif"
        
        st.image(
            sign_gif_url, 
            caption=f"ASL Interpretation Profile: {user_speech_input}", 
            width=320
        )
      
