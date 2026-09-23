import streamlit as st
from datetime import datetime
from gtts import gTTS
import os
from PIL import Image

st.set_page_config(page_title="Medical Assistant - Tiruvuru", layout="centered", page_icon="🏥")
st.warning("⚠️ Educational Purpose Only - Consult Real Doctor")
st.title("🏥 Medical Assistant Pro Max - Tiruvuru")

# Voice function - For illiterate people
def speak(text):
    try:
        clean_text = text.replace("🤒","").replace("🤧","").replace("😮‍💨","").replace("🤕","").replace("🤢","").replace("🤮","").replace("🚽","").replace("😣","").replace("💔","").replace("🦴","").replace("🦵","").replace("🍬","").replace("❤️","").replace("😵‍💫","").replace("🔥","").replace("👁️","").replace("👂","").replace("🦷","").replace("🧴","").replace("🩹","").replace("😤","").replace("🦟","").replace("🩺","").replace("💊","").replace("🥗","").replace("⚠️","").replace("📞","").replace("**","")
        tts = gTTS(text=clean_text[:400], lang='en', slow=False)
        tts.save("voice.mp3")
        with open("voice.mp3", "rb") as f:
            st.audio(f.read(), format="audio/mp3")
        os.remove("voice.mp3")
    except:
        st.write("Voice loading...")

# SIDEBAR - ALL 7 FEATURES
feature = st.sidebar.selectbox("📋 Select Feature",
    ["AI Doctor Chat - 30+ Symptoms",
     "💊 Medicine Info",
     "🧘 Health Tips & Yoga",
     "🚨 Emergency Alert",
     "🤖 AI Chatbot 24/7",
     "📸 Image Analyzer",
     "ℹ️ About"])

# FEATURE 1: YOUR 30+ SYMPTOMS + VOICE + BUTTON BOTH
if feature == "AI Doctor Chat - 30+ Symptoms":
    st.subheader("Chat with AI Doctor - Type Any Symptom")
    st.caption("30+ Symptoms: fever, cold, cough, headache, stomach, vomiting, diarrhea, throat, chest, back, knee, diabetes, BP, dizziness, allergy, acidity, eye, ear, tooth, skin, wound, constipation, asthma, malaria, dengue, typhoid etc.")
    q = st.chat_input("Type your symptom in English...")

    if q:
        st.chat_message("user").write(q)
        q_lower = q.lower()
        reply = ""

        if "fever" in q_lower:
            reply = "🤒 **FEVER:**\n🩺 Rest, water, cold cloth on forehead\n💊 Dolo 650 after food\n🥗 Khichdi, coconut water"
        elif "cold" in q_lower:
            reply = "🤧 **COLD:**\n🩺 Steam 2 times, keep warm\n💊 Cetzine, Vicks rub\n🥗 Hot soup, ginger tea"
        elif "cough" in q_lower:
            reply = "😮‍💨 **COUGH:**\n🩺 Salt water gargle, wear mask\n💊 Honey+ginger, Ascoril syrup"
        elif "headache" in q_lower:
            reply = "🤕 **HEADACHE:**\n🩺 Dark room, no phone, sleep well\n💊 Paracetamol, head massage"
        elif "stomach" in q_lower:
            reply = "🤢 **STOMACH PAIN:**\n🩺 No spicy, jeera water, rest\n💊 Digene, Eno\n🥗 Curd rice, banana"
        elif "vomit" in q_lower:
            reply = "🤮 **VOMITING:**\n🩺 No food 1 hour, sip water only\n💊 Perinorm, lemon water\n🥗 ORS, coconut water later"
        elif "diarrhea" in q_lower or "loose motion" in q_lower:
            reply = "🚽 **DIARRHEA:**\n🩺 Drink ORS, no oily food\n💊 Eldoper, ORS powder\n🥗 Banana, curd rice"
        elif "sore throat" in q_lower or "throat pain" in q_lower or "throat" in q_lower:
            reply = "😣 **SORE THROAT:**\n🩺 Warm salt gargle 3 times\n💊 Azithromycin (doctor advice)\n🥗 Warm water, honey"
        elif "chest pain" in q_lower or "chest" in q_lower:
            reply = "💔 **CHEST PAIN - EMERGENCY:**\n🩺 Sit, rest, don't walk\n⚠️ Go to Tiruvuru Govt Hospital IMMEDIATELY\n📞 Call 108"
        elif "back pain" in q_lower or "back" in q_lower:
            reply = "🦴 **BACK PAIN:**\n🩺 No heavy lift, hot bag\n💊 Diclofenac gel, Move spray\n🥗 Straight sleep"
        elif "knee" in q_lower or "joint" in q_lower:
            reply = "🦵 **KNEE/JOINT PAIN:**\n🩺 Hot bag, no long standing\n💊 Calcium, oil massage\n🥗 Milk, ragi"
        elif "diabetes" in q_lower or "sugar" in q_lower:
            reply = "🍬 **DIABETES:**\n🩺 No sugar, walk 30 min daily\n💊 Check sugar, tablet as doctor said\n🥗 Millets, vegetables"
        elif "bp" in q_lower or "blood pressure" in q_lower or "pressure" in q_lower:
            reply = "❤️ **BP:**\n🩺 Less salt, no tension, walk\n💊 BP tablet regular\n🥗 Less oil, fruits"
        elif "dizziness" in q_lower or "dizzy" in q_lower:
            reply = "😵‍💫 **DIZZINESS:**\n🩺 Sit, drink water\n💊 Vertin, check BP\n🥗 Glucose water"
        elif "allergy" in q_lower or "itch" in q_lower:
            reply = "🤧 **ALLERGY/ITCHING:**\n🩺 No dust, clean clothes\n💊 Cetzine, coconut oil\n🥗 Neem bath"
        elif "acidity" in q_lower or "gas" in q_lower or "heartburn" in q_lower:
            reply = "🔥 **ACIDITY/GAS:**\n🩺 Eat on time, walk after food\n💊 Pantop D, Gelusil\n🥗 Cold milk, banana"
        elif "eye" in q_lower:
            reply = "👁️ **EYE PAIN/REDNESS:**\n🩺 No mobile, wash with clean water\n💊 Eye drops (Ciplox), cold cloth\n⚠️ Go to eye doctor if 2 days"
        elif "ear" in q_lower:
            reply = "👂 **EAR PAIN:**\n🩺 No water inside, no earbud\n💊 Ear drops, warm cloth\n⚠️ ENT doctor if severe"
        elif "tooth" in q_lower or "teeth" in q_lower:
            reply = "🦷 **TOOTH PAIN:**\n🩺 Salt water gargle, clove oil\n💊 Ketorol DT, brush 2 times\n⚠️ Dentist visit"
        elif "skin" in q_lower or "rash" in q_lower or "pimple" in q_lower:
            reply = "🧴 **SKIN RASH:**\n🩺 Keep clean, no scratching\n💊 Candid powder, coconut oil\n🥗 Neem, turmeric"
        elif "wound" in q_lower or "cut" in q_lower or "bleed" in q_lower:
            reply = "🩹 **WOUND/CUT:**\n🩺 Wash with Dettol, apply Betadine\n💊 Bandage, TT injection if needed\n⚠️ Hospital if deep cut"
        elif "constipation" in q_lower:
            reply = "😣 **CONSTIPATION:**\n🩺 Drink more water, walk\n💊 Loose syrup, fiber foods\n🥗 Papaya, banana, vegetables"
        elif "asthma" in q_lower or "breathing" in q_lower:
            reply = "😤 **ASTHMA/BREATHING PROBLEM:**\n🩺 Sit, no dust, inhaler if you have\n⚠️ Go to hospital if breathless\n💊 Asthalin inhaler"
        elif "malaria" in q_lower:
            reply = "🦟 **MALARIA (SUSPECT):**\n🩺 Fever with chills\n⚠️ Blood test needed - Go to Govt Hospital\n💊 Do not self-medicate"
        elif "dengue" in q_lower:
            reply = "🦟 **DENGUE (SUSPECT):**\n🩺 High fever, body pains, platelets low\n⚠️ Blood test - Go to Govt Hospital\n🥗 Papaya leaf juice, coconut water"
        elif "typhoid" in q_lower:
            reply = "🤒 **TYPHOID (SUSPECT):**\n🩺 Continuous fever, stomach pain\n⚠️ Widal test needed\n💊 Doctor antibiotics needed"
        else:
            reply = f"For '{q}':\n🩺 Take rest, drink 3L water, sleep 8 hours.\n🥗 Eat light food.\n⚠️ If severe or 2+ days, visit Tiruvuru Govt Hospital."

        st.chat_message("assistant").write(reply)

        # AUTO VOICE + BUTTON BOTH - FOR ILLITERATE HELP
        st.write("🔊 **AI Speaking - For those who can't read:**")
        speak(reply)

        st.write("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔊 Malli Vinu / Replay Voice"):
                speak(reply)
        with col2:
            report_text = f"""Medical Assistant - Tiruvuru
Date: {datetime.now()}
Symptom: {q}
Advice: {reply}
Note: Educational purpose only, consult real doctor.
Hospital: Tiruvuru Govt Hospital
"""
            st.download_button("📄 Download Prescription", data=report_text, file_name="Prescription.txt", mime="text/plain", use_container_width=True)

# FEATURE 2: MEDICINE INFO
elif feature == "💊 Medicine Info":
    st.subheader("💊 Medicine Information")
    med = st.selectbox("Select Medicine", ["Dolo 650", "Cetzine", "Digene", "Pantop D", "Azithromycin", "Metformin", "ORS", "Diclofenac Gel", "Paracetamol"])
    med_data = {
        "Dolo 650": "Use: Fever, headache, body pain. Dose: 1 tab after food, max 3 per day. Note: Educational only, ask doctor.",
        "Cetzine": "Use: Cold, allergy, sneezing, itching. Dose: 1 at night. Side: Sleepy. No driving.",
        "Digene": "Use: Gas, acidity, stomach pain. Dose: 10ml after food. No spicy food.",
        "Pantop D": "Use: Acidity, heartburn, gas. Dose: 1 before breakfast empty stomach.",
        "Azithromycin": "Use: Throat infection. Dose: Doctor prescription must - 3 days course. Don't self take.",
        "Metformin": "Use: Diabetes sugar control. Dose: Only as doctor said. Walk daily must.",
        "ORS": "Use: Loose motion, vomiting, dehydration. Mix 1 packet in 1L water. Must for kids.",
        "Diclofenac Gel": "Use: Back pain, knee pain. Apply on pain area 2 times. External only.",
        "Paracetamol": "Use: Fever, headache. Dose: 500mg adults after food. Safe."
    }
    st.info(med_data[med])
    if st.button(f"🔊 Voice for {med}"):
        speak(med_data[med])

# FEATURE 3: HEALTH TIPS & YOGA
elif feature == "🧘 Health Tips & Yoga":
    st.subheader("🧘 Health Tips & Yoga")
    tab1, tab2 = st.tabs(["🌿 Health Tips", "🧘 Yoga"])
    with tab1:
        st.write("""
        **Morning 6 AM:** 2 glass warm water, Walk 30 min, Millets + fruits
        **Afternoon:** Curd rice, veggies, 3L water, No oily fast food
        **Night:** Sleep 10 PM, 8 hours, No phone 1 hour before, Light dinner
        """)
    with tab2:
        st.write("""
        - 🧘 **Anulom Vilom (10 min):** For BP, cold, headache, stress
        - 🧘 **Vajrasana (5 min after food):** For gas, acidity, digestion
        - 🧘 **Bhujangasana:** For back pain
        - 🧘 **Tadasana:** For height, back, posture
        - 🧘 **Walking 30 min:** Best for diabetes, BP, knee pain
        """)
        if st.button("🔊 Play Yoga Voice"):
            speak("Yoga tips: Anulom Vilom for BP and headache, Vajrasana after food for acidity, Bhujangasana for back pain, walk 30 minutes daily for diabetes.")

# FEATURE 4: EMERGENCY ALERT
elif feature == "🚨 Emergency Alert":
    st.subheader("🚨 Emergency Alert - Tiruvuru")
    st.error("📞 EMERGENCY? CALL NOW")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**🚑 108 - Ambulance**\n**🚓 100 - Police**\n**🔥 101 - Fire**")
    with c2:
        st.write("**🏥 Tiruvuru Govt Hospital**\n**🏥 Vijayawada Govt Hospital**\n**👨‍⚕️ 24/7 Doctor**")
    st.write("---")
    st.write("**If Chest Pain / Accident / Bleeding / Breathless:**\n1. Call 108\n2. Don't move patient\n3. Go to nearest Govt Hospital")
    if st.button("🔊 Emergency Voice"):
        speak("Emergency: If chest pain, accident, heavy bleeding, breathless, call 108 now. Go to Tiruvuru Government Hospital.")

# FEATURE 5: AI CHATBOT 24/7
elif feature == "🤖 AI Chatbot 24/7":
    st.subheader("🤖 AI Chatbot 24/7 - Ask Anything")
    q2 = st.chat_input("Ask me... Ex: What food for diabetes? Hello?")
    if q2:
        st.chat_message("user").write(q2)
        ql = q2.lower()
        if "hi" in ql or "hello" in ql:
            ans = "Hello! I am Tiruvuru Medical AI, 24/7 available. Tell symptom like fever, cold, BP, sugar? Or ask health tips, food, exercise?"
        elif "food" in ql:
            ans = "Healthy Food: Millets, vegetables, fruits, curd rice, coconut water, 3L water. Avoid oily, spicy, sugar, fast food."
        elif "exercise" in ql:
            ans = "Daily: Walk 30 min, yoga 15 min. Good for diabetes, BP, back pain, weight loss."
        else:
            ans = f"For '{q2}': Take rest, drink water, sleep 8 hours. For detailed advice go to AI Doctor Chat 30+ Symptoms."
        st.chat_message("assistant").write(ans)
        speak(ans)
        if st.button("🔊 Replay Voice"):
            speak(ans)

# FEATURE 6: IMAGE ANALYZER
elif feature == "📸 Image Analyzer":
    st.subheader("📸 Image Analyzer - Upload Medical Image")
    img = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])
    if img:
        image = Image.open(img)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        st.info("Educational only. Consult doctor for real diagnosis. Keep image clean, good light.")
        if st.button("🔊 Voice Info"):
            speak("Image uploaded. This is educational only. Consult real doctor for diagnosis.")

# FEATURE 7: ABOUT
else:
    st.subheader("ℹ️ About Project")
    st.write("""
    **Tiruvuru Medical Pro Max - Made by Nageena ❤️**
    **7 Features:**
    1. AI Doctor Chat - 30+ Symptoms + Voice + Download
    2. Medicine Info - 9 Medicines
    3. Health Tips & Yoga
    4. Emergency Alert 108
    5. AI Chatbot 24/7
    6. Image Analyzer
    7. About

    **Special:** Auto Voice for illiterate people + Replay Button
    **For:** Tiruvuru People Health Awareness
    **Note:** Educational Only, Not Real Doctor
    """)

