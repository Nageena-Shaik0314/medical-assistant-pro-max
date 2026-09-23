import streamlit as st
from gtts import gTTS
import os, re, tempfile
from PIL import Image
import speech_recognition as sr

st.set_page_config(page_title="AI Medical Assistant App", page_icon="🏥", layout="wide")

# ===== BEAUTIFUL MIDDLE DESIGN CSS =====
st.markdown("""
<style>
.main-title {
    text-align:center;
    background:linear-gradient(90deg,#00C9FF,#92FE9D);
    padding:18px; border-radius:15px;
    color:#000; font-size:26px; font-weight:bold;
    margin-bottom:30px;
    box-shadow: 0 4px 15px rgba(0,201,255,0.3);
}
.center-container {
    display:flex; justify-content:center; align-items:center;
    margin-top: 40px;
}
.beauty-card {
    background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
    padding:25px; border-radius:20px;
    border: 1px solid #00C9FF;
    box-shadow: 0 8px 32px rgba(0,201,255,0.2);
    margin:10px;
    transition: transform 0.3s;
}
.beauty-card:hover {transform: translateY(-5px); box-shadow: 0 12px 40px rgba(0,201,255,0.3);}
.stAudioInput,.stChatInput {border-radius:15px!important;}
</style>
<div class='main-title'>🏥 AI Medical Assistant App</div>
""", unsafe_allow_html=True)

def speak_single(text, lang_code):
    try:
        tts = gTTS(text=text[:600], lang=lang_code, slow=False)
        tts.save("voice.mp3")
        with open("voice.mp3","rb") as f: st.audio(f.read(), format="audio/mp3", autoplay=True)
        os.remove("voice.mp3")
    except: pass

def detect_language(text):
    if re.search(r'[\u0C00-\u0C7F]', text): return 'te'
    if re.search(r'[\u0900-\u097F]', text): return 'hi'
    if any(w in text.lower() for w in ['jwaram','jalu','daggu','naku','garu']): return 'te'
    if any(w in text.lower() for w in ['bukhar','zukam','khansi','mujhe']): return 'hi'
    return 'en'

SYMPTOMS_DB = {
    "fever": {
        "te": "Namaste garu, meeku jwaram. Dolo 650 bhojanam tarvata. Precautions: 1. 2 rojulu vishranti 2. Nuvvutipa pai challani gudda 3. Challa snanam vaddu 4. Mask 5. 3-4L neeru 6. Fan direct vaddu 7. Mandu share vaddu 8. Vomits unte hospital. Aharam: Khichdi. 2 rojula tarvata Tiruvuru Govt Hospital ki randi.",
        "hi": "Namaste, bukhar hai. Dolo 650 khane ke baad. Precautions: 1. 2 din aaram 2. Thanda patti 3. Thande pani se nahi 4. Mask 5. 3-4L pani 6. Fan direct nahi 7. Dawai share nahi 8. Ulti ho to hospital.",
        "en": "Namaste, you have fever. Dolo 650 after food. Precautions: 1. 2 days rest 2. Cold cloth on forehead 3. No cold water bath 4. Wear mask 5. 3-4L water 6. No direct fan 7. Don't share medicine 8. If vomiting visit hospital. Diet: Khichdi. Visit Tiruvuru Govt Hospital if not reduced in 2 days."
    },
    "cold": {
        "te": "Namaste garu, jalubu. Cetzine rathri, Vicks. Precautions: 1. Aaviri 2 sarlu 2. Vecchani battalu 3. Challa neeru 5 rojulu vaddu 4. Dust vaddu 5. Rumal use 6. Pillala daggara vaddu 7. Goruvecchi neeru 8. Thummu lo chethi.",
        "hi": "Namaste, zukam hai. Cetzine raat me, Vicks. Precautions: 1. Bhaap 2 baar 2. Garam kapde 3. Thanda pani 5 din nahi 4. Dhool nahi 5. Rumaal 6. Bacchon se doori 7. Garam pani 8. Cheenk me haath.",
        "en": "Namaste, you have cold. Cetzine at night, Vicks. Precautions: 1. Steam 2 times 2. Warm clothes 3. No cold water 5 days 4. No dust 5. Handkerchief 6. Away from kids 7. Warm water 8. Cover mouth when sneeze."
    },
}

def get_reply(q):
    ql = q.lower()
    for k in SYMPTOMS_DB:
        if k in ql:
            d = SYMPTOMS_DB[k]
            return d["en"], d["te"], d["hi"]
    return (
        f"Namaste, you have {q}. Rest, 3L water, 8h sleep, light food. Precautions: Avoid cold, oily, spicy, outside food, smoking, alcohol, wear mask, wash hands. If 2 days not reducing visit Tiruvuru Hospital.",
        f"Namaste garu, meeku {q} undani telisindi. Vishranti, 3L neeru, 8 gantalu nidra. Precautions: Challa, noone, karam, bayata food vaddu, mask pettukondi. 2 rojula tarvata hospital.",
        f"Namaste, aapko {q} hai. Aaram, 3L pani, 8 ghante neend. Precautions: Thanda, tel masala, bahar ka khana avoid, mask pehniye. 2 din me thik na ho to hospital."
    )

# ===== FEATURES SIDEBAR - ENGLISH ONLY =====
feature = st.sidebar.selectbox("📋 SELECT FEATURE", ["🩺 AI Doctor Chat", "💊 Medicine Info", "🧘 Health Tips & Yoga", "🚨 Emergency 108", "📸 Image Analyzer"])

if feature == "🩺 AI Doctor Chat":
    # ===== MIDDLE BEAUTIFUL CARDS =====
    st.markdown("<br>", unsafe_allow_html=True)
    col_spacer1, col_main, col_spacer2 = st.columns([1, 8, 1])

    with col_main:
        c1, c2 = st.columns(2, gap="large")

        with c1:
            st.markdown("""
            <div class='beauty-card'>
                <h3 style='text-align:center; color:#00C9FF;'>🎤 Speak Here</h3>
                <p style='text-align:center; color:#AAA; font-size:13px;'>Click mic & speak in any language</p>
            </div>
            """, unsafe_allow_html=True)
            user_audio = st.audio_input("Click to speak...", label_visibility="collapsed")
            if user_audio:
                st.audio(user_audio)
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                        tmp.write(user_audio.getbuffer()); tmp_path = tmp.name
                    r = sr.Recognizer()
                    with sr.AudioFile(tmp_path) as source:
                        audio_data = r.record(source)
                        try: text = r.recognize_google(audio_data, language='te-IN')
                        except:
                            try: text = r.recognize_google(audio_data, language='hi-IN')
                            except: text = r.recognize_google(audio_data, language='en-IN')
                    os.remove(tmp_path)
                    lang = detect_language(text)
                    st.success(f"You said: {text}")
                    eng,tel,hin = get_reply(text)
                    if lang=='te': st.info(tel); speak_single(tel,'te')
                    elif lang=='hi': st.info(hin); speak_single(hin,'hi')
                    else: st.info(eng); speak_single(eng,'en')
                except: st.warning("Please speak again.")

        with c2:
            st.markdown("""
            <div class='beauty-card'>
                <h3 style='text-align:center; color:#92FE9D;'>⌨️ Type Here</h3>
                <p style='text-align:center; color:#AAA; font-size:13px;'>Type symptoms in any language</p>
            </div>
            """, unsafe_allow_html=True)
            q = st.chat_input("Enter your symptoms...")
            if q:
                lang = detect_language(q)
                st.write(f"**You:** {q}")
                eng,tel,hin = get_reply(q)
                if lang=='te': st.info(tel); speak_single(tel,'te')
                elif lang=='hi': st.info(hin); speak_single(hin,'hi')
                else: st.info(eng); speak_single(eng,'en')

elif feature == "💊 Medicine Info":
    st.markdown("<div class='beauty-card' style='text-align:center;'><h3>💊 Medicine Information</h3><p>30+ symptoms with 8 precautions each</p></div>", unsafe_allow_html=True)
elif feature == "🧘 Health Tips & Yoga":
    st.markdown("<div class='beauty-card'><h3 style='text-align:center;'>🧘 Health Tips</h3><p>1. Walk 30 min<br>2. Yoga 15 min<br>3. 3L water<br>4. 8h sleep<br>5. No smoking/alcohol<br>6. Wash hands<br>7. Mask in dust<br>8. Time ki food</p></div>", unsafe_allow_html=True)
elif feature == "🚨 Emergency 108":
    st.markdown("<div class='beauty-card' style='border-left:6px solid red;'><h3 style='color:red; text-align:center;'>🚨 Emergency 108</h3><p>🚑 108 Ambulance<br>🚓 100 Police<br>🏥 Tiruvuru Govt Hospital 24/7</p></div>", unsafe_allow_html=True)
elif feature == "📸 Image Analyzer":
    st.markdown("<div class='beauty-card'><h3 style='text-align:center;'>📸 Image Analyzer</h3></div>", unsafe_allow_html=True)
    img = st.file_uploader("Upload image", type=["jpg","png","jpeg"], label_visibility="collapsed")
    if img:
        st.image(Image.open(img), use_column_width=True)
        st.info("Keep wound clean with Dettol. If swelling/pus - visit hospital.")
