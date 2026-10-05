import streamlit as st, re, base64, os
from PIL import Image
from gtts import gTTS
from pydub import AudioSegment

st.set_page_config(page_title="Tiruvuru Native Script Doctor", layout="wide")
st.markdown("<h2 style='text-align:center;color:#00E5FF'>తిరువూరు AI Doctor - Native Scripts</h2>", unsafe_allow_html=True)

def speak_sequential(te_text, hi_text, en_text):
    try:
        gTTS(text=te_text, lang='te', slow=False).save("te.mp3")
        gTTS(text=hi_text, lang='hi', slow=False).save("hi.mp3")
        gTTS(text=en_text, lang='en', slow=False).save("en.mp3")
        combined = AudioSegment.from_mp3("te.mp3") + AudioSegment.silent(duration=700) + AudioSegment.from_mp3("hi.mp3") + AudioSegment.silent(duration=700) + AudioSegment.from_mp3("en.mp3")
        combined.export("final.mp3", format="mp3")
        with open("final.mp3","rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.markdown(f"<audio controls autoplay style='width:100%'><source src='data:audio/mp3;base64,{b64}' type='audio/mp3'></audio>", unsafe_allow_html=True)
    except Exception as e:
        st.warning("Voice loading...")

# --- NATIVE SCRIPT DATABASE - 3 LANGUAGES IN ORIGINAL SCRIPT ---
SYMPTOMS_DB = {
"fever": {
"te": "నమస్తే, మీకు జ్వరం ఉంది. డోలో 650 తీసుకోండి. 1. విశ్రాంతి 2. చల్లని గుడ్డ 3. చల్లని స్నానం వద్దు 4. మాస్క్ 5. 3-4 లీటర్ల నీరు 6. ఫ్యాన్ వద్దు 7. మందు షేర్ వద్దు 8. వాంతులు ఉంటే హాస్పిటల్. ఆహారం: ఖిచిడి, గంజి",
"hi": "नमस्ते, आपको बुखार है। डोलो 650 लीजिए। 1. आराम 2. ठंडी पट्टी 3. ठंडा पानी नहीं 4. मास्क 5. 3-4 लीटर पानी 6. फैन नहीं 7. शेयर नहीं 8. उल्टी तो हॉस्पिटल।",
"en": "Hello, you have Fever. Dolo 650. 1.Rest 2.Cold cloth 3.No cold bath 4.Mask 5.3-4L water 6.No fan 7.Dont share 8.If vomit hospital. Food: Khichdi, kanji"
},
"cold": {
"te": "నమస్తే, మీకు జలుబు ఉంది. సెట్రిజిన్ రాత్రి. 1. ఆవిరి 2 సార్లు 2. వెచ్చని బట్టలు 3. చల్లని నీరు 5 రోజులు వద్దు 4. దుమ్ము వద్దు 5. రుమాలు 6. పిల్లల దగ్గర వద్దు 7. గోరువెచ్చని నీరు",
"hi": "नमस्ते, आपको जुकाम है। सेट्रिजिन रात में। 1. भाप 2 बार 2. गरम कपड़े 3. ठंडा पानी 5 दिन नहीं 4. धूल नहीं 5. रुमाल 6. बच्चों से दूरी 7. गरम पानी",
"en": "Hello, you have Cold. Cetrizine night. 1.Steam twice 2.Warm clothes 3.No cold water 5 days 4.No dust 5.Hanky 6.Away kids 7.Warm water"
},
"cough": {
"te": "నమస్తే, మీకు దగ్గు ఉంది. అస్కోరిల్. 1. ఆవిరి 2. తేనె+మిరియం 3. చల్లనివి వద్దు 4. డస్ట్ మాస్క్ 5. గోరువెచ్చని నీరు",
"hi": "नमस्ते, आपको खांसी है। एस्कोरिल। 1. भाप 2. शहद 3. ठंडा नहीं 4. मास्क 5. गरम पानी",
"en": "Hello, you have Cough. Ascoril. 1.Steam 2.Honey 3.No cold 4.Mask 5.Warm water"
},
"headache": {
"te": "నమస్తే, మీకు తలనొప్పి ఉంది. డోలో 650. 1. చీకటి గదిలో విశ్రాంతి 2. ఫోన్ వద్దు 3. 3 లీటర్ల నీరు 4. టీ తక్కువ 5. 8 గంటల నిద్ర",
"hi": "नमस्ते, आपको सिर दर्द है। डोलो 650। 1. अंधेरे में आराम 2. फोन नहीं 3. 3 लीटर पानी 4. चाय कम 5. 8 घंटे नींद",
"en": "Hello, you have Headache. Dolo 650. 1.Dark room rest 2.No phone 3.3L water 4.Less tea 5.8h sleep"
},
}

def get_reply(sym):
    sym=sym.lower()
    for k in SYMPTOMS_DB:
        if k in sym: return SYMPTOMS_DB[k]
    return {"te":"మీకు ఏ సమస్య ఉందో చెప్పండి.","hi":"आपको क्या समस्या है बताइए।","en":"Please tell your symptoms."}

feature = st.sidebar.selectbox("SELECT", ["AI Doctor Chat - 3 Native Voices", "Diet Plan Section", "Health Tips Section", "Image Analyser Section"])

if "Doctor Chat" in feature:
    user_input = st.text_input("లక్షణాలు చెప్పండి / लक्षण बताएं / Enter Symptoms", placeholder="నాకు జ్వరం / मुझे बुखार है / I have fever")
    if user_input:
        d = get_reply(user_input)
        st.markdown(f"<div style='background:#1E1E1E;padding:20px;border-radius:15px;border:1px solid #00E5FF'><p style='color:#92FE9D;font-size:18px'><b>తెలుగు:</b> {d['te']}</p><hr><p style='color:#FFD93D;font-size:18px'><b>हिंदी:</b> {d['hi']}</p><hr><p style='color:#00E5FF'><b>English:</b> {d['en']}</p></div>", unsafe_allow_html=True)
        speak_sequential(d['te'], d['hi'], d['en'])

elif "Diet Plan" in feature:
    te="ఉదయం: గోరువెచ్చని నీరు + రెండు అరటిపండ్లు, మధ్యాహ్నం: అన్నం + పప్పు + పెరుగు, రాత్రి: రెండు చపాతీలు తొమ్మిది గంటల లోపు."; hi="सुबह: गुनगुना पानी + दो केले, दोपहर: चावल + दाल + दही, रात: दो चपाती नौ बजे से पहले।"; en="Morning: Lukewarm water + two bananas, Afternoon: Rice + dal + curd, Night: Two chapatis before nine."
    st.markdown(f"<div style='background:#1E1E1E;padding:20px;border-radius:15px;border:1px solid #92FE9D'><p style='color:#92FE9D'>తెలుగు: {te}</p><p style='color:#FFD93D'>हिंदी: {hi}</p><p style='color:#00E5FF'>English: {en}</p></div>", unsafe_allow_html=True)
    speak_sequential(te, hi, en)

elif "Health Tips" in feature:
    te="రోజూ 30 నిమిషాలు నడవండి, 3 లీటర్ల నీరు తాగండి, 8 గంటలు నిద్రపోండి."; hi="रोज 30 मिनट पैदल चलें, 3 लीटर पानी पिएं, 8 घंटे सोएं।"; en="Walk 30 minutes daily, drink 3 liters water, sleep 8 hours."
    st.markdown(f"<div style='background:#1E1E1E;padding:20px;border-radius:15px'><p style='color:#92FE9D'>తెలుగు: {te}</p><p style='color:#FFD93D'>हिंदी: {hi}</p><p style='color:#00E5FF'>English: {en}</p></div>", unsafe_allow_html=True)
    speak_sequential(te, hi, en)

elif "Image Analyser" in feature:
    f = st.file_uploader("ఫోటో అప్‌లోడ్ చేయండి / फोटो अपलोड करें", type=["jpg","png","jpeg"])
    if f:
        st.image(Image.open(f), use_column_width=True)
        te="ఫోటో చూశాను, డాక్టర్‌కి చూపించండి, శుభ్రంగా ఉంచండి."; hi="फोटो देख ली, डॉक्टर को दिखाइए, साफ रखिए।"; en="Seen photo, show to doctor, keep clean."
        st.markdown(f"<p style='color:#92FE9D'>తెలుగు: {te}</p><p style='color:#FFD93D'>हिंदी: {hi}</p><p style='color:#00E5FF'>English: {en}</p>", unsafe_allow_html=True)
        speak_sequential(te, hi, en)
