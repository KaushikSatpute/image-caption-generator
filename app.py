import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Custom CSS for Dark Mode, Interactive Upload Box, Modern Buttons, and Animations
st.markdown(
    """
    <style>
        /* Smooth Dark Theme Background */
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        body, .stApp {
            background: linear-gradient(-45deg, #121212, #1e1e1e, #252525);
            background-size: 400% 400%;
            animation: gradientBG 10s ease infinite;
            color: white;
        }

        /* Title Animation */
        @keyframes titleFadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .main-title {
            color: #4CAF50;
            text-align: center;
            font-size: 44px;
            font-weight: bold;
            animation: titleFadeIn 1.5s ease-in-out;
        }

        /* Upload Section - Modern Look */
        .upload-box {
            border: 2px dashed #4CAF50;
            background-color: rgba(255, 255, 255, 0.08);
            padding: 20px;
            border-radius: 12px;
            transition: all 0.3s ease;
            text-align: center;
            font-size: 18px;
        }

        .upload-box:hover {
            transform: scale(1.05);
            background-color: rgba(255, 255, 255, 0.15);
        }

        /* Modern Input Box for API */
        .api-input input {
            border: 2px solid #4CAF50;
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border-radius: 8px;
            padding: 10px;
            font-size: 16px;
        }

        /* Modern Button Styles */
        .stButton>button {
            background: linear-gradient(135deg, #4CAF50 0%, #2E8B57 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease-in-out;
        }

        .stButton>button:hover {
            background: linear-gradient(135deg, #2E8B57 0%, #1E6B43 100%);
            transform: scale(1.05);
        }

        /* Image Hover Effects */
        .stImage {
            border-radius: 15px;
            transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
        }

        .stImage:hover {
            transform: scale(1.02);
            box-shadow: 0px 0px 20px rgba(255, 255, 255, 0.2);
        }

        /* Footer Animation */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            font-size: 16px;
            color: white;
            text-align: center;
            padding: 12px 0;
            background: rgba(76, 175, 80, 0.8);
            animation: fadeIn 2s ease-in-out;
        }

        .footer a {
            color: white;
            text-decoration: none;
            font-weight: bold;
        }

        .footer a:hover {
            color: yellow;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Display Title
st.markdown('<p class="main-title">📸 Image Captioning & Tagging</p>', unsafe_allow_html=True)

# Upload Section with Styled Div
st.markdown('<div class="upload-box">📂 Drag & Drop or Click to Upload an Image</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])

# API Key Input with Styled Box
st.markdown('<div class="api-input">🔑 Enter API Key:</div>', unsafe_allow_html=True)
API_KEY = st.text_input("", type="password")

if uploaded_file is not None:
    if st.button('🚀 Upload & Generate'):
        if API_KEY.strip() == '':
            st.error('❌ Enter a valid API key')
        else:
            # Create temp directory
            os.makedirs("temp", exist_ok=True)

            # Save uploaded file
            file_path = os.path.join("temp", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())

            img = Image.open(file_path)

            try:
                # Configure Google Gemini AI
                genai.configure(api_key=API_KEY)
                model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model

                # Generate Caption and Tags
                caption = model.generate_content(["Write a caption for the image in English:", img])
                tags = model.generate_content(["Generate 5 hashtags for the image in a line in English:", img])

                # Display Uploaded Image
                st.image(img, caption="📌 Uploaded Image")

                # Display Caption
                st.subheader("📝 Caption:")
                st.write(f"**{caption.text}**")

                # Display Tags
                st.subheader("🏷️ Tags:")
                st.write(f"`{tags.text}`")

            except Exception as e:
                error_msg = str(e)
                if "API_KEY_INVALID" in error_msg:
                    st.error("❌ Invalid API Key. Please enter a valid API Key.")
                else:
                    st.error(f"⚠️ Failed to configure API due to: {error_msg}")

# Footer Section
footer = """
    <div class="footer">
        <p>🚀 Built with ❤ by <a href="https://www.linkedin.com/in/kaushik-satpute" target="_blank">Kaushik Satpute</a></p>
    </div>
"""
st.markdown(footer, unsafe_allow_html=True)
