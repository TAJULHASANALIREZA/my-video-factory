import streamlit as st
import os
import subprocess

st.set_page_config(page_title="AI Video Factory v11.0", page_icon="🎬", layout="centered")

st.title("🎬 AI Video Factory v11.0")
st.subheader("Ultimate Deep Metadata Purge Web App")
st.write("अपनी वीडियो अपलोड करो, इसका डिजिटल इतिहास जड़ से साफ़ हो जाएगा।")

# --- फ्री ट्रायल सिस्टम (Session State) ---
if "trials_left" not in st.session_state:
    st.session_state.trials_left = 2

st.sidebar.markdown("### 📊 आपका अकाउंट स्टेटस")
if st.session_state.trials_left > 0:
    st.sidebar.success(f"🟢 फ्री ट्रायल बाकी: {st.session_state.trials_left}")
else:
    st.sidebar.error("🔴 फ्री ट्रायल समाप्त!")

# --- मुख्य लॉजिक ---
if st.session_state.trials_left > 0:
    # फाइल अपलोडर
    uploaded_file = st.file_uploader("वीडियो फाइल चुनें (.mp4)", type=["mp4"])

    if uploaded_file is not None:
        st.info(f"📥 फाइल सफलतापूर्वक लोड हुई: {uploaded_file.name}")
        
        if st.button("🚀 स्टार्ट पावरफुल मेटाडेटा क्लियर"):
            input_filename = "temp_input.mp4"
            output_filename = "clean_output.mp4"
            
            if os.path.exists(output_filename):
                os.remove(output_filename)
                
            with open(input_filename, "wb") as f:
                f.write(uploaded_file.read())
                
            with st.spinner("गहन मेटाडेटा सफाई जारी है... कृपया रुकें..."):
                try:
                    cmd = [
                        "ffmpeg", "-y", "-i", input_filename,
                        "-map_metadata", "-1", "-c:v", "copy", "-c:a", "copy",
                        output_filename
                    ]
                    
                    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    
                    if os.path.exists(output_filename):
                        st.success("🎉 मेटाडेटा पूरी तरह साफ़ हो चुका है!")
                        
                        # डाउनलोड बटन
                        with open(output_filename, "rb") as file:
                            st.download_button(
                                label="📥 क्लीन वीडियो डाउनलोड करें",
                                data=file,
                                file_name=f"clean_{uploaded_file.name}",
                                mime="video/mp4"
                            )
                        
                        # सफलतापूर्वक डाउनलोड/प्रोसेस होने पर 1 ट्रायल कम करें
                        st.session_state.trials_left -= 1
                        st.rerun()
                        
                    else:
                        st.error("FFmpeg फाइल बनाने में असमर्थ रहा।")
                        st.code(result.stderr)
                        
                except Exception as e:
                    st.error(f"त्रुटि: {e}")
                    
                finally:
                    if os.path.exists(input_filename):
                        os.remove(input_filename)
else:
    # ट्रायल खत्म होने पर दिखने वाली पेमेंट स्क्रीन (As per Image 28585.jpg)
    st.error("⚠️ आपका फ्री ट्रायल समाप्त हो चुका है!")
    
    st.markdown("### 🔐 आगे इस्तेमाल करने के लिए प्रीमियम प्लान अनलॉक करें")
    st.info("अनलिमिटेड वीडियो मेटाडेटा क्लियर करने के लिए केवल **₹49** का सुरक्षित भुगतान करें।")
    
    # दो कॉलम बनाकर डिटेल्स दिखाना
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        **💳 भुगतान की जानकारी:**
        * **नाम:** tajul saiyyad
        * **बैंक:** State Bank of India
        * **UPI ID:** `tajulwara786@oksbi`
        
        **📱 स्टेप्स:**
        1. ऊपर दी गई **UPI ID** को कॉपी करें या अपने किसी भी पेमेंट ऐप (Google Pay, PhonePe, Paytm) से इस पर **₹49** ट्रांसफर करें।
        2. पेमेंट सफल होने के बाद उसका **स्क्रीनशॉट** लें।
        3. स्क्रीनशॉट हमारे व्हाट्सएप नंबर पर भेजें।
        """)
        
    with col2:
        st.warning("💡 **नोट:** स्क्रीनशॉट वेरीफाई होते ही हमारी टीम बैकएंड से आपका प्रीमियम एक्सेस तुरंत चालू कर देगी।")

