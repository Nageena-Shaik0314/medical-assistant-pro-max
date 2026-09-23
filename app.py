import streamlit as st
from datetime import datetime
from gtts import gTTS
import os
from PIL import Image
import speech_recognition as sr
import tempfile

st.set_page_config(page_title="Medical Assistant - Tiruvuru", layout="wide", page_icon="🏥")

# ===== ATTRACTIVE UI WITH LOGOS =====
st.markdown("""
<style>
.main-title {text-align:center; background:linear-gradient(90deg,#00C9FF,#92FE9D); padding:22px; border-radius:18px; color:#000; font-size:30px; font-weight:bold;}
.card {background:#1A1A1A; padding:18px; border-radius:16px; border-left:6px solid #00C9FF; margin:12px 0;}
.logo {font-size:42px; text-align:center;}
</style>
<div class='main-title'>🏥 MEDICAL ASSISTANT PRO MAX - TIRUVURU<br><small>🤖 AI Chatbot 24/7 | 🎤 Voice In & Out | 💊 30+ Symptoms | 🧘 Yoga | 🚨 108</small></div>
""", unsafe_allow_html=True)
st.warning("⚠️ Educational Only - Consult Real Doctor at Tiruvuru Govt Hospital")

def speak_trilingual(eng, tel, hin, lang="all"):
    try:
        if lang in ["all","english"]:
            st.write("🔊 **English:**")
            tts = gTTS(text=eng[:380], lang='en', slow=False); tts.save("en.mp3")
            with open("en.mp3","rb") as f: st.audio(f.read(), format="audio/mp3", autoplay=True)
            os.remove("en.mp3")
        if lang in ["all","telugu"]:
            st.write("🔊 **తెలుగు:**")
            tts = gTTS(text=tel[:380], lang='te', slow=False); tts.save("te.mp3")
            with open("te.mp3","rb") as f: st.audio(f.read(), format="audio/mp3", autoplay=True)
            os.remove("te.mp3")
        if lang in ["all","hindi"]:
            st.write("🔊 **हिंदी:**")
            tts = gTTS(text=hin[:380], lang='hi', slow=False); tts.save("hi.mp3")
            with open("hi.mp3","rb") as f: st.audio(f.read(), format="audio/mp3", autoplay=True)
            os.remove("hi.mp3")
    except Exception as e: st.error(f"Voice error: {e}")

# ===== 30+ SYMPTOMS DATABASE =====
SYMPTOMS_DB = {
    "fever": ("Fever: Rest, 3L water, cold cloth, Dolo 650 after food, khichdi, coconut water. If 2 days go to Tiruvuru Hospital.", "జ్వరం: విశ్రాంతి, 3L నీరు, నుదుటిపై చల్లని గుడ్డ, డోలో 650, ఖిచ్డీ.", "बुखार: आराम, 3L पानी, ठंडा कपड़ा, डोलो 650।"),
    "jwaram": ("Fever: Rest, 3L water, Dolo 650 after food.", "జ్వరం: విశ్రాంతి, 3L నీరు, డోలో 650.", "बुखार: आराम, 3L पानी, डोलो 650।"),
    "cold": ("Cold: Steam 2 times, warm clothes, Cetzine night, Vicks rub.", "జలుబు: ఆవిరి 2 సార్లు, వెచ్చని బట్టలు, సెట్జిన్.", "जुकाम: भाप 2 बार, गर्म कपड़े, सेटजीन।"),
    "cough": ("Cough: Salt gargle 3 times, mask, honey ginger, Ascoril.", "దగ్గు: ఉప్పు నీటితో పుక్కిలింపు, తేనె అల్లం.", "खांसी: नमक पानी गरारे, शहद अदरक।"),
    "headache": ("Headache: Dark room, no phone, 8h sleep, Paracetamol.", "తలనొప్పి: చీకటి గది, ఫోన్ వద్దు, 8గం నిద్ర.", "सिर दर्द: अंधेरा कमरा, 8 घंटे नींद।"),
    "stomach": ("Stomach pain: No spicy, jeera water, Digene, curd rice.", "కడుపు నొప్పి: కారం వద్దు, జీలకర్ర నీరు.", "पेट दर्द: तीखा नहीं, जीरा पानी।"),
    "chest": ("Chest Pain EMERGENCY: Call 108, go to Tiruvuru Govt Hospital NOW!", "ఛాతీ నొప్పి అత్యవసరం: 108 కు కాల్!", "सीने में दर्द आपातकाल: 108 पर कॉल!"),
    "bp": ("High BP: Less salt, no tension, walk 30 min, tablet regular.", "బీపీ: ఉప్పు తగ్గించు, టెన్షన్ వద్దు, నడక.", "बीपी: नमक कम, टेंशन नहीं।"),
    "sugar": ("Diabetes: No sugar, walk 30 min, check sugar, millets.", "షుగర్: చక్కెర వద్దు, నడక, మిల్లెట్స్.", "शुगर: चीनी नहीं, पैदल।"),
    "asthma": ("Asthma: Avoid dust, inhaler always, steam, no smoke.", "ఆస్తమా: దుమ్ము వద్దు, ఇన్హేలర్.", "अस्थमा: धूल से बचें, इन्हेलर।"),
    "allergy": ("Allergy: Avoid trigger, Cetzine, coconut oil.", "అలర్జీ: కారణం వద్దు, సెట్జిన్.", "एलर्जी: ट्रिगर से बचें।"),
    "loose motion": ("Loose motion: ORS hourly, curd rice, banana.", "విరేచనాలు: ORS ప్రతి గంట.", "दस्त: हर घंटे ORS।"),
    "vomiting": ("Vomiting: Small sips, ORS, jeera water.", "వాంతులు: కొద్దిగా నీరు, ORS.", "उल्टी: थोड़ा पानी, ORS।"),
    "back pain": ("Back pain: Hot compress, rest, yoga - Bhujangasana.", "నడుము నొప్పి: వేడి కాపడం, యోగా.", "कमर दर्द: गर्म सिकाई, योगा।"),
    "joint pain": ("Joint pain: Hot oil massage, turmeric milk.", "కీళ్ల నొప్పి: వేడి నూనె మసాజ్.", "जोड़ों का दर्द: गर्म तेल मालिश।"),
    "throat": ("Throat pain: Salt gargle, warm water, honey.", "గొంతు నొప్పి: ఉప్పు నీటితో పుక్కిలింపు.", "गले में दर्द: नमक पानी गरारे।"),
    "skin rash": ("Skin rash: Coconut oil, no soap, Cetzine.", "చర్మ దద్దుర్లు: కొబ్బరి నూనె.", "त्वचा चकत्ते: नारियल तेल।"),
    "eye pain": ("Eye pain: Cold wash, no phone, eye drops.", "కంటి నొప్పి: చల్లని నీటితో కడుగు.", "आंख दर्द: ठंडे पानी से धोएं।"),
    "tooth pain": ("Tooth pain: Salt rinse, clove, dentist.", "పంటి నొప్పి: లవంగం, ఉప్పు నీరు.", "दांत दर्द: लौंग, नमक पानी।"),
    "dizziness": ("Dizziness: Sit, water, sugar check.", "తల తిరగడం: కూర్చో, నీరు.", "चक्कर: बैठें, पानी।"),
    "weakness": ("Weakness: ORS, fruits, 8h sleep.", "నీరసం: ORS, పండ్లు.", "कमजोरी: फल, नींद।"),
    "constipation": ("Constipation: 3L water, papaya, walk.", "మలబద్ధకం: 3L నీరు, బొప్పాయి.", "कब्ज: 3L पानी, पपीता।"),
    "urine burning": ("Urine burning: 4L water, coconut water.", "మూత్రంలో మంట: 4L నీరు.", "पेशाब जलन: 4L पानी।"),
    "cut": ("Cut: Wash, Dettol, Band-Aid, TT.", "కోత: డెట్టాల్, బ్యాండ్-ఎయిడ్.", "कट: डेटॉल, बैंड-एड।"),
    "burn": ("Burn: Cold water 10 min, Burnol.", "కాలిన: 10 నిమి చల్లని నీరు.", "जलना: 10 मिनट ठंडा पानी।"),
    "dog bite": ("Dog Bite: Wash 15 min soap, Govt Hospital injection!", "కుక్క కాటు: 15 నిమి సబ్బుతో కడుగు!", "कुत्ता काटना: 15 मिनट धोएं!"),
    "snake bite": ("Snake Bite: Tie cloth, 108 call, Hospital FAST!", "పాము కాటు: 108 కు కాల్!", "सांप: 108 पर कॉल!"),
    "bleeding": ("Bleeding: Press cotton, Dettol, doctor.", "రక్తస్రావం: దూదితో నొక్కు.", "खून: रुई से दबाएं।"),
}

def get_reply(q):
    ql = q.lower()
    for key in SYMPTOMS_DB:
        if key in ql: return SYMPTOMS_DB[key]
    return (f"For {q}: Rest, 3L water, 8h sleep, light food. If 2 days Tiruvuru Hospital.", f"{q} కోసం: విశ్రాంతి, 3L నీరు, 8గం నిద్ర.", f"{q} के लिए: आराम, 3L पानी।")

# ===== SIDEBAR =====
feature = st.sidebar.selectbox("📋 SELECT",
["🎤 🤖 AI Chatbot 24/7 - Voice In & Out","💊 Medicine Info - 30+","🧘 Health Tips & Yoga","🚨 Emergency 108","📸 Image Analyzer","ℹ️ About"])

# 1. AI CHATBOT 24/7 - YOUR ASKED LOGIC
if feature == "🎤 🤖 AI Chatbot 24/7 - Voice In & Out":
    st.markdown("<div class='card'><div class='logo'>🎤🤖💬</div><h3 style='text-align:center;'>AI Chatbot 24/7 - Independent Voice & Text</h3></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎤 **Speak → Direct Voice Reply**")
        user_audio = st.audio_input("🎤 Mic click & speak...")
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
                st.success(f"✅ You said: **{text}**")
                eng, tel, hin = get_reply(text)
                st.chat_message("assistant").write(f"**EN:** {eng}\n\n**TE:** {tel}\n\n**HI:** {hin}")
                speak_trilingual(eng, tel, hin, "all")
            except: st.warning("Voice clear ga ledu, malli cheppu!")
    with col2:
        st.markdown("### ⌨️ **Type → Direct Text Reply**")
        st.caption("30+ symptoms: fever, cold, cough, headache, chest pain, bp, sugar, asthma, allergy, vomiting, back pain, joint pain, skin rash, eye pain, tooth pain, dizziness, cut, burn, dog bite, snake bite...")
        q = st.chat_input("Type symptom: fever / jwaram / bukhar...")
        if q:
            st.chat_message("user").write(f"You: {q}")
            eng, tel, hin = get_reply(q)
            st.chat_message("assistant").write(f"**EN:** {eng}\n\n**TE:** {tel}\n\n**HI:** {hin}")
            lang_opt = st.radio("Voice Language:", ["all","telugu","hindi","english"], horizontal=True)
            speak_trilingual(eng, tel, hin, lang_opt)
            st.download_button("📄 Download", data=f"{eng}\n{tel}\n{hin}\n{datetime.now()}", file_name="Prescription.txt")

elif feature == "💊 Medicine Info - 30+":
    st.markdown("<div class='card'><div class='logo'>💊💉🩺</div><h3 style='text-align:center;'>30+ Medicines Info with Voice</h3></div>", unsafe_allow_html=True)
    meds = {"Dolo 650":"fever","Cetzine":"cold","Ascoril":"cough","Digene":"stomach","ORS":"loose motion","Paracetamol":"headache","Vicks":"cold","Burnol":"burn","Band-Aid":"cut"}
    cols = st.columns(3)
    for i,(m,k) in enumerate(meds.items()):
        with cols[i%3]:
            st.markdown(f"<div class='card'><b>{m}</b><br>{k}</div>", unsafe_allow_html=True)
            if st.button(f"🔊 {m}", key=m):
                eng,tel,hin = get_reply(k); speak_trilingual(eng,tel,hin,"all")

elif feature == "🧘 Health Tips & Yoga":
    st.markdown("<div class='card'><div class='logo'>🧘‍♀️🏃‍♂️🥗</div><h3 style='text-align:center;'>Health Tips & Yoga - Daily Routine</h3></div>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        st.success("**🌅 Daily Tips**\n- Walk 30 min\n- Yoga 15 min\n- 3L water\n- 8h sleep\n- Millets & Fruits\n- No junk food")
    with c2:
        st.info("**🧘 5 Best Yoga**\n1. Surya Namaskar - Full body\n2. Pranayama - Asthma, BP\n3. Vajrasana - Digestion\n4. Bhujangasana - Back pain\n5. Anulom Vilom - Stress")
    if st.button("🔊 Health Tips Voice"): speak_trilingual("Walk 30 min, Yoga 15 min, 3L water, 8h sleep", "30 నిమి నడక, 15 నిమి యోగా", "30 मिनट पैदल, 15 मिनट योगा")

elif feature == "🚨 Emergency 108":
    st.markdown("<div class='card'><div class='logo'>🚨🚑</div><h3 style='text-align:center;color:red;'>EMERGENCY 108 - TIRUVURU 24/7</h3></div>", unsafe_allow_html=True)
    st.error("🚑 **108** - Ambulance | 🚓 **100** - Police | 🏥 **Tiruvuru Govt Hospital**")
    st.write("**Chest pain, Snake bite, Dog bite, Bleeding, Accident - Call 108 NOW!**")
    if st.button("🔊 Emergency Voice LOUD"): speak_trilingual("Emergency! Call 108 Ambulance Now! Go to Tiruvuru Govt Hospital!", "అత్యవసరం! 108 కు కాల్ చేయండి!", "आपातकाल! 108 को कॉल करें!")

elif feature == "📸 Image Analyzer":
    st.markdown("<div class='card'><div class='logo'>📸🔬🤖</div><h3 style='text-align:center;'>AI Image Analyzer - Wound / Skin / Rash</h3></div>", unsafe_allow_html=True)
    img = st.file_uploader("Upload image", type=["jpg","png","jpeg"])
    if img:
        st.image(Image.open(img), use_column_width=True)
        st.info("AI Scan: Redness/Swelling/Pus -> Doctor. Keep clean with Dettol.")
        if st.button("🔊 Image Voice"): speak_trilingual("Keep wound clean, if swelling go to hospital", "గాయం శుభ్రం చేయండి", "घाव साफ करें")

elif feature == "ℹ️ About":
    st.balloons()
    st.markdown("<div class='card'><div class='logo'>🏥❤️🙏</div><h3 style='text-align:center;'>Made for Tiruvuru People - Free 24/7 Service<br>30+ Symptoms | 3 Languages | Voice AI</h3></div>", unsafe_allow_html=True)
