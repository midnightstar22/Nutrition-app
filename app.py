import numpy as np
from tensorflow.keras.preprocessing import image

# Your class map
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

# Load and preprocess image
img = image.load_img("test.jpg", target_size=(224, 224))
img_array = image.img_to_array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Predict
pred = model.predict(img_array)
predicted_class = np.argmax(pred)

# Print label
print("Predicted class:", class_names[predicted_class])
