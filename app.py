import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
from nutritionix import get_nutrition_info  # You must define or import this
import io

# Load trained model
model = tf.keras.models.load_model("food11_mobilenetv2.h5")  # Adjust path if needed

# Food11 class labels
class_names = {
    0: "Dairy products",
    1: "Desserts",
    2: "Egg dishes",
    3: "Fried food",
    4: "Meat",
    5: "Noodles/Pasta",
    6: "Rice",
    7: "Seafoods",
    8: "Soup",
    9: "Vegetables/Fruit",
    10: "Other food"
}

# Streamlit app layout
st.title("🍽️ Nutrition App - Food11 Classifier")
st.write("Upload a food image to identify its category and see nutrition info.")

# Upload image
uploaded_file = st.file_uploader("Choose a food image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).resize((224, 224)).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Preprocess the image
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict class
    predictions = model.predict(img_array)
    class_index = int(np.argmax(predictions))
    confidence = float(predictions[0][class_index])
    class_label = class_names[class_index]

    # Display result
    st.info(f"🔢 Class Index: {class_index}")
    st.success(f"🍲 Predicted Food Category: **{class_label}**")
    st.write(f"📊 Confidence: {confidence * 100:.2f}%")

    # Fetch nutrition info (optional)
    with st.spinner("Fetching nutrition info..."):
        nutrition = get_nutrition_info(class_label)

    if "foods" in nutrition:
        food_info = nutrition["foods"][0]
        st.subheader("🧪 Nutrition Facts (per serving)")
        st.write(f"**Calories:** {food_info['nf_calories']} kcal")
        st.write(f"**Carbs:** {food_info['nf_total_carbohydrate']} g")
        st.write(f"**Protein:** {food_info['nf_protein']} g")
        st.write(f"**Fat:** {food_info['nf_total_fat']} g")
    else:
        st.warning("⚠️ Couldn't fetch detailed nutrition data.")
