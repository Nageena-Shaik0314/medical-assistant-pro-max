import streamlit as st, base64
from PIL import Image
from gtts import gTTS

st.set_page_config(page_title="AI MEDICAL ASSISTANT", layout="wide")

st.markdown("<h1 style='text-align:center;'>🩺 AI MEDICAL ASSISTANT 🌈</h1><p style='text-align:center;color:gray;'>తెలుగు | हिंदी | English</p>", unsafe_allow_html=True)

def speak_sequential(te_text, hi_text, en_text):
    try:
        # Telugu
        tts_te = gTTS(text=te_text, lang='te', slow=False)
        tts_te.save("te.mp3")
        # Hindi
        tts_hi = gTTS(text=hi_text, lang='hi', slow=False)
        tts_hi.save("hi.mp3")
        # English
        tts_en = gTTS(text=en_text, lang='en', slow=False)
        tts_en.save("en.mp3")

        # Play one by one - No pydub needed, so no ffmpeg error!
        st.markdown("<p style='text-align:center'>🎧 <b>Okati tharvatha okati vinandi - Telugu -> Hindi -> English</b></p>", unsafe_allow_html=True)
        st.audio("te.mp3", format="audio/mp3")
        st.audio("hi.mp3", format="audio/mp3")
        st.audio("en.mp3", format="audio/mp3")
        
    except Exception as e:
        st.error(f"Voice Error: {e}. Internet check chey, gTTS ki net kavali.")

# Native script DB - No emojis inside
SYMPTOMS_DB = {
"fever": {"te": "నమస్తే, మీకు జ్వరం ఉంది. డోలో 650 తీసుకోండి, విశ్రాంతి, చల్లని గుడ్డ, 3-4 లీటర్ల నీరు, ఫ్యాన్ వద్దు, మందు షేర్ వద్దు.", "hi": "नमस्ते, आपको बुखार है। डोलो 650 लीजिए, आराम, ठंडी पट्टी, 3-4 लीटर पानी, फैन नहीं, शेयर नहीं।", "en": "Hello, you have Fever. Dolo 650, rest, cold cloth, 3-4L water, no fan, dont share medicine."},
"cold": {"te": "నమస్తే, మీకు జలుబు ఉంది. సెట్రిజిన్ రాత్రి, ఆవిరి 2 సార్లు, వెచ్చని బట్టలు, చల్లని నీరు 5 రోజులు వద్దు.", "hi": "नमस्ते, आपको जुकाम है। सेट्रिजिन रात में, भाप 2 बार, गरम कपड़े, ठंडा पानी 5 दिन नहीं।", "en": "Hello, you have Cold. Cetrizine at night, steam twice, warm clothes, no cold water 5 days."},
"cough": {"te": "నమస్తే, మీకు దగ్గు ఉంది. అస్కోరిల్ సిరప్, ఆవిరి, తేనె మిరియం, చల్లనివి వద్దు, మాస్క్.", "hi": "नमस्ते, आपको खांसी है। एस्कोरिल सिरप, भाप, शहद, ठंडा नहीं, मास्क।", "en": "Hello, you have Cough. Ascoril syrup, steam, honey, no cold items, mask."},
"headache": {"te": "నమస్తే, తలనొప్పి ఉంది. డోలో 650, చీకటి గదిలో విశ్రాంతి, ఫోన్ వద్దు, 3 లీటర్ల నీరు, నిద్ర.", "hi": "नमस्ते, सिरदर्द है। डोलो 650, अंधेरे कमरे में आराम, फोन नहीं, 3 लीटर पानी, नींद।", "en": "Hello, Headache. Dolo 650, rest in dark room, no phone, 3L water, sleep."},
"stomach pain": {"te": "నమస్తే, కడుపు నొప్పి ఉంది. గ్యాస్ టాబ్లెట్, వేడి నీరు, గోరువెచ్చని నీరు, నూనె పదార్థాలు వద్దు, ఖాళీ కడుపు వద్దు.", "hi": "नमस्ते, पेट दर्द है। गैस टेबलेट, गरम पानी, तेल मसाला नहीं, खाली पेट नहीं।", "en": "Hello, Stomach Pain. Gas tablet, warm water, no oily food, dont keep empty stomach."},
"chest pain": {"te": "నమస్తే, ఛాతీ నొప్పి ప్రమాదం. వెంటనే 108 కి కాల్ చేయండి, నడవద్దు, విశ్రాంతి, డాక్టర్ దగ్గరకు వెళ్ళండి.", "hi": "नमस्ते, सीने में दर्द खतरा। तुरंत 108 पर कॉल करें, चलें नहीं, आराम, डॉक्टर के पास जाएं।", "en": "Hello, Chest Pain is risky. Call 108 immediately, dont walk, rest, go to doctor."},
"back pain": {"te": "నమస్తే, నడుము నొప్పి ఉంది. వేడి కాపడం, వంగవద్దు, బరువు ఎత్తవద్దు, నిటారుగా కూర్చోండి, వ్యాయామం.", "hi": "नमस्ते, कमर दर्द है। गरम सिकाई, झुकें नहीं, वजन न उठाएं, सीधा बैठें।", "en": "Hello, Back Pain. Hot pack, dont bend, dont lift weight, sit straight."},
"knee pain": {"te": "నమస్తే, మోకాలు నొప్పి ఉంది. వేడి కాపడం, నడవడం తగ్గించండి, బరువు తగ్గండి, వైద్యుడిని కలవండి.", "hi": "नमस्ते, घुटने में दर्द है। गरम सिकाई, चलना कम करें, वजन घटाएं।", "en": "Hello, Knee Pain. Hot pack, reduce walking, reduce weight, consult doctor."},
"diabetes": {"te": "నమస్తే, షుగర్ ఉంది. తీపి వద్దు, రోజూ 30 నిమిషాలు నడవండి, మందు మానవద్దు, క్రమం తప్పకుండా చెక్.", "hi": "नमस्ते, शुगर है। मीठा नहीं, रोज 30 मिनट चलें, दवा न छोड़ें, नियमित जांच।", "en": "Hello, Diabetes. No sugar, walk 30 min daily, dont stop medicine, regular checkup."},
"bp high": {"te": "నమస్తే, బీపీ ఎక్కువ ఉంది. ఉప్పు తగ్గించండి, కోపం వద్దు, నడవండి, మందు క్రమంగా వేసుకోండి, టెన్షన్ వద్దు.", "hi": "नमस्ते, बीपी ज्यादा है। नमक कम करें, गुस्सा नहीं, चलें, दवा समय पर लें।", "en": "Hello, High BP. Reduce salt, no anger, walk, take medicine regularly, no tension."},
"bp low": {"te": "నమస్తే, బీపీ తక్కువ ఉంది. ఉప్పు నీరు తాగండి, పడుకోండి, కాళ్ళు పైకి పెట్టండి, ఓఆర్ఎస్ తాగండి.", "hi": "नमस्ते, बीपी कम है। नमक पानी पिएं, लेट जाएं, पैर ऊपर रखें, ओआरएस पिएं।", "en": "Hello, Low BP. Drink salt water, lie down, keep legs up, drink ORS."},
"acidity": {"te": "నమస్తే, గ్యాస్ ఆమ్లం ఉంది. పాన్ డి, కారం వద్దు, టీ కాఫీ వద్దు, సమయానికి తినండి, 3 లీటర్ల నీరు.", "hi": "नमस्ते, एसिडिटी है। पैन डी, मिर्च नहीं, चाय कॉफी नहीं, समय पर खाएं।", "en": "Hello, Acidity. Pan D, no spice, no tea coffee, eat on time, 3L water."},
"vomiting": {"te": "నమస్తే, వాంతులు ఉన్నాయి. ఓఆర్ఎస్, ఎమ్సెట్, కొద్దిగా కొద్దిగా నీరు, నూనె వద్దు, వైద్యుడిని కలవండి.", "hi": "नमस्ते, उल्टी है। ओआरएस, एमसेट, थोड़ा थोड़ा पानी, तेल नहीं, डॉक्टर से मिलें।", "en": "Hello, Vomiting. ORS, Emset, small sips water, no oil, consult doctor."},
"diarrhea": {"te": "నమస్తే, విరేచనాలు ఉన్నాయి. ఓఆర్ఎస్ ఎక్కువగా తాగండి, పెరుగు అన్నం, బయట తిండి వద్దు, చేతులు కడుక్కోండి.", "hi": "नमस्ते, दस्त हैं। ओआरएस ज्यादा पिएं, दही चावल, बाहर का खाना नहीं, हाथ धोएं।", "en": "Hello, Diarrhea. Drink more ORS, curd rice, no outside food, wash hands."},
"constipation": {"te": "నమస్తే, మలబద్ధకం ఉంది. నీరు ఎక్కువ తాగండి, పీచు పదార్థాలు, అరటిపండు, బొప్పాయి, నడవండి.", "hi": "नमस्ते, कब्ज है। पानी ज्यादा पिएं, फाइबर, केला, पपीता, चलें।", "en": "Hello, Constipation. Drink more water, fiber foods, banana, papaya, walk."},
"throat pain": {"te": "నమస్తే, గొంతు నొప్పి ఉంది. ఉప్పు నీటితో పుక్కిలించండి, గోరువెచ్చని నీరు, చల్లనివి వద్దు, మాట తగ్గించండి.", "hi": "नमस्ते, गले में दर्द है। नमक पानी से गरारे, गुनगुना पानी, ठंडा नहीं, बोलना कम।", "en": "Hello, Throat Pain. Salt water gargle, warm water, no cold, talk less."},
"eye pain": {"te": "నమస్తే, కంటి నొప్పి ఉంది. ఫోన్ తగ్గించండి, చల్లని నీటితో కడగండి, కళ్ళు నలపవద్దు, డాక్టర్‌ను కలవండి.", "hi": "नमस्ते, आंख में दर्द है। फोन कम करें, ठंडे पानी से धोएं, मलें नहीं, डॉक्टर से मिलें।", "en": "Hello, Eye Pain. Reduce phone, wash with cold water, dont rub, consult doctor."},
"ear pain": {"te": "నమస్తే, చెవి నొప్పి ఉంది. చెవిలో ఏమీ పెట్టవద్దు, నీరు పోనివ్వవద్దు, వేడి కాపడం, డాక్టర్‌ను కలవండి.", "hi": "नमस्ते, कान में दर्द है। कान में कुछ न डालें, पानी न जाने दें, गरम सिकाई, डॉक्टर से मिलें।", "en": "Hello, Ear Pain. Dont put anything in ear, no water, hot pack, consult doctor."},
"skin allergy": {"te": "నమస్తే, చర్మ అలెర్జీ ఉంది. దురద పెట్టవద్దు, సబ్బు మార్చండి, దుమ్ము వద్దు, సెట్రిజిన్, శుభ్రంగా ఉండండి.", "hi": "नमस्ते, स्किन एलर्जी है। खुजलाएं नहीं, साबुन बदलें, धूल नहीं, सेट्रिजिन, साफ रहें।", "en": "Hello, Skin Allergy. Dont scratch, change soap, no dust, cetrizine, stay clean."},
"dandruff": {"te": "నమస్తే, చుండ్రు ఉంది. తల శుభ్రంగా ఉంచండి, నూనె తగ్గించండి, యాంటీ డాండ్రఫ్ షాంపూ వాడండి.", "hi": "नमस्ते, रूसी है। सिर साफ रखें, तेल कम करें, एंटी डैंड्रफ शैम्पू।", "en": "Hello, Dandruff. Keep head clean, reduce oil, use anti dandruff shampoo."},
"hair fall": {"te": "నమస్తే, జుట్టు రాలుతుంది. టెన్షన్ తగ్గించండి, ప్రోటీన్ తినండి, నూనె మసాజ్, నిద్ర సరిగా పడుకోండి.", "hi": "नमस्ते, बाल झड़ रहे हैं। टेंशन कम करें, प्रोटीन खाएं, तेल मालिश, नींद पूरी लें।", "en": "Hello, Hair Fall. Reduce tension, eat protein, oil massage, proper sleep."},
"weight loss": {"te": "నమస్తే, బరువు తగ్గాలి. నడక 45 నిమిషాలు, నూనె తీపి వద్దు, నీరు ఎక్కువ, రాత్రి తక్కువ తినండి.", "hi": "नमस्ते, वजन घटाना है। 45 मिनट चलें, तेल मीठा नहीं, पानी ज्यादा, रात कम खाएं।", "en": "Hello, Weight Loss. Walk 45 min, no oil sugar, more water, eat less at night."},
"weight gain": {"te": "నమస్తే, బరువు పెరగాలి. ప్రోటీన్ ఎక్కువ, పాలు గుడ్లు, వ్యాయామం, సమయానికి తినండి, నిద్ర.", "hi": "नमस्ते, वजन बढ़ाना है। प्रोटीन ज्यादा, दूध अंडे, व्यायाम, समय पर खाएं।", "en": "Hello, Weight Gain. More protein, milk eggs, exercise, eat on time, sleep."},
"sleeplessness": {"te": "నమస్తే, నిద్ర పట్టడం లేదు. రాత్రి 10 గంటలకు పడుకోండి, ఫోన్ వద్దు, వేడి పాలు, టెన్షన్ వద్దు, ధ్యానం.", "hi": "नमस्ते, नींद नहीं आती। रात 10 बजे सोएं, फोन नहीं, गरम दूध, टेंशन नहीं, ध्यान।", "en": "Hello, Sleeplessness. Sleep at 10pm, no phone, warm milk, no tension, meditation."},
"stress": {"te": "నమస్తే, ఒత్తిడి ఉంది. ధ్యానం చేయండి, నడవండి, సంగీతం వినండి, ఫోన్ తగ్గించండి, కుటుంబంతో మాట్లాడండి.", "hi": "नमस्ते, तनाव है। ध्यान करें, चलें, संगीत सुनें, फोन कम करें, परिवार से बात करें।", "en": "Hello, Stress. Meditate, walk, listen music, reduce phone, talk with family."},
"body pain": {"te": "నమస్తే, ఒళ్ళు నొప్పులు ఉన్నాయి. విశ్రాంతి, వేడి నీటి స్నానం, డోలో, నీరు ఎక్కువ తాగండి, బరువు వద్దు.", "hi": "नमस्ते, बदन दर्द है। आराम, गरम पानी से नहाएं, डोलो, पानी ज्यादा पिएं।", "en": "Hello, Body Pain. Rest, hot water bath, Dolo, drink more water, no weight lifting."},
"leg swelling": {"te": "నమస్తే, కాలు వాపు ఉంది. కాలు పైకి పెట్టండి, ఉప్పు తగ్గించండి, నడవండి, బీపీ చెక్ చేయించండి, డాక్టర్‌ను కలవండి.", "hi": "नमस्ते, पैर में सूजन है। पैर ऊपर रखें, नमक कम करें, चलें, बीपी जांच, डॉक्टर से मिलें।", "en": "Hello, Leg Swelling. Keep leg up, reduce salt, walk, check BP, consult doctor."},
"dehydration": {"te": "నమస్తే, నీరసం నీళ్ళు తక్కువ. ఓఆర్ఎస్, కొబ్బరి నీళ్ళు, 3-4 లీటర్ల నీరు, ఎండలో తిరగవద్దు, మజ్జిగ.", "hi": "नमस्ते, पानी की कमी। ओआरएस, नारियल पानी, 3-4 लीटर पानी, धूप में न जाएं, छाछ।", "en": "Hello, Dehydration. ORS, coconut water, 3-4L water, dont roam in sun, buttermilk."},
"urine infection": {"te": "నమస్తే, మూత్ర ఇన్ఫెక్షన్ ఉంది. నీరు 4 లీటర్లు తాగండి, మూత్రం ఆపవద్దు, శుభ్రత, పుల్లనివి తగ్గించండి, డాక్టర్‌ను కలవండి.", "hi": "नमस्ते, यूरिन इन्फेक्शन है। 4 लीटर पानी पिएं, पेशाब न रोकें, सफाई, खट्टा कम करें, डॉक्टर से मिलें।", "en": "Hello, Urine Infection. Drink 4L water, dont hold urine, hygiene, reduce sour, consult doctor."},
"cold hands": {"te": "నమస్తే, చేతులు చల్లగా ఉన్నాయి. వెచ్చని బట్టలు, వేడి నీరు, రక్త పరీక్ష చేయించండి, టీ తాగండి.", "hi": "नमस्ते, हाथ ठंडे हैं। गरम कपड़े, गरम पानी, खून जांच, चाय पिएं।", "en": "Hello, Cold Hands. Warm clothes, warm water, blood test, drink tea."},
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
