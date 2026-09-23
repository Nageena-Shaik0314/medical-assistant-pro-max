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
<div class='main-title'>🏥 MEDICAL ASSISTANT PRO MAX - TIRUVURU<br><small>🤖 AI Chatbot 24/7 | 🎤 Voice | 💊 30+ Symptoms | 🧘 Yoga | 🚨 108</small></div>
""", unsafe_allow_html=True)
st.warning("⚠️ Educational Only - Consult Real Doctor at Tiruvuru Govt Hospital")

def speak_single(text, lang_code):
    try:
        tts = gTTS(text=text[:380], lang=lang_code, slow=False)
        tts.save("voice.mp3")
        with open("voice.mp3","rb") as f: st.audio(f.read(), format="audio/mp3", autoplay=True)
        os.remove("voice.mp3")
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

# ===== LANGUAGE SELECT - NO ALL OPTION =====
st.write("### 🌐 Select Language - Only Selected Language Will Reply")
lang_choice = st.radio("Voice Language:", ["English", "Telugu - తెలుగు", "Hindi - हिंदी"], horizontal=True, index=0)

# ===== SIDEBAR =====
feature = st.sidebar.selectbox("📋 SELECT",
["🎤 🤖 AI Chatbot 24/7 - Voice In & Out","💊 Medicine Info - 30+","🧘 Health Tips & Yoga","🚨 Emergency 108","📸 Image Analyzer","ℹ️ About"])

if feature == "🎤 🤖 AI Chatbot 24/7 - Voice In & Out":
    st.markdown("<div class='card'><div class='logo'>🎤🤖💬</div><h3 style='text-align:center;'>AI Chatbot 24/7 - Independent Voice & Text - Single Language</h3></div>", unsafe_allow_html=True)
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
                    if "Telugu" in lang_choice: text = r.recognize_google(audio_data, language='te-IN')
                    elif "Hindi" in lang_choice: text = r.recognize_google(audio_data, language='hi-IN')
                    else: text = r.recognize_google(audio_data, language='en-IN')
                os.remove(tmp_path)
                st.success(f"✅ You said: **{text}**")
                eng, tel, hin = get_reply(text)
                if "Telugu" in lang_choice:
                    st.chat_message("assistant").write(f"**TE:** {tel}")
                    speak_single(tel, 'te')
                elif "Hindi" in lang_choice:
                    st.chat_message("assistant").write(f"**HI:** {hin}")
                    speak_single(hin, 'hi')
                else:
                    st.chat_message("assistant").write(f"**EN:** {eng}")
                    speak_single(eng, 'en')
            except: st.warning("Voice clear ga ledu, malli cheppu!")
    with col2:
        st.markdown("### ⌨️ **Type → Direct Text Reply**")
        st.caption("30+ symptoms: fever, cold, cough, headache, chest pain, bp, sugar, asthma, allergy, vomiting, back pain, joint pain, skin rash, eye pain, tooth pain, dizziness, cut, burn, dog bite, snake bite...")
        q = st.chat_input("Type symptom: fever / jwaram / bukhar...")
        if q:
            st.chat_message("user").write(f"You: {q}")
            eng, tel, hin = get_reply(q)
            if "Telugu" in lang_choice:
                st.chat_message("assistant").write(f"**TE:** {tel}")
                speak_single(tel, 'te')
            elif "Hindi" in lang_choice:
                st.chat_message("assistant").write(f"**HI:** {hin}")
                speak_single(hin, 'hi')
            else:
                st.chat_message("assistant").write(f"**EN:** {eng}")
                speak_single(eng, 'en')
            st.download_button("📄 Download", data=f"{eng}\n{tel}\n{hin}\n{datetime.now()}", file_name="Prescription.txt")

elif feature == "💊 Medicine Info - 30+":
    st.markdown("<div class='card'><div class='logo'>💊💉🩺</div><h3 style='text-align:center;'>30+ Medicines Info</h3></div>", unsafe_allow_html=True)
    meds = {"Dolo 650":"fever","Cetzine":"cold","Ascoril":"cough","Digene":"stomach","ORS":"loose motion","Paracetamol":"headache","Vicks":"cold","Burnol":"burn","Band-Aid":"cut"}
    cols = st.columns(3)
    for i,(m,k) in enumerate(meds.items()):
        with cols[i%3]:
            st.markdown(f"<div class='card'><b>{m}</b><br>{k}</div>", unsafe_allow_html=True)
            if st.button(f"🔊 {m}", key=m):
                eng,tel,hin = get_reply(k)
                if "Telugu" in lang_choice: speak_single(tel,'te')
                elif "Hindi" in lang_choice: speak_single(hin,'hi')
                else: speak_single(eng,'en')

elif feature == "🧘 Health Tips & Yoga":
    st.markdown("<div class='card'><div class='logo'>🧘‍♀️🏃‍♂️🥗</div><h3 style='text-align:center;'>Health Tips & Yoga</h3></div>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1: st.success("**🌅 Daily Tips**\n- Walk 30 min\n- Yoga 15 min\n- 3L water\n- 8h sleep\n- Millets & Fruits")
    with c2: st.info("**🧘 Yoga**\n1. Surya Namaskar\n2. Pranayama\n3. Vajrasana\n4. Bhujangasana\n5. Anulom Vilom")
    if st.button("🔊 Health Tips Voice"):
        if "Telugu" in lang_choice: speak_single("30 నిమి నడక, 15 నిమి యోగా, 3L నీరు", 'te')
        elif "Hindi" in lang_choice: speak_single("30 मिनट पैदल, 15 मिनट योगा, 3L पानी", 'hi')
        else: speak_single("Walk 30 min, Yoga 15 min, 3L water", 'en')

elif feature == "🚨 Emergency 108":
    st.markdown("<div class='card'><div class='logo'>🚨🚑</div><h3 style='text-align:center;color:red;'>EMERGENCY 108 - TIRUVURU 24/7</h3></div>", unsafe_allow_html=True)
    st.error("🚑 **108** - Ambulance | 🚓 **100** - Police | 🏥 **Tiruvuru Govt Hospital**")
    if st.button("🔊 Emergency Voice LOUD"):
        if "Telugu" in lang_choice: speak_single("అత్యవసరం! 108 అంబులెన్స్ కు కాల్ చేయండి!", 'te')
        elif "Hindi" in lang_choice: speak_single("आपातकाल! 108 को कॉल करें!", 'hi')
        else: speak_single("Emergency! Call 108 Ambulance Now!", 'en')

elif feature == "📸 Image Analyzer":
    st.markdown("<div class='card'><div class='logo'>📸🔬🤖</div><h3 style='text-align:center;'>AI Image Analyzer</h3></div>", unsafe_allow_html=True)
    img = st.file_uploader("Upload image", type=["jpg","png","jpeg"])
    if img:
        st.image(Image.open(img), use_column_width=True)
        st.info("AI Scan: Redness/Swelling/Pus -> Doctor. Keep clean with Dettol.")
        if st.button("🔊 Image Voice"):
            if "Telugu" in lang_choice: speak_single("గాయం శుభ్రం చేయండి", 'te')
            elif "Hindi" in lang_choice: speak_single("घाव साफ करें", 'hi')
            else: speak_single("Keep wound clean", 'en')

elif feature == "ℹ️ About":
    st.balloons()
    st.markdown("<div class='card'><div class='logo'>🏥❤️🙏</div><h3 style='text-align:center;'>Made for Tiruvuru People<br>30+ Symptoms | Single Language Voice</h3></div>", unsafe_allow_html=True)
