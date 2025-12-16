
import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
from PIL import Image
import joblib
import os
import sys

# Add project root to path for src imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.model_yield import YieldModel

# Page Configuration
st.set_page_config(
    page_title="Mulberry AI | Quality & Yield",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional UI
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #2e7d32;
        color: white;
        border-radius: 8px;
        height: 48px;
        font-weight: 600;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
    }
    .card {
        background-color: white;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 24px;
    }
    h1, h2, h3 {
        color: #1a1a1a;
        font-family: 'Inter', sans-serif;
    }
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #2e7d32;
    }
    .metric-label {
        font-size: 14px;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    /* Hide Streamlit components */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Model Loading ---
@st.cache_resource
def load_models():
    # Load Yield Model
    try:
        # Load the wrapper class instance if pickled, or re-instantiate and load weights?
        # Based on src/train_yield.py: model.save() uses joblib.dump(self, path)
        yield_model = YieldModel.load("models/yield_model.pkl")
    except Exception as e:
        st.error(f"Failed to load Yield Model: {e}")
        yield_model = None

    # Load Vision Model
    try:
        vision_model = tf.keras.models.load_model("models/leaf_quality_model.h5")
    except Exception as e:
        st.error(f"Failed to load Vision Model: {e}")
        vision_model = None
        
    return yield_model, vision_model

yield_model, vision_model = load_models()

# --- Preprocessing Helper ---
def preprocess_image(image):
    # Resize to 224x224
    img = image.resize((224, 224))
    # Convert to array
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    # Expand dims to (1, 224, 224, 3)
    img_array = np.expand_dims(img_array, axis=0)
    # Preprocess (MobileNetV2: scales to [-1, 1])
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    return img_array

# --- UI Layout ---

st.title("🍃 Mulberry Leaf AI")
st.markdown("### Intelligent Quality Assessment & Yield Prediction System")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📸 Leaf Quality Analysis")
    
    tab1, tab2 = st.tabs(["Upload Image", "Camera Capture"])
    
    img_input = None
    with tab1:
        uploaded_file = st.file_uploader("Choose a leaf image", type=['jpg', 'jpeg', 'png'])
        if uploaded_file is not None:
            img_input = Image.open(uploaded_file)
            
    with tab2:
        camera_file = st.camera_input("Take a picture")
        if camera_file is not None:
            img_input = Image.open(camera_file)
    
    if img_input is not None:
        st.image(img_input, caption="Input Image", use_column_width=True)
        
        if vision_model:
            with st.spinner("Analyzing leaf structure..."):
                processed_img = preprocess_image(img_input)
                predictions = vision_model.predict(processed_img)
                
                # Class mapping: {'Excellent': 0, 'Moderate': 1, 'Poor': 2}
                classes = ['Excellent', 'Moderate', 'Poor']
                class_idx = np.argmax(predictions[0])
                confidence = np.max(predictions[0])
                result_class = classes[class_idx]
                
                # Designator color
                color_map = {
                    'Excellent': '#2e7d32', # Green
                    'Moderate': '#f57f17', # Orange
                    'Poor': '#c62828'      # Red
                }
                res_color = color_map.get(result_class, '#333')
                
                st.markdown(f"""
                <div style="background-color: {res_color}15; border-left: 4px solid {res_color}; padding: 16px; border-radius: 4px; margin-top: 16px;">
                    <h3 style="color: {res_color}; margin: 0;">{result_class}</h3>
                    <p style="margin: 4px 0 0 0; color: #666;">Confidence: {confidence:.2%}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Store quality score for yield prediction (Excellent=1.0, Moderate=0.5, Poor=0.0 roughly, or custom scale)
                # Let's use a mapping for the yield input
                quality_score_map = {'Excellent': 9.0, 'Moderate': 6.0, 'Poor': 3.0} # Approximate mapping to scale 1-10
                st.session_state['detected_quality'] = quality_score_map[result_class]
        else:
            st.warning("Vision model not loaded.")
            
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("⚖️ Cocoon Yield Prediction")
    
    # Defaults
    default_quality = st.session_state.get('detected_quality', 7.5)
    
    with st.form("yield_form"):
        st.markdown("#### Environmental Parameters")
        
        temp = st.slider("Temperature (°C)", min_value=15.0, max_value=40.0, value=25.0, step=0.1)
        humidity = st.slider("Humidity (%)", min_value=30.0, max_value=100.0, value=70.0, step=0.1)
        
        st.markdown("#### Quality Metrics")
        quality_score = st.number_input("Avg Quality Score (1-10)", 
                                      min_value=1.0, max_value=10.0, 
                                      value=float(default_quality),
                                      step=0.1,
                                      help="Auto-filled if image analysis is run")
        
        submitted = st.form_submit_button("Predict Yield")
        
        if submitted:
            if yield_model:
                # Feature order: ['avg_quality_score', 'temperature', 'humidity']
                # Create DataFrame to match training input
                input_data = pd.DataFrame({
                    'avg_quality_score': [quality_score],
                    'temperature': [temp],
                    'humidity': [humidity]
                })
                
                prediction = yield_model.predict(input_data)[0]
                
                st.markdown("---")
                st.markdown('<p class="metric-label">Estimated Cocoon Yield</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="metric-value">{prediction:.2f} kg</p>', unsafe_allow_html=True)
                
                # Contextual info
                st.info(f"Based on Quality: {quality_score}, Temp: {temp}°C, Humidity: {humidity}%")
            else:
                st.error("Yield model not loaded.")
                
    st.markdown('</div>', unsafe_allow_html=True)
