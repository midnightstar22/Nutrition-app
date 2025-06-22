import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# Load model
model = tf.keras.models.load_model("food11_mobilenetv2.h5")

# Map class indices to actual food labels
class_names = [
    "Bread", "Dairy product", "Dessert", "Egg", "Fried food",
    "Meat", "Noodles-Pasta", "Rice", "Seafood", "Soup", "Vegetable-Fruit"
]

# Title
st.title("🍽️ Food Image Classifier (Food11)")

# Upload image
uploaded_file = st.file_uploader("Upload a food image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert('RGB')
    st.image(img, caption='Uploaded Image', use_column_width=True)

    # Preprocess image
    img = img.resize((160, 160))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    prediction = model.predict(img_array)
    predicted_class_index = np.argmax(prediction)
    predicted_label = class_names[predicted_class_index]

    st.subheader(f"🍜 Predicted Class: `{predicted_label}`")
    st.write("🔍 Confidence Scores:")
    for i, score in enumerate(prediction[0]):
        st.write(f"{class_names[i]}: {score:.2f}")
