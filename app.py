import streamlit as st
import os
import subprocess

st.title("🎬 AI Video Factory v10.0")
st.subheader("Ultimate Deep Metadata Purge Web App")
st.write("अपनी वीडियो अपलोड करो, इसका डिजिटल इतिहास जड़ से साफ़ हो जाएगा।")

# फाइल अपलोडर
uploaded_file = st.file_uploader("वीडियो फाइल चुनें (.mp4)", type=["mp4"])

if uploaded_file is not None:
    # फाइल लोड होने का मैसेज
    st.info(f"📥 फाइल सफलतापूर्वक लोड हुई: {uploaded_file.name}")
    
    # प्रोसेस करने का बटन
    if st.button("🚀 स्टार्ट पावरफुल मेटाडेटा क्लियर"):
        # अस्थाई रूप से इनपुट फाइल को सेव करना
        input_filename = "temp_input.mp4"
        output_filename = "clean_output.mp4"
        
        # पुराना आउटपुट अगर मौजूद हो तो डिलीट करना
        if os.path.exists(output_filename):
            os.remove(output_filename)
            
        with open(input_filename, "wb") as f:
            f.write(uploaded_file.read())
            
        # स्टेटस दिखाना
        with st.spinner("गहन मेटाडेटा सफाई जारी है... कृपया रुकें..."):
            try:
                # FFmpeg कमांड जो सारा मेटाडेटा साफ कर देती है
                cmd = [
                    "ffmpeg", "-y", "-i", input_filename,
                    "-map_metadata", "-1", "-c:v", "copy", "-c:a", "copy",
                    output_filename
                ]
                
                # कमांड रन करना
                result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                if os.path.exists(output_filename):
                    st.success("🎉 मेटाडेटा पूरी तरह साफ़ हो चुका है!")
                    
                    # डाउनलोड बटन दिखाना
                    with open(output_filename, "rb") as file:
                        st.download_button(
                            label="📥 क्लीन वीडियो डाउनलोड करें",
                            data=file,
                            file_name=f"clean_{uploaded_file.name}",
                            mime="video/mp4"
                        )
                else:
                    st.error("FFmpeg फाइल बनाने में असमर्थ रहा।")
                    st.code(result.stderr)
                    
            except Exception as e:
                st.error(f"त्रुटि: {e}")
                
            finally:
                # काम होने के बाद अस्थाई इनपुट फाइल हटाना
                if os.path.exists(input_filename):
                    os.remove(input_filename)
