import streamlit as st
from gtts import gTTS
import os, re, tempfile
import speech_recognition as sr

st.set_page_config(page_title="AI Medical Assistant App", page_icon="🏥", layout="wide")

# ===== ONLY ONE HEADING - AI MEDICAL ASSISTANT APP =====
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
        "te": "Namaste garu, meeku jwaram vachindani telisindi. Dayachesi bhayapadakandi. Dolo 650 tablet bhojanam tarvata vesukondi. Precautions: 1. 2 rojulu vishranti 2. Nuvvutipa pai challani gudda 3. Challa neetitho snanam vaddu 4. Mask pettukondi 5. 3-4L neeru, kobbari neeru 6. Fan kindha direct ga vaddu 7. Mandu share cheyakandi 8. Vomits unte hospital ki randi. Aharam: Khichdi, kobbari neeru. 2 rojula tarvata thagakapotey Tiruvuru Govt Hospital ki randi garu.",
        "hi": "Namaste, aapko bukhar hai. Dolo 650 khane ke baad 2 baar. Precautions: 1. 2 din aaram 2. Maathe par thanda patti 3. Thande pani se nahana nahi 4. Mask pehniye 5. 3-4L pani 6. Direct fan me nahi 7. Dawai share nahi 8. Ulti ho to hospital. 2 din me thik na ho to Tiruvuru hospital aaiye.",
        "en": "Namaste, you have fever. Please take Dolo 650 after food 2 times. Precautions: 1. 2 days complete rest 2. Cold cloth on forehead every 2 hours 3. No cold water bath 4. Wear mask 5. 3-4L water, coconut water 6. No direct fan 7. Don't share medicine 8. If vomiting, visit hospital. Diet: Khichdi, coconut water. If not reduced in 2 days visit Tiruvuru Govt Hospital."
    },
    "cold": {
        "te": "Namaste garu, meeku jalubu. Cetzine rathri 1, Vicks rasukondi. Precautions: 1. Roju 2 sarlu aaviri 2. Vecchani battalu 3. Challa neeru, ice cream 5 rojulu vaddu 4. Dust, fan direct vaddu 5. Rumal tho nose clean 6. Pillala daggara ki vellakandi 7. Goruvecchi neeru mathrame 8. Thummu vachinappudu chethi addupettukondi. 5 rojula kanna ekkuva unte hospital ki randi.",
        "hi": "Namaste, aapko zukam hai. Cetzine raat me, Vicks lagaiye. Precautions: 1. Din me 2 baar bhaap 2. Garam kapde 3. Thanda pani 5 din nahi 4. Dhool se bachiye 5. Rumaal use kijiye 6. Bacchon se doori 7. Garam pani 8. Cheenk me haath aage. 5 din se zyada ho to hospital aaiye.",
        "en": "Namaste, you have cold. Cetzine at night, Vicks on chest. Precautions: 1. Steam 2 times 2. Warm clothes 3. No cold water, ice cream 5 days 4. Avoid dust, direct fan 5. Use handkerchief 6. Keep distance from kids 7. Only warm water 8. Cover mouth when sneezing. If more than 5 days visit hospital."
    },
}

def get_reply(q):
    ql = q.lower()
    for k in SYMPTOMS_DB:
        if k in ql:
            d = SYMPTOMS_DB[k]
            return d["en"], d["te"], d["hi"]
    return (
        f"Namaste, you have {q}. Take rest, 3L water, 8h sleep, light food. Precautions: Avoid cold, oily, spicy, outside food, smoking, alcohol, wear mask, wash hands. If 2 days not reducing visit Tiruvuru Hospital.",
        f"Namaste garu, meeku {q} undani telisindi. Vishranti, 3L neeru, 8 gantalu nidra, thelikaina aharam. Precautions: Challa neeru, noone, karam, bayata food, smoking, alcohol vaddu, mask pettukondi, chethulu kadukondi. 2 rojula tarvata hospital ki randi.",
        f"Namaste, aapko {q} hai. Aaram, 3L pani, 8 ghante neend, halka bhojan. Precautions: Thanda, tel masala, bahar ka khana, smoking, alcohol avoid, mask pehniye, haath dhoiye. 2 din me thik na ho to hospital jaiye."
    )

# ===== CLEAN UI - ONLY ENGLISH LABELS =====
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
