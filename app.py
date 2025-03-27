import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Custom CSS for Dark Theme
st.markdown(
    """
    <style>
        body, .stApp {
            background-color: #121212;  /* Dark Gray Background */
            color: white; /* White Text */
        }
        .stTextInput, .stFileUploader, .stButton>button {
            background-color: #1E1E1E; /* Dark Input Fields */
            color: white;
            border: 1px solid #333;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #1E90FF;  /* Bright Blue Headings */
        }
        .stImage {
            border-radius: 10px; /* Rounded Image */
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('📸 Image Captioning and Tagging')

uploaded_file = st.file_uploader("📂 Choose an image...", type=["jpg", "png", "jpeg"])

API_KEY = st.text_input("🔑 Enter your API Key: Get your Google Studio API key from [here](https://makersuite.google.com/app/apikey)", type="password")

if uploaded_file is not None:
    if st.button('🚀 Upload & Generate'):
        if API_KEY.strip() == '':
            st.error('❌ Enter a valid API key')
        else:
            file_path = os.path.join("temp", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())

            img = Image.open(file_path)

            try:
                genai.configure(api_key=API_KEY)
                model = genai.GenerativeModel('gemini-1.5-flash')  # ✅ Updated Model

                caption = model.generate_content(["Write a caption for the image in English:", img])
                tags = model.generate_content(["Generate 5 hashtags for the image in a line in English:", img])

                st.image(img, caption="📌 Uploaded Image")
                st.subheader("📝 Caption:")
                st.write(f"**{caption.text}**")

                st.subheader("🏷️ Tags:")
                st.write(f"`{tags.text}`")

            except Exception as e:
                error_msg = str(e)
                if "API_KEY_INVALID" in error_msg:
                    st.error("❌ Invalid API Key. Please enter a valid API Key.")
                else:
                    st.error(f"⚠️ Failed to configure API due to: {error_msg}")

# Footer with Developer Name
footer = """
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            font-size: 16px;
            color: white; 
            text-align: center;
            padding: 10px 0;
            background: #1E90FF;  /* Dark Blue Footer */
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

    <div class="footer">
        <p>🚀 Developed with ❤ by <a href="https://www.linkedin.com/in/kaushik-satpute" target="_blank">Kaushik Satpute</a></p>
    </div>
"""
st.markdown(footer, unsafe_allow_html=True)
