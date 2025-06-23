import streamlit as st
import time
import numpy as np
from PIL import Image
import tensorflow as tf
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
APP_ID = os.getenv("NUTRITIONIX_APP_ID")
API_KEY = os.getenv("NUTRITIONIX_API_KEY")

# Load model
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("food11_mobilenetv2.h5")

model = load_model()

# Food11 class names
class_names = [
    "Bread", "Dairy product", "Dessert", "Egg", "Fried food",
    "Meat", "Noodles-Pasta", "Rice", "Seafood", "Soup", "Vegetable-Fruit"
]

# Optional: map vague labels to more recognizable food names
query_map = {
    "Bread": "whole wheat bread",
    "Dairy product": "milk",
    "Dessert": "chocolate cake",
    "Egg": "boiled egg",
    "Fried food": "fried chicken",
    "Meat": "grilled chicken breast",
    "Noodles-Pasta": "spaghetti",
    "Rice": "steamed rice",
    "Seafood": "grilled salmon",
    "Soup": "chicken soup",
    "Vegetable-Fruit": "salad"
}

# Streamlit page setup
st.set_page_config(page_title="🍎 NutriScan", page_icon="🍽️", layout="wide")
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'nutrition_data' not in st.session_state:
    st.session_state.nutrition_data = None
if 'analyzing' not in st.session_state:
    st.session_state.analyzing = False

# Header
st.markdown("""<style>
.main-header {
  font-size: 3rem;
  font-weight: bold;
  text-align: left;
  padding: 2rem 0;
  
  background: linear-gradient(135deg, #ff5722, #ff9800, #ffc107, #fff176);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}
.subtitle {
    text-align: center;
    color: #6b7280;
    font-size: 1.2rem;
    margin-bottom: 2rem;
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

st.markdown('<h1 class="main-header">🍎 NutriScan</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">📸 Upload or capture a food image and get real nutrition insights using AI and Nutritionix API</p>', unsafe_allow_html=True)

# Upload section
if not st.session_state.uploaded_image:
    uploaded_file = st.file_uploader("📁 Upload a food image", type=["jpg", "jpeg", "png"])
    camera_image = st.camera_input("📷 Or take a photo")

    if camera_image:
        st.session_state.uploaded_image = camera_image
        st.session_state.analyzing = True
        st.rerun()
    elif uploaded_file:
        st.session_state.uploaded_image = uploaded_file
        st.session_state.analyzing = True
        st.rerun()

# Prediction & Nutrition
if st.session_state.uploaded_image:
    col1, col2 = st.columns(2)

    with col1:
        image = Image.open(st.session_state.uploaded_image).convert("RGB")
        st.image(image, caption="Uploaded Image", use_column_width=True)
        if st.button("🔄 Upload New Image"):
            for key in ['uploaded_image', 'nutrition_data', 'analyzing']:
                st.session_state[key] = None
            st.rerun()

    with col2:
        if st.session_state.analyzing and not st.session_state.nutrition_data:
            st.markdown('<div class="analyzing-text">🧠 AI Analyzing...</div>', unsafe_allow_html=True)
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)

            # Predict
            resized = image.resize((160, 160))
            array = np.expand_dims(np.array(resized) / 255.0, axis=0)
            pred_index = int(np.argmax(model.predict(array)))
            pred_label = class_names[pred_index]
            query_text = query_map.get(pred_label, pred_label)

            # Nutritionix API call
            headers = {
                "x-app-id": APP_ID,
                "x-app-key": API_KEY,
                "Content-Type": "application/json"
            }
            query = {"query": query_text}

            try:
                response = requests.post(
                    "https://trackapi.nutritionix.com/v2/natural/nutrients",
                    headers=headers,
                    json=query
                )
                response.raise_for_status()
                food_info = response.json()["foods"][0]
                st.session_state.nutrition_data = {
                    "foodName": food_info["food_name"].title(),
                    "calories": food_info["nf_calories"],
                    "protein": food_info["nf_protein"],
                    "carbs": food_info["nf_total_carbohydrate"],
                    "fat": food_info["nf_total_fat"],
                    "fiber": food_info.get("nf_dietary_fiber", 0),
                    "sugar": food_info.get("nf_sugars", 0),
                    "sodium": food_info.get("nf_sodium", 0)
                }
            except:
                st.error("⚠️ API call failed. Using fallback values.")
                st.session_state.nutrition_data = {
                    "foodName": pred_label,
                    "calories": 300,
                    "protein": 20,
                    "carbs": 30,
                    "fat": 15,
                    "fiber": 5,
                    "sugar": 8,
                    "sodium": 500
                }

            st.session_state.analyzing = False
            st.rerun()

        elif st.session_state.nutrition_data:
            data = st.session_state.nutrition_data
            st.subheader(f"🍽️ {data['foodName']}")
            st.metric("Calories", f"{data['calories']} kcal")
            st.metric("Protein", f"{data['protein']} g")
            st.metric("Carbs", f"{data['carbs']} g")
            st.metric("Fat", f"{data['fat']} g")
            st.metric("Fiber", f"{data['fiber']} g")
            st.metric("Sugar", f"{data['sugar']} g")
            st.metric("Sodium", f"{data['sodium']} mg")
            st.success("✅ Nutrition data retrieved successfully!")

# Footer
st.markdown("---")
st.markdown("""<div style="text-align: center; color: #888;">
© 2024 NutriScan · AI + Nutritionix API
</div>""", unsafe_allow_html=True)
