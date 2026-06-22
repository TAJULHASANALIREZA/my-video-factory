import streamlit as st
import os
import subprocess

st.set_page_config(page_title="AI Video Factory v12.5", page_icon="🎬", layout="centered")

st.title("🎬 AI Video Factory v12.5")
st.subheader("Ultimate Deep Metadata Purge Web App")
st.write("Upload your video, and its digital history will be wiped out instantly.")

# --- सीक्रेट प्रोमो कोड सेटिंग (जिसे चाहो उसे फ्री एक्सेस दो) ---
SECRET_PROMO_CODE = "TAJFREE99"

# --- फ्री ट्रायल सिस्टम (Session State) ---
if "trials_left" not in st.session_state:
    st.session_state.trials_left = 2

if "premium_unlocked" not in st.session_state:
    st.session_state.premium_unlocked = False

st.sidebar.markdown("### 📊 Account Status")
if st.session_state.premium_unlocked:
    st.sidebar.success("👑 PREMIUM UNLOCKED (VIP Access)")
elif st.session_state.trials_left > 0:
    st.sidebar.info(f"🟢 Free Trials Left: {st.session_state.trials_left}")
else:
    st.sidebar.error("🔴 Free Trial Expired!")

# --- मुख्य लॉजिक (डेटा प्राइवेसी के साथ) ---
if st.session_state.trials_left > 0 or st.session_state.premium_unlocked:
    uploaded_file = st.file_uploader("Choose a video file (.mp4)", type=["mp4"])

    if uploaded_file is not None:
        st.info(f"📥 File Loaded Successfully: {uploaded_file.name}")
        
        if st.button("🚀 Start Deep Metadata Purge"):
            input_filename = "temp_input.mp4"
            output_filename = "clean_output.mp4"
            
            if os.path.exists(output_filename):
                os.remove(output_filename)
                
            with open(input_filename, "wb") as f:
                f.write(uploaded_file.read())
                
            with st.spinner("Purging all metadata tracks... Please wait..."):
                try:
                    cmd = [
                        "ffmpeg", "-y", "-i", input_filename,
                        "-map_metadata", "-1", "-c:v", "copy", "-c:a", "copy",
                        output_filename
                    ]
                    
                    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    
                    if os.path.exists(output_filename):
                        st.success("🎉 Metadata completely wiped out!")
                        
                        with open(output_filename, "rb") as file:
                            st.download_button(
                                label="📥 Download Clean Video",
                                data=file,
                                file_name=f"clean_{uploaded_file.name}",
                                mime="video/mp4"
                            )
                        
                        if not st.session_state.premium_unlocked:
                            st.session_state.trials_left -= 1
                            st.rerun()
                        
                    else:
                        st.error("FFmpeg processing failed.")
                        st.code(result.stderr)
                        
                except Exception as e:
                    st.error(f"Error: {e}")
                    
                finally:
                    # सुरक्षा: काम होते ही सर्वर से फाइल तुरंत डिलीट
                    if os.path.exists(input_filename):
                        os.remove(input_filename)
else:
    # --- पूरी तरह सुरक्षित पेमेंट स्क्रीन ---
    st.error("⚠️ Your Free Trial Has Expired!")
    st.markdown("### 🔐 Unlock Premium Plan for Unlimited Access")
    st.info("Get unlimited video metadata clearing securely.")
    
    # VIP प्रोमो कोड बॉक्स
    st.markdown("#### 🎁 Have a VIP Promo Code?")
    user_code = st.text_input("Enter Promo Code here:", placeholder="Type code here...", type="password")
    
    if st.button("Apply Code"):
        if user_code.strip() == SECRET_PROMO_CODE:
            st.session_state.premium_unlocked = True
            st.success("🎉 VIP Access Granted! Premium unlocked for free.")
            st.rerun()
        else:
            st.error("❌ Invalid Promo Code!")
            
    st.markdown("---")
    
    # इंटरनेशनल पेमेंट गेटवे लिंक्स (कोई बैंक या यूपीआई जानकारी टेक्स्ट में नहीं दिखेगी)
    st.markdown("#### 💳 Secure Payment Options:")
    st.write("Click below to pay via our secure international merchant gateway. Your personal financial details are 100% encrypted.")
    
    # सुरक्षित पेमेंट बटन्स (यहाँ तुम अपने PayPal, Stripe, या Razorpay के मर्चेंट लिंक डाल सकते हो)
    st.link_button("🌐 Pay via PayPal ($1.99 USD)", "https://www.paypal.me/your_paypal_username")
    st.link_button("🇮🇳 Pay via UPI / Cards (₹49 INR)", "https://pages.razorpay.com/your_secure_page")
    
    st.warning("📱 After completing the payment, kindly share the confirmation screenshot with our support team to activate your lifetime premium account instantly.")
