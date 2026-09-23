import streamlit as st
from gtts import gTTS
import os, re, tempfile
from PIL import Image
import speech_recognition as sr

st.set_page_config(page_title="AI Medical Assistant App", page_icon="🏥", layout="wide")

st.markdown("""
<style>
.main-title {
    text-align:center;
    background:linear-gradient(90deg,#00C9FF,#92FE9D);
    padding:18px; border-radius:15px;
    color:#000; font-size:26px; font-weight:bold;
    margin-bottom:30px;
    box-shadow: 0 4px 15px rgba(0,201,255,0.3);
}
.beauty-card {
    background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
    padding:25px; border-radius:20px;
    border: 1px solid #00C9FF;
    box-shadow: 0 8px 32px rgba(0,201,255,0.2);
    margin:10px;
}
</style>
<div class='main-title'>🏥 AI Medical Assistant App - Tiruvuru Govt Hospital</div>
""", unsafe_allow_html=True)

def speak_single(text, lang_code):
    try:
        if os.path.exists("voice.mp3"): os.remove("voice.mp3")
        tts = gTTS(text=text[:600], lang=lang_code, slow=False)
        tts.save("voice.mp3")
        with open("voice.mp3","rb") as f: st.audio(f.read(), format="audio/mp3", autoplay=True)
        os.remove("voice.mp3")
    except: pass

def detect_language(text):
    if re.search(r'[\u0C00-\u0C7F]', text): return 'te'
    if re.search(r'[\u0900-\u097F]', text): return 'hi'
    if any(w in text.lower() for w in ['jwaram','jalu','daggu','naku','garu','kadupu','noppi']): return 'te'
    if any(w in text.lower() for w in ['bukhar','zukam','khansi','mujhe']): return 'hi'
    return 'en'

SYMPTOMS_DB = {
    "fever": {"te": "Jwaram. Dolo 650 tharuvata. 1.Vishranti 2.Challani gudda 3.Challa snanam vaddu 4.Mask 5.3-4L neeru 6.Fan vaddu 7.Mandu share vaddu 8.Vantulu unte hospital. Aharam: Khichdi, ganji", "hi": "Bukhar. Dolo 650. 1.Aaram 2.Thanda patti 3.Thanda pani nahi 4.Mask 5.3-4L pani 6.Fan nahi 7.Share nahi 8.Ulti to hospital.", "en": "Fever. Dolo 650. 1.Rest 2.Cold cloth 3.No cold bath 4.Mask 5.3-4L water 6.No fan 7.Dont share 8.If vomit hospital."},
    "cold": {"te": "Jalubu. Cetrizine night. 1.Aaviri 2 sarlu 2.Vecchani battalu 3.Challa neeru 5 rojulu vaddu 4.Dust vaddu 5.Rumal 6.Pillala daggara vaddu 7.Goruvecchi neeru 8.Thummu lo chethi", "hi": "Zukam. Cetrizine. 1.Bhaap 2.Garam kapde 3.Thanda pani 5 din nahi 4.Dhool nahi 5.Rumaal 6.Baccho se doori 7.Garam pani 8.Cheenk me haath", "en": "Cold. Cetrizine. 1.Steam 2.Warm clothes 3.No cold water 5 days 4.No dust 5.Hanky 6.Away kids 7.Warm water 8.Cover sneeze"},
    "cough": {"te": "Daggu. Ascoril. 1.Aaviri 2.Honey+miriyam 3.Challa vaddu 4.Dust mask 5.Goruvecchi neeru 6.Pillala ki dooram 7.Daggetappudu chethi 8.7 rojulu unte hospital", "hi": "Khansi. Ascoril. 1.Bhaap 2.Shahad 3.Thanda nahi 4.Mask 5.Garam pani 6.Baccho se door 7.Khanste haath 8.7 din to hospital", "en": "Cough. Ascoril. 1.Steam 2.Honey 3.No cold 4.Mask 5.Warm water 6.Away kids 7.Cover 8.If >7 days hospital"},
    "headache": {"te": "Thala noppi. Dolo 650. 1.Chikati gadi rest 2.Phone vaddu 3.3L neeru 4.Tea thakkuva 5.8h nidra 6.Oli vaddu 7.Massage 8.2 rojulu thaggakapothe hospital", "hi": "Sir dard. Dolo 650. 1.Andhere me aaram 2.Phone nahi 3.3L pani 4.Chai kam 5.8h neend 6.Shore nahi 7.Massage 8.2 din nahi to hospital", "en": "Headache. Dolo 650. 1.Dark room rest 2.No phone 3.3L water 4.Less tea 5.8h sleep 6.No noise 7.Massage 8.If 2 days hospital"},
    "stomach pain": {"te": "Kadupu noppi. Cyclopam, Gelusil. 1.Ganji 2.Oily vaddu 3.Hot bag 10 min 4.Left side 5.Gattiga nakakandi 6.2h emi vaddhu 7.Clockwise massage 8.6h pain unte hospital", "hi": "Pet dard. Cyclopam. 1.Ganji 2.Oily nahi 3.Hot bag 4.Left side 5.Press nahi 6.2h kuch nahi 7.Massage 8.6h dard to hospital", "en": "Stomach pain. Cyclopam. 1.Kanji only 2.No oily 3.Hot bag 4.Left side 5.Dont press 6.Nothing 2h 7.Massage 8.If >6h hospital"},
    "vomiting": {"te": "Vantulu. Vomikind 4mg. 1.30min emi vaddhu 2.ORS koncham 3.Noru kadukko 4.Perfume vaddu 5.Travel vaddu 6.Left side 7.Biryani vaddu 8.3-4 sarlu unte hospital", "hi": "Ulti. Vomikind. 1.30min kuch nahi 2.ORS thoda 3.Muh dho 4.Khushboo nahi 5.Travel nahi 6.Left side 7.Biryani nahi 8.3-4 se zyada hospital", "en": "Vomiting. Vomikind. 1.Nothing 30min 2.Sip ORS 3.Wash mouth 4.No smell 5.No travel 6.Left side 7.No biryani 8.If >3-4 hospital"},
    "diarrhea": {"te": "Virarechana. ORS, Econorm. 1.ORS ekkuva 2.Ganji 3.Perugu annam 4.Bayata food vaddu 5.Paalu vaddu 6.Chethulu kadukko 7.Mask 8.Blood unte hospital", "hi": "Dast. ORS. 1.ORS zyada 2.Ganji 3.Dahi chawal 4.Bahar khana nahi 5.Doodh nahi 6.Haath dho 7.Mask 8.Khoon to hospital", "en": "Diarrhea. ORS. 1.More ORS 2.Kanji 3.Curd rice 4.No outside food 5.No milk 6.Wash hands 7.Mask 8.If blood hospital"},
    "constipation": {"te": "Malabaddhakam. 1.3-4L neeru 2.Papaya, kela 3.Walk 30min 4.Time ki food 5.Oily thakkuva 6.Masala vaddu 7.Maidha vaddu 8.3 rojulu unte hospital", "hi": "Kabz. 1.3-4L pani 2.Papita kela 3.Walk 30min 4.Time par khana 5.Oily kam 6.Masala nahi 7.Maida nahi 8.3 din to hospital", "en": "Constipation. 1.3-4L water 2.Papaya banana 3.Walk 30min 4.Timely food 5.Less oily 6.No masala 7.No maida 8.If 3 days hospital"},
    "acidity": {"te": "Acidity. Pan 40 morning. 1.Khali kadupu vaddu 2.Karam vaddu 3.Tea coffee vaddu 4.Time ki tinali 5.Chintala vaddu 6.Nidra 8h 7.Oily vaddu 8.Blood vanti unte hospital", "hi": "Acidity. Pan 40. 1.Khali pet nahi 2.Mirch nahi 3.Chai coffee nahi 4.Time par khao 5.Tension nahi 6.8h neend 7.Oily nahi 8.Khoon ulti to hospital", "en": "Acidity. Pan 40 morning. 1.No empty stomach 2.No spicy 3.No tea coffee 4.Timely eat 5.No tension 6.8h sleep 7.No oily 8.If blood vomit hospital"},
    "body pain": {"te": "Ollu noppulu. Dolo 650. 1.Rest 2.3L neeru 3.Walk thakkuva 4.Balamaina pani vaddu 5.Vecchani neeru 6.8h nidra 7.Massage 8.2 rojulu unte hospital", "hi": "Badan dard. Dolo 650. 1.Aaram 2.3L pani 3.Walk kam 4.Bhari kaam nahi 5.Garam pani 6.8h neend 7.Massage 8.2 din to hospital", "en": "Body pain. Dolo 650. 1.Rest 2.3L water 3.Less walk 4.No heavy work 5.Warm water 6.8h sleep 7.Massage 8.If 2 days hospital"},
    "back pain": {"te": "Nadumu noppi. 1.Kinda kurchovaddu 2.Baruva ethakandi 3.Hot bag 4.Straight kurchondi 5.Bike ekkuva vaddu 6.8h nidra gattiga bed 7.Massage 8.Numbness unte hospital", "hi": "Kamar dard. 1.Neeche mat baitho 2.Wajan mat uthao 3.Hot bag 4.Seedha baitho 5.Bike kam 6.Sakht bistar 7.Massage 8.Sunn ho to hospital", "en": "Back pain. 1.Dont sit down 2.No weight 3.Hot bag 4.Sit straight 5.Less bike 6.Hard bed 7.Massage 8.If numbness hospital"},
    "knee pain": {"te": "Mokalla noppi. 1.Ekkuva nadavaddu 2.Hot bag 3.Weight thaggandi 4.Metlu vaddu 5.Kinda kurchovaddu 6.Oil massage 7.Vecchani battalu 8.Vapu unte hospital", "hi": "Ghutne dard. 1.Zyada chalo nahi 2.Hot bag 3.Wajan kam 4.Seedhi nahi 5.Neeche nahi 6.Massage 7.Garam kapde 8.Sujan to hospital", "en": "Knee pain. 1.Less walk 2.Hot bag 3.Reduce weight 4.No stairs 5.Dont sit down 6.Massage 7.Warm clothes 8.If swelling hospital"},
    "toothache": {"te": "Pannu noppi. 1.Goruvecchi neetilo uppu 2.Cold ice 3.Sweet vaddu 4.Brush 2 sarlu 5.Cheyyi petakandi 6.Vecchani neeru 7.Lavangam 8.2 rojulu unte dentist", "hi": "Daat dard. 1.Garam pani namak 2.Barf 3.Meetha nahi 4.Brush 2 baar 5.Haath mat lagao 6.Garam pani 7.Laung 8.2 din to dentist", "en": "Toothache. 1.Warm salt water 2.Ice 3.No sweet 4.Brush twice 5.Dont touch 6.Warm water 7.Clove 8.If 2 days dentist"},
    "ear pain": {"te": "Chevi noppi. 1.Stick vaddu 2.Neeru pokunda 3.Cold vaddu 4.Earphone vaddu 5.Goruvecchi kapuram 6.Gattiga kadakandi 7.No oil 8.Chi mu unte hospital", "hi": "Kaan dard. 1.Stick nahi 2.Paani mat jane do 3.Thanda nahi 4.Earphone nahi 5.Garam sek 6.Zor se mat kheecho 7.Tel nahi 8.Mawaad to hospital", "en": "Ear pain. 1.No stick 2.No water inside 3.No cold 4.No earphone 5.Warm compress 6.Dont pull 7.No oil 8.If pus hospital"},
    "eye pain": {"te": "Kallu noppi. 1.Phone thakkuva 2.Chikati lo chadavaddhu 3.Rub cheyoddu 4.Challa neeru kadukko 5.Dust ki dooram 6.8h nidra 7.Glasses 8.Redness unte hospital", "hi": "Aankh dard. 1.Phone kam 2.Andhere me mat padho 3.Ragdo nahi 4.Thande pani se dho 5.Dhool se door 6.8h neend 7.Chashma 8.Laali to hospital", "en": "Eye pain. 1.Less phone 2.No reading in dark 3.Dont rub 4.Wash cold water 5.Away dust 6.8h sleep 7.Glasses 8.If redness hospital"},
    "skin allergy": {"te": "Charmam allergy. Cetzine. 1.Gokakandi 2.Detol snanam 3.Dust vaddu 4.Kottha soap vaddu 5.Vecchani battalu 6.Challa neeru vaddu 7.Clean ga undu 8.Vyapisthe hospital", "hi": "Skin allergy. Cetzine. 1.Khujlao nahi 2.Detol nahao 3.Dhool nahi 4.Naya soap nahi 5.Garam kapde nahi 6.Thanda pani nahi 7.Saaf raho 8.Faile to hospital", "en": "Skin allergy. Cetzine. 1.Dont scratch 2.Detol bath 3.No dust 4.No new soap 5.No warm clothes 6.No cold water 7.Stay clean 8.If spreads hospital"},
    "throat pain": {"te": "Gonthu noppi. 1.Goruvecchi neetilo uppu gargle 2.Challa vaddu 3.Ice vaddu 4.Arupulu vaddu 5.Vecchani neeru 6.Honey 7.Dust mask 8.2 rojulu unte hospital", "hi": "Gale dard. 1.Garam pani namak gargle 2.Thanda nahi 3.Barf nahi 4.Chillao nahi 5.Garam pani 6.Shahad 7.Mask 8.2 din to hospital", "en": "Throat pain. 1.Warm salt gargle 2.No cold 3.No ice 4.No shouting 5.Warm water 6.Honey 7.Mask 8.If 2 days hospital"},
    "chest pain": {"te": "Gunde noppi EMERGENCY. 1.Ventane 108 2.Padukondi 3.Nadavaddu 4.Bhayam vaddu 5.Oily ippudu vaddu 6.Tight shirt vaddu 7.Acidity anukokandi 8.Ventane Hospital", "hi": "Seene dard EMERGENCY. 1.Turant 108 2.Let jao 3.Chalo nahi 4.Daro nahi 5.Oily abhi nahi 6.Tight shirt nahi 7.Acidity mat samjho 8.Turant Hospital", "en": "Chest pain EMERGENCY. 1.Call 108 now 2.Lie down 3.Dont walk 4.Dont fear 5.No oily now 6.No tight shirt 7.Dont think acidity 8.Go Hospital now"},
    "dizziness": {"te": "Thalathirugudu. 1.Ventane kurchondi 2.Neeru tagandi 3.Bike aapandi 4.Tala kinda pettakandi 5.3L neeru 6.8h nidra 7.Tea thakkuva 8.Padipothe hospital", "hi": "Chakkar. 1.Turant baitho 2.Paani piyo 3.Bike roko 4.Sir neeche mat karo 5.3L pani 6.8h neend 7.Chai kam 8.Gir jao to hospital", "en": "Dizziness. 1.Sit immediately 2.Drink water 3.Stop bike 4.Dont bend head 5.3L water 6.8h sleep 7.Less tea 8.If fall hospital"},
    "high bp": {"te": "High BP. 1.Uppu thakkuva 2.Walk 30min 3.Tension vaddu 4.8h nidra 5.Oily vaddu 6.Mandhu time ki 7.BP check roj 8.Thala noppi unte hospital", "hi": "High BP. 1.Namak kam 2.Walk 30min 3.Tension nahi 4.8h neend 5.Oily nahi 6.Dawa time par 7.Roz check 8.Sir dard to hospital", "en": "High BP. 1.Less salt 2.Walk 30min 3.No tension 4.8h sleep 5.No oily 6.Med on time 7.Daily check 8.If headache hospital"},
    "diabetes": {"te": "Sugar. 1.Sweet vaddu 2.Rice thakkuva 3.Walk 30min 4.Time ki food 5.Mandhu time ki 6.Sugar check 7.Gayalu unte niluvu 8.Kallu check", "hi": "Sugar. 1.Meetha nahi 2.Chawal kam 3.Walk 30min 4.Time par khana 5.Dawa time 6.Check sugar 7.Ghav dhyan 8.Aankh check", "en": "Diabetes. 1.No sweet 2.Less rice 3.Walk 30min 4.Timely food 5.Med on time 6.Check sugar 7.Care wounds 8.Eye check"},
    "loose motion": {"te": "Nello pakam. ORS ekkuva. Perugu annam, arati pandu. Bayata food, paalu vaddu.", "hi": "Loose motion. ORS zyada. Dahi chawal, kela. Bahar khana, doodh nahi.", "en": "Loose motion. More ORS. Curd rice, banana. No outside food, milk."},
    "gas": {"te": "Gas. Gelusil. 1.Time ki tinali 2.Thondaraga tinakandi 3.Masala vaddu 4.Cool drink vaddu 5.Walk 10 min 6.Perugu 7.Maidha vaddu 8.Noppi ekkuva unte hospital", "hi": "Gas. Gelusil. 1.Time par khao 2.Jaldi mat khao 3.Masala nahi 4.Cold drink nahi 5.Walk 10 min 6.Dahi 7.Maida nahi 8.Dard zyada to hospital", "en": "Gas. Gelusil. 1.Timely eat 2.Dont eat fast 3.No masala 4.No cold drink 5.Walk 10min 6.Curd 7.No maida 8.If more pain hospital"},
    "weight loss": {"te": "Barevu thaggu. 1.Time ki 3 puru tinali 2.Protein egg pappu 3.Paalu 4.Walk kadu gym light 5.8h nidra 6.Tension vaddu 7.Junk vaddu 8.Checkup hospital", "hi": "Wajan kam. 1.Time par 3 baar khao 2.Protein anda dal 3.Doodh 4.Light gym 5.8h neend 6.Tension nahi 7.Junk nahi 8.Checkup hospital", "en": "Weight loss. 1.3 times timely 2.Protein egg dal 3.Milk 4.Light gym 5.8h sleep 6.No tension 7.No junk 8.For checkup hospital"},
    "insomnia": {"te": "Nidra pataka. 1.Phone 9pm vaddu 2.Tea coffee evening vaddu 3.10pm ki paduko 4.Goruvecchi paalu 5.Yoga 10 min 6.Chikati room 7.Alochana vaddu 8.3 rojulu lekapothe hospital", "hi": "Neend nahi. 1.9pm ke baad phone nahi 2.Shaam ko chai nahi 3.10pm so jao 4.Garam doodh 5.Yoga 10min 6.Andhera kamra 7.Soch nahi 8.3 din nahi to hospital", "en": "Insomnia. 1.No phone after 9pm 2.No tea evening 3.Sleep 10pm 4.Warm milk 5.Yoga 10min 6.Dark room 7.No overthink 8.If 3 days no sleep hospital"},
    "anxiety": {"te": "Tension. 1.Deep breath 10 sarlu 2.Walk 30min 3.Music vinu 4.Phone thakkuva 5.8h nidra 6.Tea coffee thakkuva 7.Friends tho matladu 8.Ekkuva unte hospital", "hi": "Tension. 1.Gehri saans 10 baar 2.Walk 30min 3.Music suno 4.Phone kam 5.8h neend 6.Chai kam 7.Dosto se baat 8.Zyada to hospital", "en": "Anxiety. 1.Deep breath 10 times 2.Walk 30min 3.Listen music 4.Less phone 5.8h sleep 6.Less tea coffee 7.Talk to friends 8.If more hospital"},
    "wound": {"te": "Gayamu. 1.Detol tho kadukko 2.Betadine rasi 3.Clean cloth kattuko 4.Roju 2 sarlu dressing 5.Neeru tagakunda 6.Dust vaddu 7.Tetanus 8.Pus unte hospital", "hi": "Ghav. 1.Detol se dho 2.Betadine lagao 3.Saaf patti 4.Roz 2 baar dressing 5.Paani mat lagao 6.Dhool nahi 7.Tetanus 8.Mawaad to hospital", "en": "Wound. 1.Wash Detol 2.Betadine 3.Clean bandage 4.Dressing twice 5.No water 6.No dust 7.Tetanus 8.If pus hospital"},
    "breathing": {"te": "Oopiri aadaka EMERGENCY. 1.Ventane 108 2.Kurchondi 3.Dust nundi bayataku 4.Tight dress vaddu 5.Aaviri 6.Smoke vaddu 7.Bhayam vaddu 8.Ventane hospital", "hi": "Saans problem EMERGENCY. 1.Turant 108 2.Baitho leto nahi 3.Dhool se bahar 4.Tight kapde nahi 5.Bhaap 6.Dhua nahi 7.Daro nahi 8.Turant hospital", "en": "Breathing difficulty EMERGENCY. 1.Call 108 2.Sit dont lie 3.Out of dust 4.No tight dress 5.Steam 6.No smoke 7.Dont fear 8.Hospital now"},
    "cold fever": {"te": "Jalubu jwaram. Dolo 650, Cetzine. 1.Rest 2.Aaviri 3.Goruvecchi neeru 4.Challa vaddu 5.Mask 6.3L neeru 7.Pillala daggara vaddu 8.2 rojulu thaggakapothe hospital", "hi": "Zukam bukhar. Dolo Cetzine. 1.Aaram 2.Bhaap 3.Garam pani 4.Thanda nahi 5.Mask 6.3L pani 7.Baccho se door 8.2 din nahi to hospital", "en": "Cold fever. Dolo Cetzine. 1.Rest 2.Steam 3.Warm water 4.No cold 5.Mask 6.3L water 7.Away kids 8.If 2 days hospital"},
}

def get_reply(q):
    ql = q.lower()
    for k in SYMPTOMS_DB:
        if k in ql: return SYMPTOMS_DB[k]["en"], SYMPTOMS_DB[k]["te"], SYMPTOMS_DB[k]["hi"]
    if "jwaram" in ql: return SYMPTOMS_DB["fever"]["en"], SYMPTOMS_DB["fever"]["te"], SYMPTOMS_DB["fever"]["hi"]
    if "kadupu" in ql: return SYMPTOMS_DB["stomach pain"]["en"], SYMPTOMS_DB["stomach pain"]["te"], SYMPTOMS_DB["stomach pain"]["hi"]
    return (f"For {q}: Rest, 3L water, 8h sleep, light food. Precautions: No cold, oily, spicy, outside food, mask, wash hands. If 2 days no relief visit Tiruvuru Govt Hospital garu.",
            f"{q} kosam garu: Vishranti, 3L neeru, 8 gantalu nidra, light food. Jagrathalu: Challa, noone, karam, bayata food vaddu, mask, chethulu kadukkondi. 2 rojula tharvata hospital ki randi.",
            f"{q} ke liye: Aaram, 3L pani, 8h neend. Precautions: Thanda, tel masala avoid, mask, haath dho. 2 din me nahi to hospital.")

feature = st.sidebar.selectbox("📋 SELECT FEATURE", ["🩺 AI Doctor Chat", "💊 Medicine Info & Diet", "🧘 Health Tips & Yoga", "🚨 Emergency 108", "📸 Image Analyzer"])

if feature == "🩺 AI Doctor Chat":
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("<div class='beauty-card'><h3 style='text-align:center; color:#00C9FF;'>🎤 Speak Here</h3><p style='text-align:center; color:#AAA;'>Mic & speak in Telugu/Hindi/English</p></div>", unsafe_allow_html=True)
        user_audio = st.audio_input("Click to speak...", label_visibility="collapsed")
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
                if lang=='te': st.info(tel); speak_single(tel,'te')
                elif lang=='hi': st.info(hin); speak_single(hin,'hi')
                else: st.info(eng); speak_single(eng,'en')
            except: st.warning("Malli okasari cheppandi garu.")
    with col2:
        st.markdown("<div class='beauty-card'><h3 style='text-align:center; color:#92FE9D;'>⌨️ Type Here</h3><p style='text-align:center; color:#AAA;'>Type symptoms in any language</p></div>", unsafe_allow_html=True)
        q = st.chat_input("Enter symptoms... jwaram / fever")
        if q:
            lang = detect_language(q)
            st.write(f"**You:** {q}")
            eng,tel,hin = get_reply(q)
            if lang=='te': st.info(tel); speak_single(tel,'te')
            elif lang=='hi': st.info(hin); speak_single(hin,'hi')
            else: st.info(eng); speak_single(eng,'en')

elif feature == "💊 Medicine Info & Diet":
    st.markdown("<div class='beauty-card'><h3 style='text-align:center; color:#00C9FF;'>💊 Medicine Info</h3><p>Dolo 650 - Fever, headache - After food<br>Cetzine - Cold allergy - Night 1<br>Gelusil - Gas acidity - After food<br>Cyclopam - Stomach cramp - After food<br>Vomikind 4mg - Vomiting - Under tongue<br>ORS - 1 pkt in 1L water<br>Pan 40 - Morning empty stomach<br><br><i>Note garu: Doctor ni adigi vesukondi.</i></p></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='beauty-card' style='margin-top:15px; border-color:#92FE9D;'>
        <h3 style='text-align:center; color:#92FE9D;'>🥗 Diet Plan - Thine Vishayam</h3>
        <p style='font-size:14px; line-height:1.8;'>
        Namaste garu, thine vishayam lo koncham jagratha ga undandi.<br><br>
        <b>Thinalsi vishayalu:</b><br>
        - Udayam: Goruvecchi neeru + 2 kela / papaya / apple<br>
        - Madhyanam: Annam + pappu + perugu, koncham thakkuva uppu tho<br>
        - Sayantram: Kobbari neeru / fruit juice (no ice)<br>
        - Rathri: 2 chapati + light curry, 9 lopu thineyandi garu<br><br>
        <b>Thinakudadani vishayalu garu:</b><br>
        - Bayata fry, biryani, cool drinks, ekkuva karam, maida - 5 rojulu vaddu.<br>
        - Tea, coffee roju ki 1-2 sarlu chalu, ekkuva vaddhu.<br><br>
        Light ga tintu unte kadupu kuda happy ga untundi garu, thondaraga thagguthundi.
        </p>
    </div>
    """, unsafe_allow_html=True)

elif feature == "🧘 Health Tips & Yoga":
    st.markdown("""
    <div class='beauty-card'>
        <h3 style='text-align:center; color:#00C9FF;'>🧘 Daily Health Tips - Manchi Aarogyam Kosam</h3>
        <p style='font-size:14px; line-height:1.9;'>
        Namaste garu, rojulo konni chinna jagrathalu teesukunte chalu, aarogyam bavuntundi.<br><br>
        <b>1. Morning Walk:</b> Roju 30 nimishalu walk cheyandi garu, body active ga untundi, blood circulation bavuntundi.<br>
        <b>2. Yoga & Breathing:</b> 15 nimishalu yoga, deep breath cheyandi, stress, tension thagguthundi garu.<br>
        <b>3. Water:</b> Roju 3 liters neeru thappakunda tagandi garu, body clean avuthundi, jwaram kuda thondaraga thagguthundi.<br>
        <b>4. Sleep:</b> 8 gantalu nidra chala mukhyam garu, phone pakkana petti, chikati gadi lo padukondi.<br>
        <b>5. Food Time:</b> Time ki tinali garu, night 9 lopu thineyandi, light ga tintu unte aarogyam.<br>
        <b>6. Clean Habits:</b> Thine mundhu chethulu kadukkondi garu, dust lo unte mask pettukondi.<br>
        <b>7. No Bad Habits:</b> Smoking, alcohol vaddu garu, avi aarogyaniki manchidi kadu ani meeku telusu.<br>
        <b>8. Happy Mind:</b> Chinna vishayalaki tension padakandi garu, koncham music vini, friends tho matladandi.<br><br>
        Mee aarogyam me chethilo undi garu, jagratha ga undandi. Edaina doubt unte Tiruvuru Govt Hospital ki randi.
        </p>
    </div>
    """, unsafe_allow_html=True)

elif feature == "🚨 Emergency 108":
    st.markdown("<div class='beauty-card' style='border-left:6px solid red;'><h3 style='color:red; text-align:center;'>🚨 Emergency 108</h3><p style='line-height:2;'>🚑 108 - Ambulance<br>🚓 100 - Police<br>🔥 101 - Fire<br>🏥 Tiruvuru Govt Hospital - 24/7<br>👶 104 - Health Helpline<br><br>Namaste garu, emergency lo bayapadakandi, ventane call cheyandi.</p></div>", unsafe_allow_html=True)

elif feature == "📸 Image Analyzer":
    st.markdown("<div class='beauty-card'><h3 style='text-align:center;'>📸 Image Analyzer (Wound/Skin)</h3></div>", unsafe_allow_html=True)
    img = st.file_uploader("Upload image", type=["jpg","png","jpeg"])
    if img:
        st.image(Image.open(img), use_column_width=True)
        st.warning("Gayamu unte Dettol tho kadigi Betadine rayandi garu. Vapu, pus, ekkuva noppi unte ventane Tiruvuru Hospital ki randi.")
