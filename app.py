import streamlit as st
import re
from PIL import Image

st.set_page_config(page_title="AI Medical Assistant Pro Max - Tiruvuru", layout="wide")

st.markdown("""
<style>
.main-title { text-align:center; color:#00E5FF; font-size:32px; font-weight:bold; }
.beauty-card { background:#1E1E1E; padding:20px; border-radius:15px; border:1px solid #00E5FF; margin-top:10px; }
</style>
<div class='main-title'>AI Medical Assistant Pro Max</div>
""", unsafe_allow_html=True)

def detect_language(text):
    if re.search(r'[\u0C00-\u0C7F]', text): return 'te'
    if re.search(r'[\u0900-\u097F]', text): return 'hi'
    if any(w in text.lower() for w in ['bukhar','khansi','dard','pet','sir','bukhaar','zukam']): return 'hi'
    return 'en'

# --- YOUR FULL DATABASE - NOW 100% ERROR FREE ---
SYMPTOMS_DB = {
    "fever": {"te": "Namaste, meeku Jwaram. Dolo 650 tharuvata. 1.Vishranti 2.Challani gudda 3.Challa snanam vaddu 4.Mask 5.3-4L neeru 6.Fan vaddu 7.Mandu share vaddu 8.Vantulu unte hospital. Aharam: Khichdi, ganji", "hi": "asslamualaikum, app ko Bukhar hy. Dolo 650. 1.Aaram 2.Thanda patti 3.Thanda pani nahi 4.Mask 5.3-4L pani 6.Fan nahi 7.Share nahi 8.Ulti to hospital.", "en": "hello,you have Fever. Dolo 650. 1.Rest 2.Cold cloth 3.No cold bath 4.Mask 5.3-4L water 6.No fan 7.Dont share 8.If vomit hospital."},
    "cold": {"te": "Namaste, meeku Jalubu. Cetrizine night. 1.Aaviri 2 sarlu 2.Vecchani battalu 3.Challa neeru 5 rojulu vaddu 4.Dust vaddu 5.Rumal 6.Pillala daggara vaddu 7.Goruvecchi neeru 8.Thummu lo chethi", "hi": "asslamualaikum, app ko Zukam hy. Cetrizine. 1.Bhaap 2.Garam kapde 3.Thanda pani 5 din nahi 4.Dhool nahi 5.Rumaal 6.Baccho se doori 7.Garam pani 8.Cheenk me haath", "en": "hello,you have Cold. Cetrizine. 1.Steam 2.Warm clothes 3.No cold water 5 days 4.No dust 5.Hanky 6.Away kids 7.Warm water 8.Cover sneeze"},
    "cough": {"te": "Namaste, meeku Daggu. Ascoril. 1.Aaviri 2.Honey+miriyam 3.Challa vaddu 4.Dust mask 5.Goruvecchi neeru 6.Pillala ki dooram 7.Daggetappudu chethi 8.7 rojulu unte hospital", "hi": "assalamualaikum, aap ko Khansi hy. Ascoril. 1.Bhaap 2.Shahad 3.Thanda nahi 4.Mask 5.Garam pani 6.Baccho se door 7.Khanste haath 8.7 din to hospital", "en": "hello, you have Cough. Ascoril. 1.Steam 2.Honey 3.No cold 4.Mask 5.Warm water 6.Away kids 7.Cover 8.If more than 7 days hospital"},
    "headache": {"te": "Namaste,meeku Thala noppi. Dolo 650. 1.Chikati gadi rest 2.Phone vaddu 3.3L neeru 4.Tea thakkuva 5.8h nidra 6.Oli vaddu 7.Massage 8.2 rojulu thaggakapothe hospital", "hi": "assalamualaikum,aap ko Sir dard hy. Dolo 650. 1.Andhere me aaram 2.Phone nahi 3.3L pani 4.Chai kam 5.8h neend 6.Shore nahi 7.Massage 8.2 din nahi to hospital", "en": "hello,you have Headache. Dolo 650. 1.Dark room rest 2.No phone 3.3L water 4.Less tea 5.8h sleep 6.No noise 7.Massage 8.If 2 days hospital"},
    "stomach pain": {"te": "Namaste, meeku Kadupu noppi. Cyclopam, Gelusil. 1.Ganji 2.Oily vaddu 3.Hot bag 10 min 4.Left side 5.Gattiga nakakandi 6.2h emi vaddhu 7.Clockwise massage 8.6h pain unte hospital", "hi": "assalamualaikum, aap ko Pet dard hy. Cyclopam. 1.Ganji 2.Oily nahi 3.Hot bag 4.Left side 5.Press nahi 6.2h kuch nahi 7.Massage 8.6h dard to hospital", "en": "hello,you have Stomach pain. Cyclopam. 1.Kanji only 2.No oily 3.Hot bag 4.Left side 5.Dont press 6.Nothing 2h 7.Massage 8.If more than 6h hospital"},
    "vomiting": {"te": "Namaste, meeku Vantulu. Vomikind 4mg. 1.30min emi vaddhu 2.ORS koncham 3.Noru kadukko 4.Perfume vaddu 5.Travel vaddu 6.Left side 7.Biryani vaddu 8.3-4 sarlu unte hospital", "hi": "assalamualaikum,aap ko Ulti hy. Vomikind. 1.30min kuch nahi 2.ORS thoda 3.Muh dho 4.Khushboo nahi 5.Travel nahi 6.Left side 7.Biryani nahi 8.3-4 se zyada hospital", "en": "hello,you have Vomiting. Vomikind. 1.Nothing 30min 2.Sip ORS 3.Wash mouth 4.No smell 5.No travel 6.Left side 7.No biryani 8.If more than 3-4 hospital"},
    "diarrhea": {"te": "Namaste,meeku Virarechanalu. ORS, Econorm. 1.ORS ekkuva 2.Ganji 3.Perugu annam 4.Bayata food vaddu 5.Paalu vaddu 6.Chethulu kadukko 7.Mask 8.Blood unte hospital", "hi": "assalamualaikum,aap ko Dast. ORS. 1.ORS zyada 2.Ganji 3.Dahi chawal 4.Bahar khana nahi 5.Doodh nahi 6.Haath dho 7.Mask 8.Khoon to hospital", "en": "hello,you have Diarrhea. ORS. 1.More ORS 2.Kanji 3.Curd rice 4.No outside food 5.No milk 6.Wash hands 7.Mask 8.If blood hospital"},
    "constipation": {"te": "Namaste,meeku Malabaddhakam. 1.3-4L neeru 2.Papaya, kela 3.Walk 30min 4.Time ki food 5.Oily thakkuva 6.Masala vaddu 7.Maidha vaddu 8.3 rojulu unte hospital", "hi": "assalamualaikum,aap ko Kabz hy. 1.3-4L pani 2.Papita kela 3.Walk 30min 4.Time par khana 5.Oily kam 6.Masala nahi 7.Maida nahi 8.3 din to hospital", "en": "hello,you have Constipation. 1.3-4L water 2.Papaya banana 3.Walk 30min 4.Timely food 5.Less oily 6.No masala 7.No maida 8.If 3 days hospital"},
    "acidity": {"te": "Namaste,meeku Acidity. Pan 40 morning. 1.Khali kadupu vaddu 2.Karam vaddu 3.Tea coffee vaddu 4.Time ki tinali 5.Chintala vaddu 6.Nidra 8h 7.Oily vaddu 8.Blood vanti unte hospital", "hi": "assalamualaikum,aap ko Acidity. Pan 40. 1.Khali pet nahi 2.Mirch nahi 3.Chai coffee nahi 4.Time par khao 5.Tension nahi 6.8h neend 7.Oily nahi 8.Khoon ulti to hospital", "en": "hello, you have Acidity. Pan 40 morning. 1.No empty stomach 2.No spicy 3.No tea coffee 4.Timely eat 5.No tension 6.8h sleep 7.No oily 8.If blood vomit hospital"},
    "body pain": {"te": "Namaste,meeku Ollu noppulu. Dolo 650. 1.Rest 2.3L neeru 3.Walk thakkuva 4.Balamaina pani vaddu 5.Vecchani neeru 6.8h nidra 7.Massage 8.2 rojulu unte hospital", "hi": "assalamualaikum,aap ko Badan dard hy. Dolo 650. 1.Aaram 2.3L pani 3.Walk kam 4.Bhari kaam nahi 5.Garam pani 6.8h neend 7.Massage 8.2 din to hospital", "en": "hello,you have Body pain. Dolo 650. 1.Rest 2.3L water 3.Less walk 4.No heavy work 5.Warm water 6.8h sleep 7.Massage 8.If 2 days hospital"},
    "back pain": {"te": "Namaste,meeku Nadumu noppi. 1.Kinda kurchovaddu 2.Baruva ethakandi 3.Hot bag 4.Straight kurchondi 5.Bike ekkuva vaddu 6.8h nidra gattiga bed 7.Massage 8.Numbness unte hospital", "hi": "assalamualaikum,aap ko Kamar dard hy. 1.Neeche mat baitho 2.Wajan mat uthao 3.Hot bag 4.Seedha baitho 5.Bike kam 6.Sakht bistar 7.Massage 8.Sunn ho to hospital", "en": "hello,you have Back pain. 1.Dont sit down 2.No weight 3.Hot bag 4.Sit straight 5.Less bike 6.Hard bed 7.Massage 8.If numbness hospital"},
    "knee pain": {"te": "Namaste,meeku Mokalla noppi. 1.Ekkuva nadavaddu 2.Hot bag 3.Weight thaggandi 4.Metlu vaddu 5.Kinda kurchovaddu 6.Oil massage 7.Vecchani battalu 8.Vapu unte hospital", "hi": "assalamualaikum,aap ko Ghutne dard hy. 1.Zyada chalo nahi 2.Hot bag 3.Wajan kam 4.Seedhi nahi 5.Neeche nahi 6.Massage 7.Garam kapde 8.Sujan to hospital", "en": "hello,you have Knee pain. 1.Less walk 2.Hot bag 3.Reduce weight 4.No stairs 5.Dont sit down 6.Massage 7.Warm clothes 8.If swelling hospital"},
    "toothache": {"te": "Namaste,meeku Pannu noppi. 1.Goruvecchi neetilo uppu 2.Cold ice 3.Sweet vaddu 4.Brush 2 sarlu 5.Cheyyi petakandi 6.Vecchani neeru 7.Lavangam 8.2 rojulu unte dentist", "hi": "assalamualaikum,aap ko Daat dard hy. 1.Garam pani namak 2.Barf 3.Meetha nahi 4.Brush 2 baar 5.Haath mat lagao 6.Garam pani 7.Laung 8.2 din to dentist", "en": "hello,you have Toothache. 1.Warm salt water 2.Ice 3.No sweet 4.Brush twice 5.Dont touch 6.Warm water 7.Clove 8.If 2 days dentist"},
    "ear pain": {"te": "Namaste,meeku Chevi noppi. 1.Stick vaddu 2.Neeru pokunda 3.Cold vaddu 4.Earphone vaddu 5.Goruvecchi kapuram 6.Gattiga kadakandi 7.No oil 8.Chi mu unte hospital", "hi": "assalamualaikum,aap ko Kaan dard hy. 1.Stick nahi 2.Paani mat jane do 3.Thanda nahi 4.Earphone nahi 5.Garam sek 6.Zor se mat kheecho 7.Tel nahi 8.Mawaad to hospital", "en": "hello,you have Ear pain. 1.No stick 2.No water inside 3.No cold 4.No earphone 5.Warm compress 6.Dont pull 7.No oil 8.If pus hospital"},
    "eye pain": {"te": "Namaste,meeku Kallu noppi. 1.Phone thakkuva 2.Chikati lo chadavaddhu 3.Rub cheyoddu 4.Challa neeru kadukko 5.Dust ki dooram 6.8h nidra 7.Glasses 8.Redness unte hospital", "hi": "assalamualaikum,aap ko Aankh dard hy. 1.Phone kam 2.Andhere me mat padho 3.Ragdo nahi 4.Thande pani se dho 5.Dhool se door 6.8h neend 7.Chashma 8.Laali to hospital", "en": "hello,you have Eye pain. 1.Less phone 2.No reading in dark 3.Dont rub 4.Wash cold water 5.Away dust 6.8h sleep 7.Glasses 8.If redness hospital"},
    "skin allergy": {"te": "Namaste,meeku Charmam allergy. Cetzine. 1.Gokakandi 2.Detol snanam 3.Dust vaddu 4.Kottha soap vaddu 5.Vecchani battalu 6.Challa neeru vaddu 7.Clean ga undu 8.Vyapisthe hospital", "hi": "assalamualaikum,aap ko Skin allergy hy. Cetzine. 1.Khujlao nahi 2.Detol nahao 3.Dhool nahi 4.Naya soap nahi 5.Garam kapde nahi 6.Thanda pani nahi 7.Saaf raho 8.Faile to hospital", "en": "hello,you have Skin allergy. Cetzine. 1.Dont scratch 2.Detol bath 3.No dust 4.No new soap 5.No warm clothes 6.No cold water 7.Stay clean 8.If spreads hospital"},
    "throat pain": {"te": "Namaste,meeku Gonthu noppi. 1.Goruvecchi neetilo uppu gargle 2.Challa vaddu 3.Ice vaddu 4.Arupulu vaddu 5.Vecchani neeru 6.Honey 7.Dust mask 8.2 rojulu unte hospital", "hi": "assalamualaikum,aap ko Gale dard hy. 1.Garam pani namak gargle 2.Thanda nahi 3.Barf nahi 4.Chillao nahi 5.Garam pani 6.Shahad 7.Mask 8.2 din to hospital", "en": "hello,you have Throat pain. 1.Warm salt gargle 2.No cold 3.No ice 4.No shouting 5.Warm water 6.Honey 7.Mask 8.If 2 days hospital"},
    "chest pain": {"te": "Namaste,meeku Gunde noppi EMERGENCY. 1.Ventane 108 2.Padukondi 3.Nadavaddu 4.Bhayam vaddu 5.Oily ippudu vaddu 6.Tight shirt vaddu 7.Acidity anukokandi 8.Ventane Hospital", "hi": "assalamualaikum,aap ko Seene dard hy EMERGENCY. 1.Turant 108 2.Let jao 3.Chalo nahi 4.Daro nahi 5.Oily abhi nahi 6.Tight shirt nahi 7.Acidity mat samjho 8.Turant Hospital", "en": "hello,you have Chest pain EMERGENCY. 1.Call 108 now 2.Lie down 3.Dont walk 4.Dont fear 5.No oily now 6.No tight shirt 7.Dont think acidity 8.Go Hospital now"},
    "dizziness": {"te": "Namaste,meeku Thalathirugudu. 1.Ventane kurchondi 2.Neeru tagandi 3.Bike aapandi 4.Tala kinda pettakandi 5.3L neeru 6.8h nidra 7.Tea thakkuva 8.Padipothe hospital", "hi": "assalamualaikum,aap ko Chakkar. 1.Turant baitho 2.Paani piyo 3.Bike roko 4.Sir neeche mat karo 5.3L pani 6.8h neend 7.Chai kam 8.Gir jao to hospital", "en": "hello,you have Dizziness. 1.Sit immediately 2.Drink water 3.Stop bike 4.Dont bend head 5.3L water 6.8h sleep 7.Less tea 8.If fall hospital"},
    "high bp": {"te": "Namaste,meeku High BP. 1.Uppu thakkuva 2.Walk 30min 3.Tension vaddu 4.8h nidra 5.Oily vaddu 6.Mandhu time ki 7.BP check roj 8.Thala noppi unte hospital", "hi": "assalamualaikum,aap ko High BP hy. 1.Namak kam 2.Walk 30min 3.Tension nahi 4.8h neend 5.Oily nahi 6.Dawa time par 7.Roz check 8.Sir dard to hospital", "en": "hello,you have High BP. 1.Less salt 2.Walk 30min 3.No tension 4.8h sleep 5.No oily 6.Med on time 7.Daily check 8.If headache hospital"},
    "diabetes": {"te": "Namaste,meeku Sugar. 1.Sweet vaddu 2.Rice thakkuva 3.Walk 30min 4.Time ki food 5.Mandhu time ki 6.Sugar check 7.Gayalu unte niluvu 8.Kallu check", "hi": "assalamualaikum,aap ko Sugar hy. 1.Meetha nahi 2.Chawal kam 3.Walk 30min 4.Time par khana 5.Dawa time 6.Check sugar 7.Ghav dhyan 8.Aankh check", "en": "hello,you have Diabetes. 1.No sweet 2.Less rice 3.Walk 30min 4.Timely food 5.Med on time 6.Check sugar 7.Care wounds 8.Eye check"},
    "gas": {"te": "Namaste,meeku Gas. Gelusil. 1.Time ki tinali 2.Thondaraga tinakandi 3.Masala vaddu 4.Cool drink vaddu 5.Walk 10 min 6.Perugu 7.Maidha vaddu 8.Noppi ekkuva unte hospital", "hi": "assalamualaikum,aap ko Gas hy. Gelusil. 1.Time par khao 2.Jaldi mat khao 3.Masala nahi 4.Cold drink nahi 5.Walk 10 min 6.Dahi 7.Maida nahi 8.Dard zyada to hospital", "en": "hello,you have Gas. Gelusil. 1.Timely eat 2.Dont eat fast 3.No masala 4.No cold drink 5.Walk 10min 6.Curd 7.No maida 8.If more pain hospital"},
    "anxiety": {"te": "Namaste,meeku Tension. 1.Deep breath 10 sarlu 2.Walk 30min 3.Music vinu 4.Phone thakkuva 5.8h nidra 6.Tea coffee thakkuva 7.Friends tho matladu 8.Ekkuva unte hospital", "hi": "assalamualaikum,aap ko Tension hy. 1.Gehri saans 10 baar 2.Walk 30min 3.Music suno 4.Phone kam 5.8h neend 6.Chai kam 7.Dosto se baat 8.Zyada to hospital", "en": "hello,you have Anxiety. 1.Deep breath 10 times 2.Walk 30min 3.Listen music 4.Less phone 5.8h sleep 6.Less tea coffee 7.Talk to friends 8.If more hospital"},
}

def get_reply(symptom, lang):
    symptom = symptom.lower()
    for key in SYMPTOMS_DB:
        if key in symptom:
            return SYMPTOMS_DB[key].get(lang, SYMPTOMS_DB[key]['en'])
    if lang == 'te': return "Meeku em problem cheppandi."
    if lang == 'hi': return "Aapko kya problem hai bataiye."
    return "Please tell your symptoms."

# MENU - SAFE NO EMOJI IN CONDITION
feature = st.sidebar.selectbox("SELECT FEATURE", ["AI Doctor Chat", "Diet Plan Section", "Health Tips Section", "Image Analyser Section", "Emergency"])

if "Doctor Chat" in feature:
    st.markdown("<div class='beauty-card'>Type your problem</div>", unsafe_allow_html=True)
    user_input = st.text_input("Enter Symptoms")
    if user_input:
        lang = detect_language(user_input)
        st.success(get_reply(user_input, lang))

elif "Diet Plan" in feature:
    st.markdown("""
    <div class='beauty-card' style='border-color:#92FE9D;'>
    <h3 style='text-align:center; color:#92FE9D;'>Diet Plan / Aahar / ఆహార ప్రణాళిక</h3>
    <p style='color:white; font-size:14px; line-height:1.9;'>
    Udayam: Goruvecchi neeru + rendu kela / Lukewarm water + two banana / गुनगुना पानी + दो केले<br>
    Madhyanam: Annam + pappu + perugu / Rice + dal + curd / चावल + दाल + दही<br>
    Rathri: Rendu chapati / Two chapati / दो चपाती, thommidi gantala lopu / before nine / नौ बजे से पहले<br>
    Avoid: Bayata fry vaddu / Avoid outside fry / बाहर का तला न खाएं
    </p>
    </div>
    """, unsafe_allow_html=True)

elif "Health Tips" in feature:
    st.markdown("""
    <div class='beauty-card'>
    <h3 style='text-align:center; color:#00E5FF;'>Health Tips</h3>
    <p style='color:white; font-size:14px; line-height:1.9;'>
    Walk muppay nimishalu / Thirty min / तीस मिनट<br>
    Water moodu liters / Three liters / तीन लीटर<br>
    Sleep enimidi gantalu / Eight hours / आठ घंटे<br>
    Mee aarogyam me chethilo undi / Your health in your hands / स्वास्थ्य आपके हाथ में है
    </p>
    </div>
    """, unsafe_allow_html=True)

elif "Image Analyser" in feature:
    st.markdown("<div class='beauty-card' style='border-color:#FF6B6B;'><h3 style='text-align:center; color:#FF6B6B;'>Image Analyser</h3><p style='color:white; text-align:center;'>Upload Photo / Photo upload cheyandi / फोटो अपलोड करें</p></div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose Image", type=["jpg","png","jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Your Photo", use_column_width=True)
        st.success("Image Received! Chusanu / Dekh liya")
        st.markdown("""
        <div class='beauty-card'>
        <p style='color:white;'>Show to doctor / Doctor ki chupinchandi / डॉक्टर को दिखाएं<br>Keep clean / Clean ga unchandi / साफ रखें<br>Do not scratch / Gokakandi / खुजलाएं नहीं<br>Doctor advice important / Doctor salah mukhyam / डॉक्टर सलाह जरूरी है</p>
        </div>
        """, unsafe_allow_html=True)

elif "Emergency" in feature:
    st.error("EMERGENCY: Call One Zero Eight - 108")
