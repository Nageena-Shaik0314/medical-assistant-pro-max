import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Medical Assistant - Tiruvuru", layout="centered")
st.warning("⚠️ Educational Purpose Only - Consult Real Doctor")
st.title("🏥 Medical Assistant Pro Max - Tiruvuru")

feature = st.sidebar.selectbox("Select Feature", ["AI Doctor Chat", "Image Analyzer", "About"])

if feature == "AI Doctor Chat":
    st.subheader("Chat with AI Doctor - Type Any Symptom")
    st.caption("Try: fever, cold, cough, stomach pain, vomiting, diabetes, bp, chest pain, etc.")
    
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
        elif "sore throat" in q_lower or "throat pain" in q_lower:
            reply = "😣 **SORE THROAT:**\n🩺 Warm salt gargle 3 times\n💊 Azithromycin (doctor advice)\n🥗 Warm water, honey"
        elif "chest pain" in q_lower:
            reply = "💔 **CHEST PAIN - EMERGENCY:**\n🩺 Sit, rest, don't walk\n⚠️ Go to Tiruvuru Govt Hospital IMMEDIATELY\n📞 Call 108"
        elif "back pain" in q_lower:
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
        elif "cold" not in q_lower and "fever" not in q_lower: # fallback
            reply = f"For '{q}':\n🩺 Take rest, drink 3L water, sleep 8 hours.\n🥗 Eat light food.\n⚠️ If severe or 2+ days, visit Tiruvuru Govt Hospital."

        st.chat_message("assistant").write(reply)

        st.write("---")
        report_text = f"""Medical Assistant - Tiruvuru
Date: {datetime.now()}
Symptom: {q}
Advice: {reply}
Note: Educational purpose only, consult real doctor.
Hospital: Tiruvuru Govt Hospital
"""
        st.download_button("📄 Download Prescription", data=report_text, file_name="Prescription.txt", mime="text/plain", use_container_width=True)

elif feature == "Image Analyzer":
    st.subheader("📸 Image Analyzer")
    img = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])
    if img:
        st.image(img)
        st.info("Educational only. Consult doctor for real diagnosis.")

else:
    st.subheader("About Project")
    st.write("Made for Tiruvuru people - Educational health awareness project.")
    st.write("Features: 30+ Symptoms, Chat Doctor, Prescription Download")
    st.write("Made by Nageena ❤️")
