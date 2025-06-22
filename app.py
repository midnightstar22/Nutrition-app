import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

# Suppress TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

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

# Load your trained model
model = tf.keras.models.load_model("food11_mobilenetv2.h5")  # <- change this to your actual model path

# Load and preprocess the image
img_path = "your_test_image.jpg"  # <- replace with your test image path
img = image.load_img(img_path, target_size=(224, 224))  # adjust size to match your model
img_array = image.img_to_array(img) / 255.0  # normalize
img_array = np.expand_dims(img_array, axis=0)  # add batch dimension

# Make prediction
predictions = model.predict(img_array)
predicted_class = np.argmax(predictions[0])

# Print food label
print(f"Predicted class: {predicted_class} ({class_names[predicted_class]})")
