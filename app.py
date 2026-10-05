import streamlit as st, base64
from PIL import Image
from gtts import gTTS
from pydub import AudioSegment

st.set_page_config(page_title="AI MEDICAL ASSISTANT", layout="wide")

st.markdown("<h1 style='text-align:center;'>🩺 AI MEDICAL ASSISTANT 🌈</h1><p style='text-align:center;color:gray;'>తెలుగు | हिंदी | English</p>", unsafe_allow_html=True)

def speak_sequential(te_text, hi_text, en_text):
    try:
        gTTS(text=te_text, lang='te', slow=False).save("te.mp3")
        gTTS(text=hi_text, lang='hi', slow=False).save("hi.mp3")
        gTTS(text=en_text, lang='en', slow=False).save("en.mp3")
        combined = AudioSegment.from_mp3("te.mp3") + AudioSegment.silent(duration=700) + AudioSegment.from_mp3("hi.mp3") + AudioSegment.silent(duration=700) + AudioSegment.from_mp3("en.mp3")
        combined.export("final.mp3", format="mp3")
        with open("final.mp3","rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.markdown(f"<p style='text-align:center;'>🎧 <b>Sequential Voice - Telugu -> Hindi -> English</b></p><audio controls autoplay style='width:100%'><source src='data:audio/mp3;base64,{b64}' type='audio/mp3'></audio>", unsafe_allow_html=True)
    except: st.warning("Voice loading...")

# Native script DB - No emojis inside
SYMPTOMS_DB = {
"fever": {
"te": "నమస్తే, మీకు జ్వరం ఉంది. డోలో 650 తీసుకోండి. విశ్రాంతి, చల్లని గుడ్డ, చల్లని స్నానం వద్దు, మాస్క్, 3-4 లీటర్ల నీరు, ఫ్యాన్ వద్దు, మందు షేర్ వద్దు, వాంతులు ఉంటే హాస్పిటల్. ఆహారం: ఖిచిడి, గంజి",
"hi": "नमस्ते, आपको बुखार है। डोलो 650 लीजिए। आराम, ठंडी पट्टी, ठंडा पानी नहीं, मास्क, 3-4 लीटर पानी, फैन नहीं, शेयर नहीं, उल्टी तो हॉस्पिटल।",
"en": "Hello, you have Fever. Dolo 650. Rest, cold cloth, no cold bath, mask, 3-4L water, no fan, dont share, if vomit hospital."
},
"cold": {
"te": "నమస్తే, మీకు జలుబు ఉంది. సెట్రిజిన్ రాత్రి. ఆవిరి 2 సార్లు, వెచ్చని బట్టలు, చల్లని నీరు 5 రోజులు వద్దు, దుమ్ము వద్దు, రుమాలు, పిల్లల దగ్గర వద్దు, గోరువెచ్చని నీరు",
"hi": "नमस्ते, आपको जुकाम है। सेट्रिजिन रात में। भाप 2 बार, गरम कपड़े, ठंडा पानी 5 दिन नहीं, धूल नहीं, रुमाल, बच्चों से दूरी, गरम पानी",
"en": "Hello, you have Cold. Cetrizine night. Steam twice, warm clothes, no cold water 5 days, no dust, hanky, away kids, warm water"
},
"cough": {
"te": "నమస్తే, మీకు దగ్గు ఉంది. అస్కోరిల్. ఆవిరి, తేనె మిరియం, చల్లనివి వద్దు, డస్ట్ మాస్క్, గోరువెచ్చని నీరు",
"hi": "नमस्ते, आपको खांसी है। एस्कोरिल। भाप, शहद, ठंडा नहीं, मास्क, गरम पानी",
"en": "Hello, you have Cough. Ascoril. Steam, honey, no cold, mask, warm water"
},
}

def get_reply(sym):
    sym=sym.lower()
    for k in SYMPTOMS_DB:
        if k in sym: return SYMPTOMS_DB[k]
    return {"te":"మీకు ఏ సమస్య ఉందో చెప్పండి.","hi":"आपको क्या समस्या है बताइए।","en":"Please tell your symptoms."}

feature = st.sidebar.selectbox("SELECT FEATURE", ["🩺 AI Doctor Chat", "🥗 Diet Plan Section", "🧘 Health Tips Section", "📸 Image Analyser Section", "🚨 Emergency"])

if "Doctor Chat" in feature:
    st.markdown("<div style='background:#1E1E1E;padding:20px;border-radius:15px;border:1px solid #00E5FF;text-align:center;'><h3>🎤 AI Doctor Chat - 3 Languages 🗣️</h3></div>", unsafe_allow_html=True)
    user_input = st.text_input("లక్షణాలు / लक्षण / Symptoms", placeholder="నాకు జ్వరం / मुझे बुखार / I have fever")
    if user_input:
        d = get_reply(user_input)
        st.markdown(f"<div style='background:#1E1E1E;padding:20px;border-radius:15px;border:1px solid #333;margin-top:10px;'><p style='color:#92FE9D'><b>తెలుగు:</b> {d['te']}</p><hr><p style='color:#FFD93D'><b>हिंदी:</b> {d['hi']}</p><hr><p style='color:#00E5FF'><b>English:</b> {d['en']}</p></div>", unsafe_allow_html=True)
        speak_sequential(d['te'], d['hi'], d['en'])

elif "Diet Plan" in feature:
    st.markdown("<div style='background:#1E1E1E;padding:20px;border-radius:15px;border:1px solid #92FE9D'><h3 style='text-align:center'>🥗 Diet Plan Section 🍎</h3><p style='color:#92FE9D'><b>తెలుగు:</b> ఉదయం గోరువెచ్చని నీరు రెండు అరటిపండ్లు, మధ్యాహ్నం అన్నం పప్పు పెరుగు, రాత్రి రెండు చపాతీలు తొమ్మిది గంటల లోపు.</p><p style='color:#FFD93D'><b>हिंदी:</b> सुबह गुनगुना पानी दो केले, दोपहर चावल दाल दही, रात दो चपाती नौ बजे से पहले।</p><p style='color:#00E5FF'><b>English:</b> Morning lukewarm water two bananas, afternoon rice dal curd, night two chapatis before nine.</p></div>", unsafe_allow_html=True)

elif "Health Tips" in feature:
    st.markdown("<div style='background:#1E1E1E;padding:20px;border-radius:15px;border:1px solid #00E5FF'><h3 style='text-align:center'>🧘 Health Tips Section 🌿</h3><p style='color:#92FE9D'><b>తెలుగు:</b> రోజూ 30 నిమిషాలు నడవండి, 3 లీటర్ల నీరు తాగండి, 8 గంటలు నిద్రపోండి.</p><p style='color:#FFD93D'><b>हिंदी:</b> रोज 30 मिनट पैदल चलें, 3 लीटर पानी पिएं, 8 घंटे सोएं।</p><p style='color:#00E5FF'><b>English:</b> Walk 30 minutes daily, drink 3 liters water, sleep 8 hours.</p></div>", unsafe_allow_html=True)

elif "Image Analyser" in feature:
    st.markdown("<div style='background:#1E1E1E;padding:20px;border-radius:15px;border:1px solid #FF6B6B;text-align:center;'><h3>📸 Image Analyser Section 🔍</h3></div>", unsafe_allow_html=True)
    f = st.file_uploader("Photo Upload", type=["jpg","png","jpeg"])
    if f:
        st.image(Image.open(f), use_column_width=True)
        te="ఫోటో చూశాను, డాక్టర్‌కి చూపించండి, శుభ్రంగా ఉంచండి."; hi="फोटो देख ली, डॉक्टर को दिखाइए, साफ रखिए।"; en="Seen photo, show to doctor, keep clean."
        st.markdown(f"<div style='background:#1E1E1E;padding:15px;border-radius:10px'><p style='color:#92FE9D'><b>తెలుగు:</b> {te}</p><p style='color:#FFD93D'><b>हिंदी:</b> {hi}</p><p style='color:#00E5FF'><b>English:</b> {en}</p></div>", unsafe_allow_html=True)
        speak_sequential(te, hi, en)

elif "Emergency" in feature:
    st.markdown("<div style='background:#2E0000;padding:20px;border-radius:15px;text-align:center;border:2px solid red;'><h3>🚨 Emergency Section 🆘</h3><p>108 కి కాల్ చేయండి / 108 पर कॉल करें / Call 108</p></div>", unsafe_allow_html=True)
