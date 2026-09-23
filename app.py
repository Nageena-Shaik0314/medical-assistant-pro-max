import streamlit as st
from datetime import datetime
from gtts import gTTS
import os
from PIL import Image

st.set_page_config(page_title="Medical Assistant - Tiruvuru", layout="centered", page_icon="🏥")
st.warning("⚠️ Educational Only - Consult Real Doctor")
st.title("🏥 Medical Assistant Pro Max - Tiruvuru")

def speak_bilingual(eng_text, tel_text, lang_choice="both"):
    try:
        if lang_choice in ["both","english"]:
            st.write("🔊 **AI English:**")
            tts_en = gTTS(text=eng_text[:350], lang='en', slow=False)
            tts_en.save("en.mp3")
            with open("en.mp3", "rb") as f:
                st.audio(f.read(), format="audio/mp3")
            os.remove("en.mp3")
        if lang_choice in ["both","telugu"]:
            st.write("🔊 **AI Telugu - తెలుగు:**")
            tts_te = gTTS(text=tel_text[:350], lang='te', slow=False)
            tts_te.save("te.mp3")
            with open("te.mp3", "rb") as f:
                st.audio(f.read(), format="audio/mp3")
            os.remove("te.mp3")
    except Exception as e:
        st.error(f"Voice error: Add gtts in requirements.txt and reboot. {e}")

# SIDEBAR
feature = st.sidebar.selectbox("📋 Select", 
["🎤 AI Doctor Chat - Voice In & Out", "💊 Medicine Info", "🧘 Health Tips", "🚨 Emergency", "📸 Image Analyzer"])

st.sidebar.write("---")
st.sidebar.write("🎤 **User Voice:** Mic nokki matladu")
st.sidebar.write("🔊 **AI Voice:** Telugu + English")

if feature == "🎤 AI Doctor Chat - Voice In & Out":
    st.subheader("🎤 User Matladandi - AI Reply Istundi")
    
    # ===== 1. USER VOICE INPUT - NEW FEATURE YOU ASKED =====
    st.write("### 🎤 STEP 1: Nuvvu Matladu / Speak Your Symptom")
    st.caption("Mic button nokki cheppu: 'naaku jwaram undi' or 'I have fever'")
    user_audio = st.audio_input("🎤 Click to speak - Mic nokku...")
    
    user_text = ""
    if user_audio:
        st.success("✅ Nee voice record ayyindi! Vintondi...")
        st.audio(user_audio)
        # Note: Voice to text automatic kadu - nuvvu kinda type kuda chey
        st.info("🎧 Voice note: Nee voice vinnanu. Ippudu kinda text lo kuda same symptom type chey - AI voice lo reply istundi!")
        user_text = "Voice recorded - Please type below also"

    # ===== 2. TEXT INPUT ALSO =====
    st.write("### ⌨️ STEP 2: Text lo kuda type chey (Voice tho paatu)")
    q = st.chat_input("Ex: jwaram / fever / tala noppi / stomach pain...")

    if q:
        st.chat_message("user").write(f"🧑‍⚕️ You: {q}")
        if user_audio:
            st.write("🎤 + ⌨️ Voice + Text both received!")

        q_lower = q.lower()
        eng_reply = ""
        tel_reply = ""

        # DATABASE - Telugu + English Symptoms
        if "fever" in q_lower or "jwaram" in q_lower:
            eng_reply = "Fever: Rest, 3 liters water, cold cloth on forehead. Dolo 650 after food. Khichdi, coconut water. If 2 days, Tiruvuru Govt Hospital."
            tel_reply = "జ్వరం: విశ్రాంతి, 3 లీటర్ల నీరు, నుదుటిపై చల్లని గుడ్డ. భోజనం తర్వాత డోలో 650. ఖిచ్డీ, కొబ్బరి నీరు. 2 రోజులు ఉంటే తిరువూరు ఆసుపత్రి."
        elif "cold" in q_lower or "jalu" in q_lower:
            eng_reply = "Cold: Steam 2 times, warm clothes. Cetzine night, Vicks rub. Hot soup, ginger tea."
            tel_reply = "జలుబు: రోజూ 2 సార్లు ఆవిరి, వెచ్చని బట్టలు. రాత్రి సెట్జిన్, విక్స్. వేడి సూప్, అల్లం టీ."
        elif "cough" in q_lower or "daggu" in q_lower:
            eng_reply = "Cough: Salt water gargle 3 times, mask. Honey ginger, Ascoril syrup."
            tel_reply = "దగ్గు: ఉప్పు నీటితో 3 సార్లు పుక్కిలింపు, మాస్క్. తేనె అల్లం, అస్కోరిల్ సిరప్."
        elif "headache" in q_lower or "tala" in q_lower:
            eng_reply = "Headache: Dark room, no phone, 8 hours sleep. Paracetamol, head massage."
            tel_reply = "తలనొప్పి: చీకటి గది, ఫోన్ వద్దు, 8 గంటలు నిద్ర. పారాసిటమాల్, తల మసాజ్."
        elif "stomach" in q_lower or "kadupu" in q_lower:
            eng_reply = "Stomach pain: No spicy, jeera water. Digene, curd rice, banana."
            tel_reply = "కడుపు నొప్పి: కారం వద్దు, జీలకర్ర నీరు. డైజీన్, పెరుగు అన్నం, అరటిపండు."
        elif "bp" in q_lower or "pressure" in q_lower:
            eng_reply = "BP: Less salt, no tension, walk 30 min. BP tablet regular. Less oil, fruits."
            tel_reply = "బీపీ: ఉప్పు తగ్గించు, టెన్షన్ వద్దు, 30 నిమి నడక. బీపీ టాబ్లెట్. నూనె తక్కువ, పండ్లు."
        elif "sugar" in q_lower or "diabetes" in q_lower or "chakara" in q_lower:
            eng_reply = "Diabetes: No sugar, walk 30 min, check sugar. Millets, vegetables."
            tel_reply = "షుగర్: చక్కెర వద్దు, 30 నిమి నడక, షుగర్ చెక్. చిరుధాన్యాలు, కూరగాయలు."
        elif "chest" in q_lower or "gund" in q_lower:
            eng_reply = "Chest Pain Emergency: Sit, rest, call 108, go to Tiruvuru Govt Hospital immediately."
            tel_reply = "ఛాతీ నొప్పి అత్యవసరం: కూర్చోండి, 108 కు కాల్ చేయండి, వెంటనే తిరువూరు ఆసుపత్రికి వెళ్ళండి."
        else:
            eng_reply = f"For {q}: Rest, 3L water, 8 hours sleep, light food. If 2 days, Tiruvuru Govt Hospital."
            tel_reply = f"{q} కోసం: విశ్రాంతి, 3 లీటర్ల నీరు, 8 గంటలు నిద్ర, తేలికపాటి ఆహారం. 2 రోజులు ఉంటే తిరువూరు ఆసుపత్రి."

        st.chat_message("assistant").write(f"**English:** {eng_reply}\n\n**తెలుగు:** {tel_reply}")

        # ===== 3. AI VOICE REPLY - AUTOMATIC =====
        st.success("### 🔊 AI Voice Reply - AI Matladuthondi...")
        
        lang_choice = st.radio("Voice Language / భాష ఎంచుకోండి:", ["both - రెండూ", "telugu - తెలుగు మాత్రమే", "english - English only"], horizontal=True)
        
        choice_map = {"both - రెండూ":"both", "telugu - తెలుగు మాత్రమే":"telugu", "english - English only":"english"}
        
        speak_bilingual(eng_reply, tel_reply, choice_map[lang_choice])

        # Buttons
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔊 Malli Vinu / Replay"):
                speak_bilingual(eng_reply, tel_reply, choice_map[lang_choice])
        with c2:
            txt = f"Date: {datetime.now()}\nSymptom: {q}\nEN: {eng_reply}\nTE: {tel_reply}"
            st.download_button("📄 Download", data=txt, file_name="Prescription.txt")

    # Show user voice recorder again at bottom
    st.write("---")
    st.write("🎤 **Tip:** Chadavadam rani vallu - Mic lo matladi, tarvata same matter okka padam type chesina chalu, AI Telugu lo voice lo chepthundi!")

elif feature == "💊 Medicine Info":
    st.subheader("Medicine Info")
    st.write("Dolo 650 - Jwaram, Cetzine - Jalu, ORS - Neerasam")
    if st.button("🔊 Voice"): 
        speak_bilingual("Dolo 650 for fever after food", "జ్వరానికి డోలో 650 భోజనం తర్వాత")

elif feature == "🧘 Health Tips":
    st.subheader("Health Tips")
    st.write("Walk 30 min, 3L water, 8 hours sleep. Telugu: 30 nimisha nadaka, 3L neeru")
    if st.button("🔊 Voice"): 
        speak_bilingual("Walk daily 30 minutes", "రోజూ 30 నిమిషాలు నడవండి")

elif feature == "🚨 Emergency":
    st.error("🚨 108 - Ambulance / అంబులెన్స్\n🏥 Tiruvuru Govt Hospital")
    if st.button("🔊 Emergency Voice"):
        speak_bilingual("Call 108 ambulance now", "108 అంబులెన్స్ కు ఇప్పుడే కాల్ చేయండి")

elif feature == "📸 Image Analyzer":
    st.subheader("Image Analyzer")
    img = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])
    if img: 
        st.image(Image.open(img), use_column_width=True)
        st.info("Educational only. Consult doctor.")

    
