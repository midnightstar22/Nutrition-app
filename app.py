import streamlit as st
import time
from PIL import Image
import numpy as np
import tensorflow as tf

# 🧠 Load trained model
model = tf.keras.models.load_model("food11_mobilenetv2.h5")

# 🍱 Class label mapping (edit as per your actual label names if needed)
class_names = [
    "Bread", "Dairy product", "Dessert", "Egg", "Fried food",
    "Meat", "Noodles-Pasta", "Rice", "Seafood", "Soup", "Vegetable-Fruit"
]

# 🎨 Streamlit config
st.set_page_config(
    page_title="🍽️ NutriScan - Food Classifier",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 💄 Custom CSS for styling
st.markdown("""<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #10b981, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .prediction-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
    }
    .analyzing-text {
        text-align: center;
        color: #10b981;
        font-size: 1.2rem;
        font-weight: bold;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
</style>""", unsafe_allow_html=True)

# 🧠 Page header
st.markdown('<h1 class="main-header">🍽️ NutriScan</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">📷 Snap or upload a food photo and get instant predictions!</p>', unsafe_allow_html=True)

# 🖼️ Upload section
image_file = st.file_uploader("Upload a food image", type=["jpg", "jpeg", "png"])
camera_image = st.camera_input("Or take a photo")

final_image = image_file if image_file else camera_image

if final_image:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🖼️ Uploaded Image")
        img = Image.open(final_image).convert('RGB')
        st.image(img, use_column_width=True)

        if st.button("🔄 Upload Another"):
            st.experimental_rerun()

    with col2:
        st.markdown("### 🧠 Predicting...")
        with st.spinner("Analyzing your food image..."):
            time.sleep(1.5)

            # 🛠️ Preprocess
            img_resized = img.resize((160, 160))
            img_array = np.expand_dims(np.array(img_resized) / 255.0, axis=0)

            # 🔮 Predict
            prediction = model.predict(img_array)
            pred_index = np.argmax(prediction)
            pred_label = class_names[pred_index]
            confidence = prediction[0][pred_index]

            # 🎉 Output result
            st.markdown(f"""
            <div class="prediction-card">
                <h3 style="color:#10b981;">🍜 Prediction: {pred_label}</h3>
                <p style="font-size:1.1rem;">Confidence: <b>{confidence*100:.2f}%</b></p>
            </div>
            """, unsafe_allow_html=True)

            # 📊 Confidence bar chart
            st.markdown("### 🔍 Confidence for all classes")
            for i, prob in enumerate(prediction[0]):
                st.progress(prob)
                st.write(f"**{class_names[i]}** — {prob*100:.2f}%")

# 👣 Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem 0;">
    <p style="color: #9ca3af; font-size: 0.9rem;">© 2024 NutriScan • Built with Streamlit & TensorFlow</p>
</div>
""", unsafe_allow_html=True)
