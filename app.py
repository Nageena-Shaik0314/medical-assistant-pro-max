import streamlit as st
from datetime import datetime
from gtts import gTTS
import os
from PIL import Image
import speech_recognition as sr
import tempfile
import re

st.set_page_config(page_title="Medical Assistant - Tiruvuru", layout="wide", page_icon="🏥")

st.markdown("""
<style>
.main-title {text-align:center; background:linear-gradient(90deg,#00C9FF,#92FE9D); padding:22px; border-radius:18px; color:#000; font-size:30px; font-weight:bold;}
.card {background:#1A1A1A; padding:18px; border-radius:16px; border-left:6px solid #00C9FF; margin:12px 0;}
.logo {font-size:42px; text-align:center;}
</style>
<div class='main-title'>🏥 MEDICAL ASSISTANT PRO MAX - TIRUVURU<br><small>🤖 Auto Language Detect | 🎤 Voice In & Out | 💊 30+ Symptoms</small></div>
""", unsafe_allow_html=True)
st.warning("⚠️ Educational Only - Consult Real Doctor at Tiruvuru Govt Hospital")

def speak_single(text, lang_code):
    try:
        tts = gTTS(text=text[:400], lang=lang_code, slow=False)
        tts.save("voice.mp3")
        with open("voice.mp3","rb") as f: st.audio(f.read(), format="audio/mp3", autoplay=True)
        os.remove("voice.mp3")
    except: st.error("Voice error")

def detect_language(text):
    # Telugu script
    if re.search(r'[\u0C00-\u0C7F]', text): return 'te'
    # Hindi script
    if re.search(r'[\u0900-\u097F]', text): return 'hi'
    # Telugu keywords
    telugu_words = ['jwaram','jalu','daggu','talanoppi','kadupu','nalam','emi','ela','naku','undi']
    hindi_words = ['bukhar','zukam','khansi','sir dard','pet dard','bukh','sardi','kya','mujhe','hai']
    txt = text.lower()
    if any(w in txt for w in telugu_words): return 'te'
    if any(w in txt for w in hindi_words): return 'hi'
    return 'en'

SYMPTOMS_DB = {
    "fever": ("Fever: Rest, 3L water, cold cloth, Dolo 650 after food, khichdi, coconut water. If 2 days go to Tiruvuru Hospital.", "జ్వరం: విశ్రాంతి, 3L నీరు, నుదుటిపై చల్లని గుడ్డ, డోలో 650, ఖిచ్డీ. 2 రోజులు ఉంటే తిరువూరు ఆసుపత్రి.", "बुखार: आराम, 3L पानी, ठंडा कपड़ा, डोलो 650। 2 दिन रहे तो अस्पताल।"),
    "jwaram": ("Fever: Rest, 3L water, Dolo 650.", "జ్వరం: విశ్రాంతి, 3L నీరు, డోలో 650.", "बुखार: आराम, 3L पानी।"),
    "cold": ("Cold: Steam 2 times, warm clothes, Cetzine night.", "జలుబు: ఆవిరి 2 సార్లు, వెచ్చని బట్టలు.", "जुकाम: भाप 2 बार।"),
    "cough": ("Cough: Salt gargle 3 times, honey ginger.", "దగ్గు: ఉప్పు నీటితో పుక్కిలింపు.", "खांसी: नमक पानी गरारे।"),
    "headache": ("Headache: Dark room, 8h sleep, Paracetamol.", "తలనొప్పి: చీకటి గది, 8గం నిద్ర.", "सिर दर्द: अंधेरा कमरा।"),
    "stomach": ("Stomach pain: No spicy, jeera water.", "కడుపు నొప్పి: కారం వద్దు.", "पेट दर्द: तीखा नहीं।"),
    "chest": ("Chest Pain EMERGENCY Call 108!", "ఛాతీ నొప్పి 108 కు కాల్!", "सीने में दर्द 108 कॉल!"),
    "bp": ("BP: Less salt, walk 30 min.", "బీపీ: ఉప్పు తగ్గించు.", "बीपी: नमक कम।"),
    "sugar": ("Sugar: No sugar, walk 30 min.", "షుగర్: చక్కెర వద్దు.", "शुगर: चीनी नहीं।"),
    "asthma": ("Asthma: Avoid dust, inhaler.", "ఆస్తమా: దుమ్ము వద్దు.", "अस्थमा: धूल से बचें।"),
    "allergy": ("Allergy: Avoid trigger, Cetzine.", "అలర్జీ: కారణం వద్దు.", "एलर्जी: बचें।"),
    "loose motion": ("Loose motion: ORS hourly.", "విరేచనాలు: ORS.", "दस्त: ORS।"),
    "vomiting": ("Vomiting: ORS, jeera water.", "వాంతులు: ORS.", "उल्टी: ORS।"),
    "back pain": ("Back pain: Hot compress, yoga.", "నడుము నొప్పి: వేడి కాపడం.", "कमर दर्द: सिकाई।"),
    "joint pain": ("Joint pain: Hot oil massage.", "కీళ్ల నొప్పి: నూనె మసాజ్.", "जोड़ों का दर्द: मालिश।"),
    "throat": ("Throat pain: Salt gargle.", "గొంతు నొప్పి: పుక్కిలింపు.", "गले में दर्द: गरारे।"),
    "skin rash": ("Skin rash: Coconut oil.", "చర్మ దద్దుర్లు: కొబ్బరి నూనె.", "चकत्ते: नारियल तेल।"),
    "eye pain": ("Eye pain: Cold wash.", "కంటి నొప్పి: చల్లని నీరు.", "आंख दर्द: ठंडा पानी।"),
    "tooth pain": ("Tooth pain: Salt rinse, clove.", "పంటి నొప్పి: లవంగం.", "दांत दर्द: लौंग।"),
    "dizziness": ("Dizziness: Sit, water.", "తల తిరగడం: కూర్చో.", "चक्कर: बैठें।"),
    "weakness": ("Weakness: ORS, fruits.", "నీరసం: ORS.", "कमजोरी: फल।"),
    "constipation": ("Constipation: 3L water, papaya.", "మలబద్ధకం: 3L నీరు.", "कब्ज: पानी।"),
    "urine burning": ("Urine burning: 4L water.", "మూత్రంలో మంట: 4L నీరు.", "पेशाब जलन: 4L पानी।"),
    "cut": ("Cut: Dettol, Band-Aid.", "కోత: డెట్టాల్.", "कट: डेटॉल।"),
    "burn": ("Burn: Cold water 10 min.", "కాలిన: చల్లని నీరు.", "जलना: ठंडा पानी।"),
    "dog bite": ("Dog Bite: Wash 15 min, Hospital!", "కుక్క కాటు: కడుగు, ఆసుపత్రి!", "कुत्ता: धोएं, अस्पताल!"),
    "snake bite": ("Snake Bite: 108 call FAST!", "పాము కాటు: 108 కాల్!", "सांप: 108 कॉल!"),
    "bleeding": ("Bleeding: Press cotton.", "రక్తస్రావం: దూది.", "खून: रुई।"),
}

def get_reply(q):
    ql = q.lower()
    for k in SYMPTOMS_DB:
        if k in ql: return SYMPTOMS_DB[k]
    return (f"For {q}: Rest, 3L water, 8h sleep. Tiruvuru Hospital if 2 days.", f"{q} కోసం: విశ్రాంతి, 3L నీరు, 8గం నిద్ర.", f"{q} के लिए: आराम, 3L पानी।")

feature = st.sidebar.selectbox("📋 SELECT",["🎤 🤖 AI Chatbot 24/7","💊 Medicine Info","🧘 Health Tips & Yoga","🚨 Emergency 108","📸 Image Analyzer"])

if feature == "🎤 🤖 AI Chatbot 24/7":
    st.markdown("<div class='card'><div class='logo'>🎤🤖</div><h3 style='text-align:center;'>Auto Language Detect - Same Language Reply</h3><p style='text-align:center'>Telugu lo adigithe Telugu lone, Hindi lo adigithe Hindi lone, English lo adigithe English lone!</p></div>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        st.write("### 🎤 Speak → Same Language Voice")
        user_audio = st.audio_input("🎤 Mic click & speak in any language...")
        if user_audio:
            st.audio(user_audio)
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    tmp.write(user_audio.getbuffer()); tmp_path = tmp.name
                r = sr.Recognizer()
                with sr.AudioFile(tmp_path) as source:
                    audio_data = r.record(source)
                    # Try all 3 languages auto
                    try: text = r.recognize_google(audio_data, language='te-IN')
                    except:
                        try: text = r.recognize_google(audio_data, language='hi-IN')
                        except: text = r.recognize_google(audio_data, language='en-IN')
                os.remove(tmp_path)
                lang = detect_language(text)
                st.success(f"✅ You said: **{text}** | Detected: **{lang.upper()}**")
                eng,tel,hin = get_reply(text)
                if lang=='te':
                    st.chat_message("assistant").write(f"**తెలుగు:** {tel}")
                    speak_single(tel,'te')
                elif lang=='hi':
                    st.chat_message("assistant").write(f"**हिंदी:** {hin}")
                    speak_single(hin,'hi')
                else:
                    st.chat_message("assistant").write(f"**English:** {eng}")
                    speak_single(eng,'en')
            except: st.warning("Clear ga cheppu!")
    with c2:
        st.write("### ⌨️ Type → Same Language Text")
        st.caption("Try: jwaram / bukhar / fever / జ్వరం / बुखार")
        q = st.chat_input("Type in any language...")
        if q:
            lang = detect_language(q)
            st.chat_message("user").write(f"You ({lang.upper()}): {q}")
            eng,tel,hin = get_reply(q)
            if lang=='te':
                st.chat_message("assistant").write(f"**తెలుగు:** {tel}")
                speak_single(tel,'te')
            elif lang=='hi':
                st.chat_message("assistant").write(f"**हिंदी:** {hin}")
                speak_single(hin,'hi')
            else:
                st.chat_message("assistant").write(f"**English:** {eng}")
                speak_single(eng,'en')
            st.download_button("📄 Download", data=f"{eng}\n{tel}\n{hin}", file_name="Prescription.txt")

elif feature == "💊 Medicine Info":
    st.subheader("💊 Medicine Info - Auto Language")
    q = st.text_input("Medicine name in any language")
    if q:
        lang = detect_language(q)
        eng,tel,hin = get_reply(q)
        if lang=='te': st.write(tel); speak_single(tel,'te')
        elif lang=='hi': st.write(hin); speak_single(hin,'hi')
        else: st.write(eng); speak_single(eng,'en')

elif feature == "🧘 Health Tips & Yoga":
    st.subheader("🧘 Health Tips - Auto Language")
    q = st.text_input("Ask health tip in any language")
    if q:
        lang = detect_language(q)
        if lang=='te': speak_single("30 నిమి నడక, 15 నిమి యోగా", 'te')
        elif lang=='hi': speak_single("30 मिनट पैदल, 15 मिनट योगा", 'hi')
        else: speak_single("Walk 30 min, Yoga 15 min", 'en')

elif feature == "🚨 Emergency 108":
    st.error("🚨 108 - Auto language emergency voice")
    if st.button("🔊 108 Voice"):
        st.write("Will speak in your detected language")

elif feature == "📸 Image Analyzer":
    st.subheader("📸 Image Analyzer")
    img = st.file_uploader("Upload", type=["jpg","png","jpeg"])
    if img: st.image(Image.open(img), use_column_width=True)
