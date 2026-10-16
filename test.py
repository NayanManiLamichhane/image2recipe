import json
import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow import keras
from keras import models

model=models.load_model(
    'food101_model_patched.keras',
    compile=False
)

with open("class_names.json","r") as file:
    class_names=json.load(file)

print("Model loaded Successfully!")
print("Input shape:", model.input_shape)
print("Output shape:", model.output_shape)

image_path="test_image.jpg"

image=Image.open(image_path).convert("RGB")
image=image.resize((224,224))

image_array=np.array(image,dtype=np.float32)

image_array = np.expand_dims(image_array, axis=0)
print("Image shape:", image_array.shape)

predictions = model.predict(image_array, verbose=0)[0]

top_indices = np.argsort(predictions)[-3:][::-1]

print("FOOD PREDICTIONS")

for index in top_indices:
    food_name=class_names[int(index)]
    confidence=float(predictions[index])

    print(f"{food_name}: {confidence:.2%}")

best_index=int(np.argmax(predictions))

print("\nPredicted food:", class_names[best_index])
print(f"Confidence score: {predictions[best_index]:.2%}")