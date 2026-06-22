import streamlit as st
import os
import subprocess

# --- पेज की मुख्य सेटिंग्स ---
st.set_page_config(
    page_title="Metacorn - Personal VIP Edition", 
    page_icon="🔮", 
    layout="centered"
)

# --- प्रीमियम लुक और टाइटल्स ---
st.title("🔮 Metacorn - VIP Studio")
st.subheader("Ultimate Deep Metadata Purge Web App [Personal Copy]")
st.write("Upload your video to clear its digital history, metadata, and tracking signatures instantly.")

st.sidebar.markdown("### 🖥️ System Status")
st.sidebar.success("👑 VIP ACCESS ACTIVE (No Limits)")
st.sidebar.info("Max File Size Allowed: 5GB")

# --- मेन वीडियो क्लीनर लॉजिक ---
uploaded_file = st.file_uploader("Upload your video file (MP4, MKV, MOV, AVI)", type=["mp4", "mkv", "mov", "avi"])

if uploaded_file is not None:
    # फाइल का नाम और साइज दिखाना
    file_size_mb = uploaded_file.size / (1024 * 1024)
    st.info(f"📁 Selected File: {uploaded_file.name} ({file_size_mb:.2f} MB)")
    
    # क्लीनिंग बटन
    if st.button("🚀 Purge Metadata & Clear Fingerprints"):
        with st.spinner("Processing video... Removing tracking data and cleaning signatures..."):
            try:
                # टेम्परेरी फाइलें सेव करने का रास्ता
                input_path = f"temp_input_{uploaded_file.name}"
                output_path = f"clean_{uploaded_file.name}"
                
                # यूजर की फाइल को लोकल सर्वर पर लिखना
                with open(input_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # FFmpeg कमांड: सारा मेटाडेटा साफ करने और नया फिंगरप्रिंट देने के लिए
                # -map_metadata -1 मेटाडेटा उड़ाता है, -fflags +bitexact टाइमस्टैम्प बदलता है
                command = [
                    "ffmpeg", "-y", "-i", input_path, 
                    "-map_metadata", "-1", 
                    "-c", "copy", 
                    "-fflags", "+bitexact", 
                    "-flags:v", "+bitexact", 
                    "-flags:a", "+bitexact", 
                    output_path
                ]
                
                # कमांड रन करना
                result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                if result.returncode == 0 and os.path.exists(output_path):
                    st.success("✨ Success! Video metadata has been completely sanitized.")
                    
                    # क्लीन वीडियो को डाउनलोड कराने का बटन
                    with open(output_path, "rb") as file:
                        st.download_button(
                            label="📥 Download Cleaned Video",
                            data=file,
                            file_name=f"metacorn_clean_{uploaded_file.name}",
                            mime="video/mp4"
                        )
                else:
                    st.error("❌ FFmpeg processing failed. Check your server logs.")
                    st.code(result.stderr)
                    
            except Exception as e:
                st.error(f"⚠️ An error occurred: {str(e)}")
                
            finally:
                # कचरा साफ करना: काम होने के बाद टेम्परेरी फाइलें सर्वर से डिलीट करना
                if os.path.exists(input_path):
                    os.remove(input_path)
                if os.path.exists(output_path):
                    os.remove(output_path)
