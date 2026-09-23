import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Medical Assistant - Tiruvuru", layout="centered")

st.warning("⚠️ Educational Purpose Only - Consult Real Doctor")

st.title("🏥 Medical Assistant Pro Max - Tiruvuru")

# Sidebar
feature = st.sidebar.selectbox("Select Feature", ["AI Doctor Chat", "Image Analyzer", "About"])

# 1. AI DOCTOR CHAT
if feature == "AI Doctor Chat":
    st.subheader("Chat with AI Doctor")
    
    q = st.chat_input("Type your symptom in English... Ex: I have fever")
    
    if q:
        st.chat_message("user").write(q)
        
        if "fever" in q.lower():
            st.chat_message("assistant").write(
                "🤒 **FEVER:**\n"
                "🩺 Precaution: Rest, drink water, cold cloth on forehead\n"
                "💊 Tablet: Dolo 650 after food\n"
                "🥗 Food: Khichdi, coconut water, fruits\n"
                "⚠️ If 2 days more, visit Tiruvuru Govt Hospital"
            )
        elif "cold" in q.lower():
            st.chat_message("assistant").write(
                "🤧 **COLD:**\n"
                "🩺 Precaution: Steam inhalation 2 times, keep warm\n"
                "💊 Tablet: Cetzine at night, Vicks rub\n"
                "🥗 Food: Hot soup, ginger tea\n"
            )
        elif "headache" in q.lower():
            st.chat_message("assistant").write(
                "🤕 **HEADACHE:**\n"
                "🩺 Precaution: Sleep well, no phone, dark room rest\n"
                "💊 Tablet: Paracetamol, head massage\n"
                "🥗 Food: Drink more water"
            )
        elif "stomach" in q.lower() or "pain" in q.lower():
            st.chat_message("assistant").write(
                "🤢 **STOMACH PAIN:**\n"
                "🩺 Precaution: No spicy food, drink jeera water\n"
                "💊 Tablet: Digene, Eno\n"
                "🥗 Food: Curd rice, banana"
            )
        elif "cough" in q.lower():
            st.chat_message("assistant").write(
                "😮‍💨 **COUGH:**\n"
                "🩺 Precaution: Salt water gargle, wear mask\n"
                "💊 Tablet: Honey+ginger, cough syrup\n"
                "🥗 Food: Warm water, tulsi tea"
            )
        else:
            st.chat_message("assistant").write(
                f"For '{q}':\n"
                "🩺 Take rest and drink plenty of water.\n"
                "If severe, visit Tiruvuru Govt Hospital."
            )

        # DOWNLOAD BUTTON ALWAYS VISIBLE - ENGLISH
        st.write("---")
        report_text = f"""Medical Assistant - Tiruvuru
Date: {datetime.now()}
Symptom: {q}
Advice: Provided above based on symptom.
Note: Educational purpose only, consult real doctor.
"""
        st.download_button(
            "📄 Download Prescription PDF",
            data=report_text,
            file_name="Tiruvuru_Prescription.txt",
            mime="text/plain",
            use_container_width=True
        )

# 2. IMAGE ANALYZER
elif feature == "Image Analyzer":
    st.subheader("📸 Image Analyzer")
    st.write("Upload wound/skin image for basic info (Educational only)")
    img = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])
    if img:
        st.image(img, caption="Uploaded Image")
        st.info("This is for educational purpose only. Please consult doctor.")

# 3. ABOUT
else:
    st.subheader("About")
    st.write("This app is made for Tiruvuru people for basic health education.")
    st.write("Made by Nageena - Educational Project")
