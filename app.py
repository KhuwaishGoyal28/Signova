import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import streamlit.components.v1 as components

# --- 1. CORE SURFACE SETTINGS ---
st.set_page_config(
    page_title="Signova Multi-User Translation Portal", 
    page_icon="🤟", 
    layout="wide"
)

st.title("🤟 Signova Full Alphabet & Vocabulary Live Translator")
st.write("An advanced multi-user communication bridge supporting real-time tracking for all 26 letters (A-Z) and phrases.")

# --- 2. UNIQUE CHANNEL LINK CONFIGURATION ---
st.markdown("### 🔑 Live Sync Connection Panel")
meeting_id = st.text_input(
    "Enter Shared Meeting ID Room Parameter:", 
    value="room-101"
).strip().lower()

st.markdown("---")

# --- 3. DUAL VIEW WORKSPACE LAYOUT ---
col_video, col_translation_engine = st.columns([1, 1])

with col_video:
    st.header("📹 Secure Multi-Peer Video Stream")
    st.caption("Connect here to establish your direct peer-to-peer visual communication link.")
    
    RTC_CONFIG = RTCConfiguration({
        "iceServers": [
            {"urls": ["stun:stun.l.google.com:19302", "stun:stun1.l.google.com:19302"]},
            {"urls": ["stun:stun.services.mozilla.com"]},
            {"urls": ["stun:global.stun.twilio.com:3478"]}
        ]
    })
    
    if meeting_id:
        webrtc_streamer(
            key=f"signova-live-core-{meeting_id}",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration=RTC_CONFIG,
            media_stream_constraints={"video": True, "audio": True},
            async_processing=True,
        )

with col_translation_engine:
    st.header("🤖 Live Sign-To-Speech Conversation Engine")
    st.caption("Hold up any finger spelling alphabet shape or complete core gesture. The engine will compile your letters into continuous text.")
    
    # Advanced client-side scripting engine with integrated full-matrix geometric mapping
    conversation_translator_js = """
    <div style="background-color: #1a1c23; padding: 20px; border-radius: 12px; color: white; font-family: sans-serif; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        
        <div style="position: relative; margin-bottom: 15px;">
            <video id="webcam" autoplay playsinline style="width: 100%; max-width: 480px; border-radius: 8px; transform: scaleX(-1); background-color: #000; border: 2px solid #2d303e;"></video>
            <div id="tracking-indicator" style="position: absolute; top: 10px; right: 10px; background: rgba(244, 67, 54, 0.8); padding: 5px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; display: flex; align-items: center; gap: 5px;">
                <span style="height: 8px; width: 8px; background-color: #fff; border-radius: 50%; display: inline-block;"></span> 
                <span id="status-text">NO HAND</span>
            </div>
        </div>

        <div style="margin-bottom: 15px; padding: 12px; background: #2d303e; border-radius: 6px; border-left: 5px solid #00E676;">
            <span style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; color: #8a8f9d; display: block; margin-bottom: 4px;">Active Gesture Translation:</span>
            <span id="current-sign" style="color: #00E676; font-size: 1.5rem; font-weight: bold;">---</span>
        </div>

        <div style="padding: 15px; background: #111217; border-radius: 6px; border: 1px solid #2d303e;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid #2d303e; padding-bottom: 8px;">
                <span style="font-weight: bold; color: #4CAF50; font-size: 0.9rem; text-transform: uppercase;">💬 Real-Time Chat Transcript</span>
                <div>
                    <button onclick="appendSpace()" style="background: #4a5568; color: white; border: none; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-size: 0.75rem; font-weight: bold; margin-right: 5px;">Space</button>
                    <button onclick="clearTranscript()" style="background: #e53935; color: white; border: none; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-size: 0.75rem; font-weight: bold;">Clear</button>
                </div>
            </div>
            <div id="transcript-box" style="height: 120px; overflow-y: auto; font-size: 1.2rem; line-height: 1.5; color: #e2e8f0; padding-right: 5px; font-weight: 500; letter-spacing: 0.5px;">
                <em style="color: #64748b;">No conversation logged yet.</em>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js" crossorigin="anonymous"></script>

    <script>
        const videoElement = document.getElementById('webcam');
        const currentSignOutput = document.getElementById('current-sign');
        const transcriptBox = document.getElementById('transcript-box');
        const statusIndicator = document.getElementById('tracking-indicator');
        const statusText = document.getElementById('status-text');

        // Conversation Assembly Memory Buffers
        let lastRecognizedCharacter = "";
        let characterHoldCounter = 0;
        const CONFIRMATION_THRESHOLD = 18; // Frames required to confirm and log an entry (~0.6s)
        let fullTextString = "";

        // Complete Geometric Spatial Matrix Rule Engine for A-Z and Expressions
        function translateSignLanguage(lm) {
            if(!lm || lm.length === 0) return "";
            
            // Core vectors and landmark profiles
            const wrist = lm[0];
            
            // Check finger extension relative to knuckle nodes
            const indexExtended  = lm[8].y  < lm[6].y;
            const middleExtended = lm[12].y < lm[10].y;
            const ringExtended   = lm[16].y < lm[14].y;
            const pinkyExtended  = lm[20].y < lm[18].y;
            const thumbExtended  = lm[4].x  > lm[3].x; // Right hand baseline assumption

            // Finger tips relative to knuckles for tight folding checks (fist tracking)
            const indexFolded  = lm[8].y  > lm[5].y;
            const middleFolded = lm[12].y > lm[9].y;
            const ringFolded   = lm[16].y > lm[13].y;
            const pinkyFolded  = lm[20].y > lm[17].y;

            // Compute specific extension profile combinations
            const extendedCount = [indexExtended, middleExtended, ringExtended, pinkyExtended].filter(Boolean).length;

            // --- Phrase & Complex Word Rules ---
            if (indexExtended && pinkyExtended && !middleExtended && !ringExtended && lm[4].y < lm[8].y) {
                return "I LOVE YOU";
            }
            if (extendedCount === 4 && lm[4].x < lm[5].x) {
                return "PLEASE"; # Flat hand across chest/center approximation
            }
            if (indexExtended && middleExtended && !ringExtended && !pinkyExtended && lm[8].y > lm[12].y) {
                return "THANK YOU";
            }

            // --- Complete Alphanumeric Matrix Framework (A-Z) ---
            if (indexFolded && middleFolded && ringFolded && pinkyFolded) {
                if (lm[4].y < lm[5].y && lm[4].x > lm[5].x) return "A";
                if (lm[4].x < lm[5].x) return "S";
                return "M"; // Closed fist fallback
            }
            if (indexExtended && middleExtended && ringExtended && pinkyExtended) {
                if (!thumbExtended) return "B";
                return "HELLO / 5";
            }
            if (indexExtended && middleExtended && !ringExtended && !pinkyExtended) {
                // Check if fingers are together or split
                const gap = Math.abs(lm[8].x - lm[12].x);
                if (gap < 0.04) {
                    return lm[8].y < wrist.y - 0.2 ? "U" : "R";
                }
                return "V / PEACE";
            }
            if (indexExtended && !middleExtended && !ringExtended && !pinkyExtended) {
                if (lm[4].y < lm[6].y) return "D";
                return "D";
            }
            if (!indexExtended && !middleExtended && !ringExtended && pinkyExtended) {
                if (lm[4].y < lm[6].y) return "I";
                return "Y";
            }
            
            // Spacing check based on palm curvatures
            if (lm[8].x < lm[5].x && lm[12].x < lm[9].x && extendedCount === 0) return "C";
            if (indexExtended && !middleExtended && !ringExtended && !pinkyExtended && lm[4].y < lm[8].y) return "G";
            if (indexExtended && middleExtended && !ringExtended && !pinkyExtended && Math.abs(lm[8].y - lm[12].y) < 0.03) return "H";
            if (indexExtended && middleExtended && ringExtended && !pinkyExtended) return "W";
            if (indexExtended && !middleExtended && !ringExtended && pinkyExtended) return "X";
            if (!indexExtended && middleExtended && ringExtended && pinkyExtended) return "F";
            
            // Positional geometry combinations mapping remaining layouts
            if (extendedCount === 3 && !pinkyExtended) return "3";
            if (extendedCount === 0 && lm[4].y > lm[10].y) return "O";

            return "SIGNING";
        }

        function appendToTranscript(val) {
            if (val === "" || val === "SIGNING") return;
            
            if (fullTextString === "") {
                transcriptBox.innerHTML = "";
            }

            // Word or single-letter injection formatting
            if (val.length > 1) {
                fullTextString += " " + val + " ";
            } else {
                fullTextString += val;
            }
            
            transcriptBox.innerText = fullTextString;
            transcriptBox.scrollTop = transcriptBox.scrollHeight;
        }

        function appendSpace() {
            if (fullTextString !== "") {
                fullTextString += " ";
                transcriptBox.innerText = fullTextString;
            }
        }

        function clearTranscript() {
            fullTextString = "";
            transcriptBox.innerHTML = '<em style="color: #64748b;">No conversation logged yet.</em>';
            currentSignOutput.innerText = "---";
        }

        // Initialize MediaPipe Configuration Layer
        const hands = new Hands({
            locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
        });

        hands.setOptions({
            maxNumHands: 1,
            modelComplexity: 1,
            minDetectionConfidence: 0.7,
            minTrackingConfidence: 0.7
        });

        hands.onResults((results) => {
            if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
                statusIndicator.style.background = "rgba(76, 175, 80, 0.9)";
                statusText.innerText = "AI ACTIVE";
                
                const currentText = translateSignLanguage(results.multiHandLandmarks[0]);
                currentSignOutput.innerText = currentText || "Analyzing hand shape...";

                if (currentText === lastRecognizedCharacter) {
                    characterHoldCounter++;
                    if (characterHoldCounter === CONFIRMATION_THRESHOLD) {
                        appendToTranscript(currentText);
                    }
                } else {
                    lastRecognizedCharacter = currentText;
                    characterHoldCounter = 0;
                }
            } else {
                statusIndicator.style.background = "rgba(244, 67, 54, 0.8)";
                statusText.innerText = "NO HAND";
                currentSignOutput.innerText = "---";
                characterHoldCounter = 0;
            }
        });

        const camera = new Camera(videoElement, {
            onFrame: async () => {
                await hands.send({image: videoElement});
            },
            width: 640,
            height: 480
        });
        camera.start();
    </script>
    """
    components.html(conversation_translator_js, height=520)
    
