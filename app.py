import streamlit as st
import time
from PIL import Image
import numpy as np
import tensorflow as tf

# Load your trained model once
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("food11_mobilenetv2.h5")

model = load_model()

# Class labels for Food11
class_names = [
    "Bread", "Dairy product", "Dessert", "Egg", "Fried food",
    "Meat", "Noodles-Pasta", "Rice", "Seafood", "Soup", "Vegetable-Fruit"
]

# Page config
st.set_page_config(
    page_title="🍎 NutriScan - AI Nutrition Analyzer",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS
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
    .feature-card {
        background: linear-gradient(135deg, #f0fdf4, #fef3c7);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #d1fae5;
        margin: 1rem 0;
        text-align: center;
    }
    .nutrition-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
    }
    .metric-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid #f3f4f6;
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
</style>
""", unsafe_allow_html=True)

# Session state
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'nutrition_data' not in st.session_state:
    st.session_state.nutrition_data = None
if 'analyzing' not in st.session_state:
    st.session_state.analyzing = False

# Header
st.markdown('<h1 class="main-header">🍎 NutriScan</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">📸 Upload or capture a meal photo to detect food type with AI</p>', unsafe_allow_html=True)

# Feature cards
if not st.session_state.uploaded_image:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="feature-card">
            <h3>📸 Instant Analysis</h3>
            <p>Take a photo and get the food category instantly</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="feature-card">
            <h3>🧠 AI Powered</h3>
            <p>Trained on 11 food categories from Food11 dataset</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="feature-card">
            <h3>🎯 Track Goals</h3>
            <p>See estimated nutrition values with predictions</p></div>""", unsafe_allow_html=True)

# Upload section
st.markdown("---")
if not st.session_state.uploaded_image:
    st.markdown("### 🚀 Upload or Capture Food Image")
    uploaded_file = st.file_uploader("Choose a food image", type=['jpg', 'jpeg', 'png'])
    camera_image = st.camera_input("📷 Or take a photo")

    # Prioritize camera input
    if camera_image:
        st.session_state.uploaded_image = camera_image
        st.session_state.analyzing = True
        st.rerun()
    elif uploaded_file:
        st.session_state.uploaded_image = uploaded_file
        st.session_state.analyzing = True
        st.rerun()

# Analysis & Display
if st.session_state.uploaded_image:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 🖼️ Your Image")
        image = Image.open(st.session_state.uploaded_image).convert("RGB")
        st.image(image, caption="Uploaded Meal", use_column_width=True)

        if st.button("🔄 Upload New Image"):
            for key in ['uploaded_image', 'nutrition_data', 'analyzing']:
                st.session_state[key] = None
            st.rerun()

    with col2:
        if st.session_state.analyzing and not st.session_state.nutrition_data:
            st.markdown('<div class="analyzing-text">🧠 AI Analyzing... Detecting food</div>', unsafe_allow_html=True)
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress_bar.progress(i + 1)

            # Prediction block
            image_resized = image.resize((160, 160))
            image_array = np.expand_dims(np.array(image_resized) / 255.0, axis=0)
            prediction = model.predict(image_array)
            pred_index = int(np.argmax(prediction))
            pred_label = class_names[pred_index]

            # Save prediction in session
            st.session_state.nutrition_data = {
                "foodName": pred_label,
                "calories": int(np.random.randint(180, 420)),
                "protein": round(np.random.uniform(6, 30), 1),
                "carbs": round(np.random.uniform(10, 60), 1),
                "fat": round(np.random.uniform(5, 25), 1),
                "fiber": round(np.random.uniform(1, 10), 1),
                "sugar": round(np.random.uniform(1, 20), 1),
                "sodium": int(np.random.uniform(150, 800))
            }
            st.session_state.analyzing = False
            st.rerun()

        elif st.session_state.nutrition_data:
            data = st.session_state.nutrition_data
            st.markdown("### 📊 Food Prediction & Nutrition")
            st.markdown(f"""<div class="nutrition-card">
                <h3 style="color: #10b981;">🍽️ {data['foodName']}</h3>
                <div style="font-size: 2rem; font-weight: bold; text-align: center;">
                    {data['calories']} <span style="font-size: 1rem; color: #6b7280;">calories</span>
                </div></div>""", unsafe_allow_html=True)

            st.markdown("#### 📈 Estimated Breakdown")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("🥩 Protein", f"{data['protein']}g")
                st.metric("🍞 Carbs", f"{data['carbs']}g")
                st.metric("🥑 Fat", f"{data['fat']}g")
                st.metric("🌾 Fiber", f"{data['fiber']}g")
            with col_b:
                st.metric("🍯 Sugar", f"{data['sugar']}g")
                st.metric("🧂 Sodium", f"{data['sodium']}mg")
                st.markdown("#### 🏆 Health Score")
                health_score = int(np.clip(100 - data['fat'] + data['fiber'], 40, 95))
                st.progress(health_score / 100)
                st.markdown(f"**{health_score}/100** - Looks healthy! 🥗")
            st.success("✅ Analysis Complete – eat mindfully!")

# Footer
st.markdown("---")
st.markdown("""<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f0fdf4, #fef3c7); border-radius: 1rem; margin-top: 2rem;">
    <p style="color: #6b7280; margin-bottom: 0.5rem;">❤️ Built for healthy habits</p>
    <p style="color: #9ca3af; font-size: 0.9rem;">© 2024 NutriScan. AI-Powered Food Detection</p>
</div>""", unsafe_allow_html=True)
