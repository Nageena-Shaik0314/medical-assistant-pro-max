import streamlit as st
from datetime import datetime
from gtts import gTTS
import os
from PIL import Image

st.set_page_config(page_title="Medical Assistant - Tiruvuru", layout="centered", page_icon="🏥")
st.warning("⚠️ Educational Only - Consult Real Doctor")
st.title("🏥 Medical Assistant Pro Max - Tiruvuru")
st.caption("🗣️ Telugu + Hindi + English - 3 Languages Voice")

def speak_trilingual(eng, tel, hin, lang="all"):
    try:
        if lang in ["all","english"]:
            st.write("🔊 **English:**")
            tts = gTTS(text=eng[:350], lang='en', slow=False)
            tts.save("en.mp3")
            with open("en.mp3","rb") as f: st.audio(f.read(), format="audio/mp3", autoplay=True)
            os.remove("en.mp3")
        if lang in ["all","telugu"]:
            st.write("🔊 **Telugu - తెలుగు:**")
            tts = gTTS(text=tel[:350], lang='te', slow=False)
            tts.save("te.mp3")
            with open("te.mp3","rb") as f: st.audio(f.read(), format="audio/mp3", autoplay=True)
            os.remove("te.mp3")
        if lang in ["all","hindi"]:
            st.write("🔊 **Hindi - हिंदी:**")
            tts = gTTS(text=hin[:350], lang='hi', slow=False)
            tts.save("hi.mp3")
            with open("hi.mp3","rb") as f: st.audio(f.read(), format="audio/mp3", autoplay=True)
            os.remove("hi.mp3")
    except Exception as e:
        st.error(f"Voice error: {e}. Please Reboot app.")

feature = st.sidebar.selectbox("📋 Select",
["🎤 AI Doctor Chat - 3 Languages","💊 Medicine Info","🧘 Health Tips","🚨 Emergency","📸 Image Analyzer"])

if feature == "🎤 AI Doctor Chat - 3 Languages":
    st.subheader("🎤 Speak in Telugu / Hindi / English")
    st.write("Try: `jwaram / bukhar / fever`, `jalu / zukam / cold`, `sir dard / tala noppi / headache`")

    st.write("### 🎤 STEP 1: Nuvvu Matladu / Aap Boliye / Speak")
    user_audio = st.audio_input("🎤 Mic nokku / Mic dabao / Click to speak...")
    if user_audio:
        st.audio(user_audio)
        st.success("✅ Voice recorded! Kinda text lo kuda type chey / neeche type bhi karo")

    q = st.chat_input("Type: jwaram / bukhar / fever / cold / khansi / daggu...")

    if q:
        st.chat_message("user").write(f"You: {q}")
        ql = q.lower()

        eng = tel = hin = ""

        if "fever" in ql or "jwaram" in ql or "bukhar" in ql or "बुखार" in q:
            eng = "Fever: Rest, 3 liters water, cold cloth on forehead. Dolo 650 after food. Khichdi, coconut water. If 2 days, go to Tiruvuru Govt Hospital."
            tel = "జ్వరం: విశ్రాంతి, 3 లీటర్ల నీరు, నుదుటిపై చల్లని గుడ్డ. భోజనం తర్వాత డోలో 650. ఖిచ్డీ, కొబ్బరి నీరు. 2 రోజులు ఉంటే తిరువూరు ఆసుపత్రి."
            hin = "बुखार: आराम करें, 3 लीटर पानी पिएं, माथे पर ठंडा कपड़ा रखें। खाने के बाद डोलो 650 लें। खिचड़ी, नारियल पानी। 2 दिन रहे तो तिरुवूरु सरकारी अस्पताल जाएं।"

        elif "cold" in ql or "jalu" in ql or "zukam" in ql or "जुकाम" in q:
            eng = "Cold: Steam 2 times, warm clothes. Cetzine at night, Vicks rub. Hot soup, ginger tea."
            tel = "జలుబు: రోజూ 2 సార్లు ఆవిరి, వెచ్చని బట్టలు. రాత్రి సెట్జిన్, విక్స్. వేడి సూప్, అల్లం టీ."
            hin = "जुकाम: दिन में 2 बार भाप लें, गर्म कपड़े पहनें। रात में सेटजीन, विक्स लगाएं। गर्म सूप, अदरक चाय।"

        elif "cough" in ql or "daggu" in ql or "khansi" in ql or "खांसी" in q:
            eng = "Cough: Salt water gargle 3 times, mask. Honey ginger, Ascoril syrup."
            tel = "దగ్గు: ఉప్పు నీటితో 3 సార్లు పుక్కిలింపు, మాస్క్. తేనె అల్లం, అస్కోరిల్ సిరప్."
            hin = "खांसी: नमक पानी से 3 बार गरारे, मास्क पहनें। शहद अदरक, एस्कोरिल सिरप।"

        elif "headache" in ql or "tala" in ql or "sir dard" in ql or "सिर दर्द" in q:
            eng = "Headache: Dark room, no phone, 8 hours sleep. Paracetamol, head massage."
            tel = "తలనొప్పి: చీకటి గది, ఫోన్ వద్దు, 8 గంటలు నిద్ర. పారాసిటమాల్, తల మసాజ్."
            hin = "सिर दर्द: अंधेरे कमरे में आराम, फोन नहीं, 8 घंटे नींद। पैरासिटामोल, सिर की मालिश।"

        elif "stomach" in ql or "kadupu" in ql or "pet dard" in ql or "पेट दर्द" in q:
            eng = "Stomach pain: No spicy, jeera water. Digene, curd rice, banana."
            tel = "కడుపు నొప్పి: కారం వద్దు, జీలకర్ర నీరు. డైజీన్, పెరుగు అన్నం, అరటిపండు."
            hin = "पेट दर्द: तीखा खाना नहीं, जीरा पानी। डाइजीन, दही चावल, केला।"

        elif "bp" in ql or "pressure" in ql:
            eng = "BP: Less salt, no tension, walk 30 min. BP tablet regular."
            tel = "బీపీ: ఉప్పు తగ్గించు, టెన్షన్ వద్దు, 30 నిమి నడక. బీపీ టాబ్లెట్."
            hin = "बीपी: नमक कम, टेंशन नहीं, 30 मिनट पैदल। बीपी गोली रोज़।"

        elif "sugar" in ql or "diabetes" in ql or "chakara" in ql:
            eng = "Diabetes: No sugar, walk 30 min, check sugar. Millets, vegetables."
            tel = "షుగర్: చక్కెర వద్దు, 30 నిమి నడక, షుగర్ చెక్. చిరుధాన్యాలు, కూరగాయలు."
            hin = "शुगर: चीनी नहीं, 30 मिनट पैदल, शुगर चेक। मिलेट्स, सब्जियां।"

        else:
            eng = f"For {q}: Rest, 3L water, 8 hours sleep, light food. If 2 days, Tiruvuru Govt Hospital."
            tel = f"{q} కోసం: విశ్రాంతి, 3 లీ నీరు, 8 గం నిద్ర, తేలికపాటి ఆహారం. 2 రోజులు ఉంటే తిరువూరు ఆసుపత్రి."
            hin = f"{q} के लिए: आराम, 3 लीटर पानी, 8 घंटे नींद, हल्का खाना। 2 दिन रहे तो तिरुवूरु अस्पताल।"

        st.chat_message("assistant").write(f"**EN:** {eng}\n\n**TE:** {tel}\n\n**HI:** {hin}")

        st.success("🔊 AI Trilingual Voice Reply...")
        lang_opt = st.radio("Voice / భాష / भाषा:", ["all - అన్నీ - सभी","telugu - తెలుగు","hindi - हिंदी","english - English"], horizontal=True)
        mp = {"all - అన్నీ - सभी":"all","telugu - తెలుగు":"telugu","hindi - हिंदी":"hindi","english - English":"english"}
        speak_trilingual(eng, tel, hin, mp[lang_opt])

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔊 Replay / Malli Vinu / Phir Suno"):
                speak_trilingual(eng, tel, hin, mp[lang_opt])
        with col2:
            st.download_button("📄 Download", data=f"{eng}\n{tel}\n{hin}", file_name="Prescription.txt")

elif feature == "💊 Medicine Info":
    st.subheader("Medicine Info - 3 Languages")
    if st.button("🔊 Voice - Dolo"): speak_trilingual("Dolo 650 for fever after food", "జ్వరానికి డోలో 650 భోజనం తర్వాత", "बुखार के लिए डोलो 650 खाने के बाद")

elif feature == "🧘 Health Tips":
    st.subheader("Health Tips")
    st.write("EN: Walk 30 min, 3L water\nTE: 30 నిమి నడక, 3L నీరు\nHI: 30 मिनट पैदल, 3L पानी")
    if st.button("🔊 Voice"): speak_trilingual("Walk 30 minutes daily", "రోజూ 30 నిమిషాలు నడవండి", "रोज 30 मिनट पैदल चलें")

elif feature == "🚨 Emergency":
    st.error("🚨 108 Ambulance / 108 అంబులెన్స్ / 108 एम्बुलेंस")
    if st.button("🔊 Emergency Voice"): speak_trilingual("Call 108 ambulance now", "108 అంబులెన్స్ కు కాల్ చేయండి", "108 एम्बुलेंस को अभी कॉल करें")

elif feature == "📸 Image Analyzer":
    st.subheader("📸 Image Analyzer")
    img = st.file_uploader("Upload", type=["jpg","png","jpeg"])
    if img: st.image(Image.open(img), use_column_width=True)
