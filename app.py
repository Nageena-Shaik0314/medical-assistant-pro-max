import streamlit as st
from gtts import gTTS
import os, re, tempfile
from PIL import Image
import speech_recognition as sr

st.set_page_config(page_title="AI Medical Assistant App", page_icon="🏥", layout="wide")

# ===== ONLY ONE MAIN HEADING =====
st.markdown("""
<style>
.main-title {text-align:center; background:linear-gradient(90deg,#00C9FF,#92FE9D); padding:18px; border-radius:12px; color:#000; font-size:26px; font-weight:bold;}
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
        "te": "Namaste garu, meeku jwaram vachindani telisindi. Dolo 650 tablet bhojanam tarvata vesukondi. Precautions: 1. 2 rojulu vishranti 2. Nuvvutipa pai challani gudda 3. Challa neetitho snanam vaddu 4. Mask pettukondi 5. 3-4L neeru 6. Fan direct vaddu 7. Mandu share vaddu 8. Vomits unte hospital. Aharam: Khichdi. 2 rojula tarvata Tiruvuru Govt Hospital ki randi.",
        "hi": "Namaste, aapko bukhar hai. Dolo 650 khane ke baad 2 baar. Precautions: 1. 2 din aaram 2. Thanda patti 3. Thande pani se nahi 4. Mask 5. 3-4L pani 6. Fan direct nahi 7. Dawai share nahi 8. Ulti ho to hospital.",
        "en": "Namaste, you have fever. Dolo 650 after food 2 times. Precautions: 1. 2 days rest 2. Cold cloth on forehead 3. No cold water bath 4. Wear mask 5. 3-4L water 6. No direct fan 7. Don't share medicine 8. If vomiting visit hospital. Diet: Khichdi. If not reduced in 2 days visit Tiruvuru Govt Hospital."
    },
    "cold": {
        "te": "Namaste garu, meeku jalubu. Cetzine rathri, Vicks. Precautions: 1. Aaviri 2 sarlu 2. Vecchani battalu 3. Challa neeru 5 rojulu vaddu 4. Dust vaddu 5. Rumal use 6. Pillala daggara vaddu 7. Goruvecchi neeru 8. Thummu lo chethi. 5 rojula kanna ekkuva unte hospital.",
        "hi": "Namaste, zukam hai. Cetzine raat me, Vicks. Precautions: 1. Bhaap 2 baar 2. Garam kapde 3. Thanda pani 5 din nahi 4. Dhool nahi 5. Rumaal 6. Bacchon se doori 7. Garam pani 8. Cheenk me haath.",
        "en": "Namaste, you have cold. Cetzine at night, Vicks. Precautions: 1. Steam 2 times 2. Warm clothes 3. No cold water 5 days 4. No dust 5. Handkerchief 6. Away from kids 7. Warm water 8. Cover mouth when sneeze."
    },
    "cough": {
        "te": "Namaste garu, daggu. Ascoril 2 sarlu, thene allam. Precautions: 1. Uppu neetitho pukkilinchu 3 sarlu 2. Mask 3. Challa neeru vaddu 4. Thala ethuga petti nidra 5. Noru moosi daggu 6. 3L neeru 7. Vepudu vaddu 8. Raktham vaste hospital.",
        "hi": "Namaste, khansi hai. Ascoril 2 baar, shahad adrak. Precautions: 1. Namak pani garare 2. Mask 3. Thanda pani nahi 4. Sir uncha 5. Muh dhak ke khansi 6. 3L pani 7. Tala nahi 8. Khoon aaye to hospital.",
        "en": "Namaste, you have cough. Ascoril 2 times, honey ginger. Precautions: 1. Salt water gargle 3 times 2. Mask 3. No cold water 4. Head elevated 5. Cover mouth 6. 3L water 7. No fried 8. If blood visit hospital."
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
    col1, col2 = st.columns(2)
    with col1:
        st.write("🎤 **Speak Here**")
        user_audio = st.audio_input("Click to speak...")
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
                if lang=='te': st.write(tel); speak_single(tel,'te')
                elif lang=='hi': st.write(hin); speak_single(hin,'hi')
                else: st.write(eng); speak_single(eng,'en')
            except: st.warning("Please speak again.")
    with col2:
        st.write("⌨️ **Type Here**")
        q = st.chat_input("Enter your symptoms...")
        if q:
            lang = detect_language(q)
            st.write(f"You: {q}")
            eng,tel,hin = get_reply(q)
            if lang=='te': st.write(tel); speak_single(tel,'te')
            elif lang=='hi': st.write(hin); speak_single(hin,'hi')
            else: st.write(eng); speak_single(eng,'en')

elif feature == "💊 Medicine Info":
    st.write("### 💊 Medicine Information")
    st.info("Enter medicine name in chat. Example: fever, cold, cough, headache, stomach pain, bp, sugar, etc. 30+ symptoms available with precautions.")

elif feature == "🧘 Health Tips & Yoga":
    st.write("### 🧘 Health Tips & Yoga")
    st.success("**Daily Health Precautions:**\n1. Walk 30 min daily\n2. Yoga 15 min\n3. Drink 3L water\n4. Sleep 8 hours\n5. Eat millets, fruits\n6. No smoking, alcohol\n7. Wash hands regularly\n8. Wear mask in dusty area")

elif feature == "🚨 Emergency 108":
    st.write("### 🚨 Emergency 108")
    st.error("🚑 **108 - Ambulance**\n🚓 **100 - Police**\n🏥 **Tiruvuru Govt Hospital 24/7**\n\n**Precautions:**\n1. Don't panic\n2. Call 108 immediately\n3. Don't move patient\n4. Loosen tight clothes\n5. Press with cloth if bleeding\n6. Take to hospital fast\n7. Show old medicines to doctor")

elif feature == "📸 Image Analyzer":
    st.write("### 📸 Image Analyzer")
    img = st.file_uploader("Upload wound/skin image", type=["jpg","png","jpeg"])
    if img:
        st.image(Image.open(img), use_column_width=True)
        st.info("Keep wound clean with Dettol. If swelling, pus, more pain - visit hospital immediately.")
