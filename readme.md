# 🍳 Snap2Recipe AI

**Turn food photos into recipes with AI.**

Snap2Recipe AI is a web application that combines deep learning and generative AI to identify food from images and generate recipe suggestions. It uses a CNN trained on the Food-101 dataset to predict food categories and the Groq API to generate recipes.

## ✨ Features

- 📸 Upload food images
- 🧠 Predict food categories using a trained CNN
- 🔍 Display the top 3 predictions with confidence scores
- 🥗 Generate recipes using an LLM API
- 📝 Get ingredients with quantities and step-by-step cooking instructions
- ⬇️ Download generated recipes
- 🖥️ Simple, interactive Streamlit interface

## 🛠️ Tech Stack

- Python
- TensorFlow / Keras
- Food-101 dataset
- NumPy
- Pillow
- Streamlit
- Groq API

## ⚙️ How It Works

1. Upload a food image.
2. The CNN processes the image and predicts the top 3 food categories.
3. The highest-ranked prediction is sent to the Groq API.
4. The LLM generates a recipe with ingredients, quantities, and cooking instructions.
5. View or download the generated recipe.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Snap2Recipe-AI.git
cd Snap2Recipe-AI
```

### 2. Install dependencies

```bash
pip install streamlit tensorflow numpy pillow groq python-dotenv
```

### 3. Configure your API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Get your API key from the [Groq Console](https://console.groq.com/).

**Never commit your `.env` file or expose your API key publicly.**

### 4. Add the required model files

Ensure the project contains the trained model and class names file:

- `food101_model_patched.keras`
- `class_names.json`

The trained model may need to be downloaded separately if it is not included in the repository.

### 5. Run the application

```bash
streamlit run app.py
```

## 📁 Project Structure

```text
Snap2Recipe-AI/
├── app.py
├── test.py
├── class_names.json
├── food101_model_patched.keras
├── .env
├── .gitignore
└── README.md
```

## 🧠 Model

The application uses a TensorFlow/Keras image classification model trained on the Food-101 dataset. It predicts food categories and returns the top three results with confidence scores.

## 🔮 Future Improvements

- Improve food classification accuracy
- Add dietary preferences and allergy-aware recipe suggestions
- Support multiple cuisines
- Improve recipe presentation and user experience
- Deploy the application online

## ⚠️ Disclaimer

Food predictions may be incorrect, and generated recipes are suggestions. The application does not verify ingredients or allergens directly from the image.

## 📄 License

Choose a license for your project before distributing it publicly.

---

**Built with Python, deep learning, and generative AI.**