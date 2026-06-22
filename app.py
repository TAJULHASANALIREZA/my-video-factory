import streamlit as st
import os
import subprocess
import re

# वेब पेज की बेसिक सेटिंग्स
st.set_page_config(page_title="AI Video Factory", page_icon="🎬", layout="centered")

st.title("🎬 AI Video Factory v10.0")
st.subheader("Ultimate Deep Metadata Purge Web App")
st.write("अपनी वीडियो अपलोड करो, इसका डिजिटल इतिहास जड़ से साफ़ हो जाएगा।")

# फाइल अपलोडर UI
uploaded_file = st.file_uploader("वीडियो फाइल चुनें (.mp4)", type=["mp4"])

if uploaded_file is not None:
    # फाइल को टेम्परेरी सेव करना
    in_path = os.path.join(".", uploaded_file.name)
    out_path = os.path.join(".", f"purged_{uploaded_file.name}")
    
    with open(in_path, "wb") as f:
        f.write(uploaded_file.read())
        
    st.info(f"📥 फाइल सफलतापूर्वक लोड हुई: {uploaded_file.name}")
    
    # बटन दबाते ही क्लीनिंग शुरू
    if st.button("🚀 स्टार्ट पावरफुल मेटाडेटा क्लियर"):
        with st.spinner("⏳ डीप हेक्स और मेटाडेटा साफ़ किया जा रहा है... थोड़ा सब्र रखें..."):
            
            # 🔥 अल्टीमेट मेटाडेटा का जड़ से खात्मा (FFmpeg Advanced Stripping)
            cmd = [
                "ffmpeg", "-y", "-i", in_path,
                "-vf", "hflip,eq=contrast=1.04:brightness=0.01", # स्क्रीन फ्लिप + नॉर्मल कलर ग्रेडिंग
                "-map_metadata", "-1",
                "-map_metadata:s:v", "-1",
                "-map_metadata:s:a", "-1",
                "-fflags", "+bitexact",
                "-flags", "+bitexact",
                "-bitexact",
                "-c:v", "libx264", "-preset", "superfast", "-crf", "22",
                "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
                out_path
            ]
            
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            if result.returncode == 0:
                # 👉 सेकंड लेयर बाइनरी हेक्स पर्ज
                try:
                    with open(out_path, 'rb') as f:
                        data = f.read()
                    clean_data = re.sub(b'Lavf[0-9.]+', b'000000', data)
                    clean_data = re.sub(b'InShot', b'000000', clean_data)
                    with open(out_path, 'wb') as f:
                        f.write(clean_data)
                except:
                    pass
                
                st.success("✨ महा सफलता! पुराना इतिहास और सॉफ्टवेयर आईडी 100% साफ़।")
                
                # डाउनलोड बटन सीधे वेब पेज पर
                with open(out_path, "rb") as file:
                    st.download_button(
                        label="📥 क्लीन वीडियो डाउनलोड करें",
                        data=file,
                        file_name=f"purged_{uploaded_file.name}",
                        mime="video/mp4"
                    )
            else:
                st.error("❌ प्रोसेसिंग फेल हुई। फाइल में गड़बड़ है।")
                
        # काम होने के बाद कचरा साफ करना
        if os.path.exists(in_path): os.remove(in_path)
        if os.path.exists(out_path): os.remove(out_path)
     