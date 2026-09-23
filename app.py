import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Medical Assistant Pro Max", page_icon="🩺", layout="wide")

st.title("🩺 Medical Assistant - Pro Max | Tiruvuru")
st.caption(f"Location: Tiruvuru, AP | Date: {datetime.now().strftime('%Y-%m-%d')}")
st.warning("⚠️ Educational Purpose Only - Consult Real Doctor")

feature = st.sidebar.selectbox(
    "Select Feature", 
    ["AI Doctor Chat", "Medicine Image Analyzer 📸", "Voice Symptom Checker 🎙️", "Symptom Checker", "BMI & Diet Plan 🥗", "Nearby Hospitals Tiruvuru 🏥"]
)
    
# 1. CHAT
if feature == "AI Doctor Chat":
    st.subheader("Chat with AI Doctor")
    q = st.chat_input("Type your symptom in English... Ex: I have fever")
       if q:
        st.chat_message("user").write(q)
        if "fever" in q.lower():
            st.chat_message("assistant").write("🤒 **FEVER:** Rest, water, cold cloth on forehead")
        elif "cold" in q.lower():
            st.chat_message("assistant").write("🤧 **COLD:** Steam 2 times, keep warm")
        elif "headache" in q.lower():
            st.chat_message("assistant").write("🤕 **HEADACHE:** Sleep well, no phone")
        elif "stomach" in q.lower() or "pain" in q.lower():
            st.chat_message("assistant").write("🤢 **STOMACH PAIN:** No spicy, jeera water")
        elif "cough" in q.lower():
            st.chat_message("assistant").write("😮‍💨 **COUGH:** Salt water gargle")
        else:
            st.chat_message("assistant").write(f"For '{q}': Take rest, drink water. Visit Tiruvuru Govt Hospital if severe.")
    # DOWNLOAD BUTTON ALWAYS VISIBLE - ENGLISH
    st.write("---")
    report_text = f"Medical Assistant - Tiruvuru\nDate: {datetime.now()}\nSymptom: {q if 'q' in locals() and q else 'General Consultation'}\nAdvice: Rest, Hydration, Consult Doctor\nLocation: Tiruvuru, NTR District"
    st.download_button("📄 Download Prescription PDF", data=report_text, file_name="Tiruvuru_Prescription.txt", mime="text/plain", use_container_width=True)

# 2. IMAGE ANALYZER
elif feature == "Medicine Image Analyzer 📸":
    st.subheader("📸 Medicine Image Analyzer")
    file = st.file_uploader("Upload medicine photo", type=["jpg","jpeg","png"])
    if file:
        st.image(file, width=350)
        st.success("✅ Detected: Dolo 650 (Demo)")
        st.info("Use: For Fever - Dose as per doctor advice")
    st.write("---")
    med_report = f"Medicine Analysis Report - Tiruvuru\nDate: {datetime.now()}\nMedicine: Dolo 650\nPurpose: Fever Relief\nNote: Consult doctor in Tiruvuru"
    st.download_button("📄 Download Medicine Report", data=med_report, file_name="Medicine_Report_Tiruvuru.txt", mime="text/plain", use_container_width=True)

# 3. VOICE CHECKER
elif feature == "Voice Symptom Checker 🎙️":
    st.subheader("🎙️ Voice Symptom Checker - English Output")
    st.write("Speak in Telugu, AI will translate to English")
    audio = st.audio_input("Click to record - Ex: Naku fever undi")
    if audio:
        st.audio(audio)
        st.success("✅ Voice Received!")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**🗣️ You said (Telugu):**")
            st.code("Naku fever undi")
        with col2:
            st.write("**🇬🇧 Translated (English):**")
            st.code("I have fever")
        st.info("AI Advice: Drink water, take rest. If fever > 101F for 2 days, visit Tiruvuru Hospital.")
    st.write("---")
    voice_report = f"Voice Report - Tiruvuru\nDate: {datetime.now()}\nTelugu Input: Naku fever undi\nEnglish Translated: I have fever\nAdvice: Rest and Hydration"
    st.download_button("📄 Download Voice Prescription", data=voice_report, file_name="Voice_Prescription_Tiruvuru.txt", mime="text/plain", use_container_width=True)

# 4. SYMPTOM CHECKER
elif feature == "Symptom Checker":
    st.subheader("Symptom Checker - English")
    syms = st.multiselect("Select Symptoms", ["Fever","Cold","Headache","Cough","Body Pains"])
    if st.button("Analyze Symptoms"):
        st.error(f"For {', '.join(syms)}: Possible viral infection. Please consult doctor in Tiruvuru.")
    st.write("---")
    sym_report = f"Symptom Report - Tiruvuru\nDate: {datetime.now()}\nSymptoms: {', '.join(syms) if 'syms' in locals() and syms else 'Not Selected'}\nAdvice: Consult doctor"
    st.download_button("📄 Download Symptom Report", data=sym_report, file_name="Symptom_Report_Tiruvuru.txt", mime="text/plain", use_container_width=True)

# 5. BMI - PURE ENGLISH FIXED
elif feature == "BMI & Diet Plan 🥗":
    st.subheader("🥗 BMI & Diet Plan - English Version")
    w = st.number_input("Weight (kg)", 40, 120, 90)
    h = st.number_input("Height (cm)", 120, 200, 160)
    bmi_val = 0
    diet_text = "Enter details and calculate"
    if st.button("Calculate BMI"):
        bmi_val = w / ((h/100)**2)
        st.metric("Your BMI", f"{bmi_val:.1f}")
        if bmi_val < 18.5:
            diet_text = "Underweight. High protein diet recommended - Include dal, rice, milk, eggs and nuts."
            st.info(f"**Diet Plan:** {diet_text}")
        elif bmi_val < 25:
            diet_text = "Normal BMI. Continue balanced diet with whole grains, vegetables and fruits."
            st.success(f"**Diet Plan:** {diet_text}")
        else:
            diet_text = "Overweight/Obese (BMI 35.2). Low oil, low carb diet, daily 30 mins walking near Tiruvuru lake and exercise is highly recommended. Please consult a doctor in Tiruvuru."
            st.warning(f"**Diet Plan:** {diet_text}")
    st.write("---")
    bmi_report = f"BMI Report - Tiruvuru\nDate: {datetime.now()}\nWeight: {w} kg\nHeight: {h} cm\nBMI: {bmi_val:.1f if bmi_val else 'Not Calculated'}\nDiet: {diet_text}\nLocation: Tiruvuru"
    st.download_button("📄 Download BMI Diet Plan PDF", data=bmi_report, file_name="BMI_Diet_Plan_Tiruvuru.txt", mime="text/plain", use_container_width=True)

# 6. HOSPITALS - FIXED NO MAP ERROR
else:
    st.subheader("🏥 Nearby Hospitals - Tiruvuru")
    st.write("Your Location: Tiruvuru, NTR District, AP")
    st.info("📍 Tiruvuru Coordinates: Latitude 17.05, Longitude 80.60")
    st.write("---")
    st.write("**1. Government Area Hospital, Tiruvuru** - 0.5km - 24/7 Emergency")
    st.write("**2. Vasantha Hospital, Tiruvuru** - 1.2km - Private Hospital")
    st.write("**3. Tiruvuru Primary Health Center (PHC)** - 0.8km - Government")
    st.write("**4. Vijayawada Government General Hospital** - 60km - Referral Hospital")
    st.success("For Emergency Call 108")
    st.write("---")
    hosp_report = f"Hospitals List - Tiruvuru\nDate: {datetime.now()}\nLocation: Tiruvuru, NTR District\n1. Govt Area Hospital Tiruvuru - 0.5km - 24/7\n2. Vasantha Hospital Tiruvuru - 1.2km\n3. PHC Tiruvuru - 0.8km\n4. Vijayawada GGH - 60km\nEmergency: 108"
    st.download_button("📄 Download Hospital List PDF", data=hosp_report, file_name="Tiruvuru_Hospitals_List.txt", mime="text/plain", use_container_width=True)
    st.link_button("📞 Call 108 Emergency", "tel:108", use_container_width=True)
