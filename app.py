
import streamlit as st
import os
import json
import numpy as np
import tensorflow as tf

from PIL import Image
from dotenv import load_dotenv
from groq import Groq



st.set_page_config(
    page_title="Snap2Recipe AI",
    page_icon="🍳",
    layout="centered"
)

load_dotenv()

#LOAD MODEL
@st.cache_resource

def load_model():
    return tf.keras.models.load_model(
        'food101_model_patched.keras',
        compile=False
    )

@st.cache_data
def load_classes():
    with open("class_names.json", "r", encoding="utf-8") as file:
        classes = json.load(file)

    return classes

# PREDICT FOOD

def predict_food(image,model,classes):
    image=image.convert("RGB").resize((224,224))
    image_array=np.array(image,dtype=np.float32)
    image_array = np.expand_dims(image_array, axis=0)
    
    predictions = model.predict(image_array, verbose=0)[0]

    top_indices = np.argsort(predictions)[-3:][::-1]

    results = [
        {
            "food": classes[int(i)],
            "confidence": float(predictions[i])
        }
        for i in top_indices
    ]
    return results


#GENERATE RECIPE

def generate_recipe(food):
    api_key=os.getenv('GROQ_API_KEY')

    if not api_key:
        raise ValueError("API is missing from your .env file")

    client=Groq(api_key=api_key)

    response=client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role":"system",
                "content":(
                    "You are a cooking assistant. "
                    "Generate clear,practical recipes"
                )
            },
            {
                "role":"user",
                "content": f"""
Generate a recipe for {food}.

Use exactly these sections:

## Ingredients
List every ingredient with its quantity and unit.

## Step-by-Step Instructions
Give numbered, clear cooking instructions.

## Cooking Time
Give the approximate preparation and cooking time.

Keep the recipe beginner-friendly.
The food name comes from an image classifier, so
mention any reasonable assumption if the identification is ambiguous.
"""
            }
        ],
        max_completion_tokens=1500
    )

    return response.choices[0].message.content




st.title("🍳 Snap2Recipe AI")
st.write("Turn a food photo into a delicious recipe.")
st.divider()

uploaded_image = st.file_uploader(
    "Upload a photo of your food",
    type=["jpg", "jpeg", "png"]
)

if uploaded_image:

    image=Image.open(uploaded_image).convert("RGB")
    st.image(
        image,
        caption="Your uploaded food image",
        use_container_width=True
    )

    if st.button("✨ Generate My Recipe", type="primary",use_container_width=True):
        try:
            with st.spinner("Identifying the food..."):
                model=load_model()
                classes=load_classes()
                predictions=predict_food(image,model,classes)

            st.subheader("Top 3 predictions")

            for item in predictions:
                food_name=item['food'].replace("_"," ").title()
                confidence=item['confidence']

                st.write(f"**{food_name}** - {confidence:.2%}")

                st.progress(min(max(confidence,0.0),1.0))

            predicted_food=predictions[0]['food']

            st.subheader(
                f"Recipe for {predicted_food.replace('_',' ').title()}"
            )

            with st.spinner("Generating your Recipe..."):
                recipe=generate_recipe(predicted_food)

            st.markdown(recipe)

            st.download_button(
                "Download Recipe",
                data=recipe,
                file_name="recipe.txt",
                mime="text/plain"
            )

        except Exception as error:
           st.error(f"Error: {error}")

                
