import streamlit as st
from datetime import datetime
from gtts import gTTS
import os
from PIL import Image
import speech_recognition as sr
import tempfile
import re

st.set_page_config(page_title="Family Doctor - Tiruvuru", layout="wide", page_icon="👨‍⚕️")

st.markdown("""
<style>
.main-title {text-align:center; background:linear-gradient(90deg,#00C9FF,#92FE9D); padding:22px; border-radius:18px; color:#000; font-size:28px; font-weight:bold;}
.card {background:#1A1A1A; padding:18px; border-radius:16px; border-left:6px solid #4CAF50; margin:12px 0;}
</style>
<div class='main-title'>👨‍⚕️ MEE FAMILY DOCTOR - TIRUVURU<br><small>🙏 Gouravam tho | 🛡️ 8 Precautions tho | Auto Language</small></div>
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
    if any(w in text.lower() for w in ['jwaram','jalu','daggu','naku','naaku','garu']): return 'te'
    if any(w in text.lower() for w in ['bukhar','zukam','khansi','mujhe','krupaya']): return 'hi'
    return 'en'

SYMPTOMS_DB = {
    "fever": {
        "te": """Namaste garu, meeku jwaram vachindani telisindi, dayachesi bhayapadakandi.

**💊 Mandu:** Dolo 650 tablet bhojanam tarvata roju 2 sarlu.

**🛡️ 8 Jagratthalu - Dayachesi patinchandi:**
1. 2 rojulu poorthi vishranti, bayata tirugakandi.
2. Prathi 2 gantalaki nuvvutipa pai challani thati gudda.
3. Challa neetitho snanam vaddu, goruvecchi neetitho cheyandi.
4. Mask pettukondi, intlo pillalaki daggara ga vellakandi.
5. Roju 3-4 liters neeru, kobbari neeru tappakunda tagandi.
6. Fan kindha direct ga padukokandi, chematalu ekkuva raakunda.
7. Oka manishi tho matrame mandu share chesukokandi.
8. Jwaram tho paatu vomits, loose motion unte ventane hospital ki randi.

**🥗 Aharam:** Khichdi, java, kobbari neeru, battayi, dhanimma pandlu. Noone, karam, biryani, cool drinks vaddu.

**🏥 Eppudu ravali:** 2 rojula tarvata thagakapotey, 102°F ekkuva unte, vomits unte Tiruvuru Govt Hospital ki randi garu.""",
        "hi": """Namaste, aapko bukhar hai, kripya chinta mat kijiye.

**💊 Dawai:** Dolo 650 khane ke baad din me 2 baar.

**🛡️ 8 Savdhaniyan:**
1. 2 din poora aaram, bahar mat jaiye.
2. Har 2 ghante maathe par thanda patti.
3. Thande pani se nahana nahi, halke garam se.
4. Mask pehniye, bacchon se doori.
5. 3-4 liter pani, nariyal pani.
6. Direct fan ke neeche mat soiye.
7. Dawai share mat kijiye.
8. Bukhar ke saath ulti, dast ho to turant hospital.

**🥗 Aahar:** Khichdi, dalia, nariyal pani, mausambi. Tel masala, biryani, cold drink nahi.
**🏥 Kab:** 2 din me thik na ho, 102°F se zyada ho to Tiruvuru hospital aaiye.""",
        "en": """Namaste, please don't worry, you have fever.

**💊 Medicine:** Dolo 650 after food 2 times daily.

**🛡️ 8 Precautions - Please follow:**
1. Take complete rest for 2 days, don't go outside.
2. Keep cold wet cloth on forehead every 2 hours.
3. Don't bath with cold water, use lukewarm only.
4. Wear mask, keep distance from children at home.
5. Drink 3-4 liters water, coconut water daily.
6. Don't sleep directly under fan.
7. Don't share medicines.
8. If fever with vomiting, loose motion, visit hospital immediately.

**🥗 Diet:** Khichdi, porridge, coconut water, orange, pomegranate. Avoid oily, spicy, biryani, cool drinks.
**🏥 When to visit:** If not reduced in 2 days, above 102°F, with vomiting, visit Tiruvuru Govt Hospital. Take care garu."""
    },
    "cold": {
        "te": """Namaste garu, meeku jalubu.

**💊 Mandu:** Cetzine rathri 1, Vicks chest paina.

**🛡️ 8 Jagratthalu:**
1. Roju 2 sarlu aaviri, towel kappukoni 10 nimishalu.
2. Vecchani battalu, sweater vesukondi.
3. Challa neeru, ice cream, cool drinks 5 rojulu vaddu.
4. Fan, AC direct ga vaddu, dust unna chota ki vellakandi.
5. Chethi rumal tho nose clean chesukondi, bayata veyakandi.
6. Pillalaki, pedda vallaki daggara ga vellakandi - vyapisthundi.
7. Goruvecchi neeru mathrame tagandi.
8. Thummu vachinappudu chethi addupettukondi.

**🥗 Aharam:** Vedi allam tea, tulasi tea, vedi soup, karam tho pappu charu.
**🏥 Eppudu:** 5 rojula kanna ekkuva, jwaram tho unte hospital ki randi.""",
        "hi": """Namaste, aapko zukam hai.

**💊 Dawai:** Cetzine raat me 1, Vicks chest par.

**🛡️ 8 Savdhaniyan:**
1. Din me 2 baar bhaap 10 min.
2. Garam kapde, sweater pehniye.
3. Thanda pani, ice cream, cold drink 5 din nahi.
4. Fan, AC direct nahi, dhool me mat jaiye.
5. Rumaal se naak saaf kijiye.
6. Bacchon, buzurgon se doori.
7. Garam pani hi pijiye.
8. Cheenk aaye to hath aage rakhiye.

**🥗 Aahar:** Garam adrak chai, tulsi chai, garam soup.
**🏥 Kab:** 5 din se zyada bukhar ke saath ho to hospital.""",
        "en": """Namaste, you have cold.

**💊 Medicine:** Cetzine at night 1, Vicks on chest.

**🛡️ 8 Precautions:**
1. Steam 2 times daily 10 min covering head.
2. Wear warm clothes, sweater.
3. No cold water, ice cream, cool drinks for 5 days.
4. Avoid direct fan, AC, dusty area.
5. Use handkerchief for nose, dispose properly.
6. Keep distance from kids, elders - contagious.
7. Drink only warm water.
8. Cover mouth when sneezing.

**🥗 Diet:** Hot ginger tea, tulsi tea, hot soup, pepper rasam.
**🏥 When:** More than 5 days with fever, visit hospital."""
    },
    "cough": {
        "te": """Namaste garu, meeku daggu.

**💊 Mandu:** Ascoril syrup roju 2 sarlu, thene allam.

**🛡️ 8 Jagratthalu:**
1. Uppu neetitho roju 3 sarlu pukkilinchandi.
2. Mask tappakunda pettukondi, bayata ummiveyakandi.
3. Challa neeru, dust, poga, beedi smoke daggara ki vellakandi.
4. Thala ethuga petti nidra pondandi, straight ga padukokandi.
5. Chethi tho noru moosi daggu randi, bayata cheyakandi.
6. Roju 3 liters goruvecchi neeru tagandi.
7. Vepudu, cool drinks, ice cream vaddu.
8. Daggu tho paatu raktham vaste ventane hospital.

**🥗 Aharam:** Then e, allam, goruvecchi neeru, thippateega. Vepudu vaddu.
**🏥 Eppudu:** 7 rojula kanna ekkuva, raktham tho unte ventane Tiruvuru hospital ki randi.""",
        "hi": """Namaste, aapko khansi hai.

**💊 Dawai:** Ascoril 2 baar, shahad adrak.

**🛡️ 8 Savdhaniyan:**
1. Namak pani se 3 baar garare.
2. Mask pehniye, bahar mat thukiye.
3. Thanda pani, dhool, dhua, beedi se bachiye.
4. Sir uncha rakh ke soiye.
5. Haath se muh dhak ke khansi kijiye.
6. 3 liter garam pani pijiye.
7. Tala hua, cold drink, ice cream nahi.
8. Khoon ke saath khansi ho to turant hospital.

**🥗 Aahar:** Shahad, adrak, garam pani.
**🏥 Kab:** 7 din se zyada, khoon ke saath ho to turant hospital.""",
        "en": """Namaste, you have cough.

**💊 Medicine:** Ascoril syrup 2 times, honey ginger.

**🛡️ 8 Precautions:**
1. Salt water gargle 3 times daily.
2. Wear mask always, don't spit in public.
3. Avoid cold water, dust, smoke, beedi.
4. Sleep with head elevated, not flat.
5. Cover mouth with hand when coughing.
6. Drink 3 liters warm water.
7. No fried, cool drinks, ice cream.
8. If blood with cough, visit hospital immediately.

**🥗 Diet:** Honey, ginger, warm water, pepper.
**🏥 When:** More than 7 days or blood with cough, visit Tiruvuru hospital immediately."""
    },
    "stomach": {
        "te": """Namaste garu, kadupu noppi.

**💊 Mandu:** Digene tablet, jeelakarra neeru.

**🛡️ 8 Jagratthalu:**
1. Karam, noone, masala, biryani, street food 5 rojulu vaddu.
2. Roju 3 liters neeru, majjiga ekkuva tagandi.
3. Time ki bhojanam cheyandi, aakali tho undakandi.
4. Bayata food, pani puri, cool drinks vaddu.
5. Aavakai, non-veg, egg vaddu ippudu.
6. Nidra sarigga pondandi, tension padakandi.
7. Bhojanam taruvata 10 nimishalu nadavandi.
8. Noppi ekkuva unte, vomits unte hospital ki randi.

**🥗 Aharam:** Perugu annam, arati, majjiga, khichdi. Thelikaina aharam.
**🏥 Eppudu:** 2 rojula kanna ekkuva noppi unte hospital.""",
        "hi": """Namaste, pet dard hai.

**💊 Dawai:** Digene, jeera pani.

**🛡️ 8 Savdhaniyan:**
1. Tikha, tel, masala, biryani, street food 5 din nahi.
2. 3 liter pani, chaas pijiye.
3. Time par khaiye, bhooka mat rahiye.
4. Bahar ka khana, pani puri, cold drink nahi.
5. Achar, non-veg, anda nahi.
6. Neend poori lijiye, tension nahi.
7. Khane ke baad 10 min chaliye.
8. Dard zyada ho, ulti ho to hospital.

**🥗 Aahar:** Dahi chawal, kela, chaas, khichdi. Halka bhojan.
**🏥 Kab:** 2 din se zyada dard ho to hospital.""",
        "en": """Namaste, stomach pain.

**💊 Medicine:** Digene tablet, cumin water.

**🛡️ 8 Precautions:**
1. No spicy, oily, masala, biryani, street food for 5 days.
2. Drink 3 liters water, buttermilk more.
3. Eat on time, don't stay hungry.
4. No outside food, pani puri, cool drinks.
5. No pickle, non-veg, egg now.
6. Sleep properly, don't take tension.
7. Walk 10 min after food.
8. If severe pain, vomiting, visit hospital.

**🥗 Diet:** Curd rice, banana, buttermilk, khichdi. Light food.
**🏥 When:** Pain more than 2 days, visit hospital."""
    },
}

def get_reply_fixed(q):
    ql = q.lower()
    for k in SYMPTOMS_DB:
        if k in ql:
            d = SYMPTOMS_DB[k]
            return d["en"], d["te"], d["hi"]
    return (
        f"Namaste, you have {q}. Rest, 3L water, 8h sleep, light food. Avoid cold, oily, spicy, outside food, smoking, alcohol. Take steam if needed, wear mask, wash hands. If 2 days not reducing, visit Tiruvuru Hospital. Take care.",
        f"Namaste garu, meeku {q} undani telisindi. Vishranti, 3L neeru, 8 gantalu nidra, thelikaina aharam. Challa neeru, noone, karam, bayata food, smoking, alcohol vaddu. Aaviri teesukondi, mask pettukondi, chethulu kadukondi. 2 rojula tarvata hospital ki randi. Jagrattha garu.",
        f"Namaste, aapko {q} hai. Aaram, 3L pani, 8 ghante neend, halka bhojan. Thanda, tel masala, bahar ka khana, smoking, alcohol avoid. Bhaap lijiye, mask pehniye, haath dhoiye. 2 din me thik na ho to hospital jaiye."
    )

feature = st.sidebar.selectbox("📋 SELECT",["👨‍⚕️ Family Doctor","💊 Medicine Info","🧘 Health Tips","🚨 Emergency 108","📸 Image Analyzer"])

if feature == "👨‍⚕️ Family Doctor":
    st.markdown("<div class='card'><h3 style='text-align:center;'>👨‍⚕️ Mee Family Doctor - 8 Precautions tho</h3></div>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        st.write("### 🎤 Voice lo adagandi garu")
        user_audio = st.audio_input("🎤 Mic...")
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
                st.success(f"✅ Meeru cheppindi: **{text}**")
                eng,tel,hin = get_reply_fixed(text)
                if lang=='te': st.chat_message("assistant").write(tel); speak_single(tel,'te')
                elif lang=='hi': st.chat_message("assistant").write(hin); speak_single(hin,'hi')
                else: st.chat_message("assistant").write(eng); speak_single(eng,'en')
            except: st.warning("Malli cheppandi garu.")
    with c2:
        st.write("### ⌨️ Type cheyandi garu")
        q = st.chat_input("Adagandi...")
        if q:
            lang = detect_language(q)
            st.chat_message("user").write(q)
            eng,tel,hin = get_reply_fixed(q)
            if lang=='te': st.chat_message("assistant").write(tel); speak_single(tel,'te')
            elif lang=='hi': st.chat_message("assistant").write(hin); speak_single(hin,'hi')
            else: st.chat_message("assistant").write(eng); speak_single(eng,'en')
            st.download_button("📄 Download", data=f"{eng}\n\n{tel}\n\n{hin}", file_name="Prescription.txt")

elif feature == "💊 Medicine Info":
    st.subheader("💊 Medicine Info - Precautions tho")
    st.info("Prathi mandu ki precautions untai - Doctor garu chepinatte vesukondi garu.")
elif feature == "🧘 Health Tips":
    st.info("**8 Precautions for Healthy Life:**\n1. 30 min walk\n2. 15 min yoga\n3. 3L water\n4. 8h sleep\n5. No smoking/alcohol\n6. Wash hands\n7. Wear mask in dust\n8. Time ki food")
elif feature == "🚨 Emergency 108":
    st.error("🚨 108 - Emergency - Dayachesi 8 precautions: 1. Bhayapadakandi 2. 108 ki call 3. Patient ni kadalakandi 4. Tight clothes vadilinchandi 5. Bleeding unte cloth tho nokkandi 6. Hospital ki teesukellandi 7. Old medicines chupinchandi 8. Doctor ki nijam cheppandi")
elif feature == "📸 Image Analyzer":
    st.subheader("📸 Image Analyzer")
    img = st.file_uploader("Upload", type=["jpg","png","jpeg"])
    if img: st.image(Image.open(img), use_column_width=True)
