import os
import tensorflow as tf
import joblib
import numpy as np
from PIL import Image
import io

class MLService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.models_path = os.path.join(self.base_path, "backend", "models")
        
        self.vision_model_path = os.path.join(self.models_path, "leaf_quality_model.h5")
        self.yield_model_path = os.path.join(self.models_path, "yield_model.pkl")
        
        self.vision_model = None
        self.yield_model = None
        self.load_models()
        
        self._initialized = True

    def load_models(self):
        """Load models once at startup."""
        print(f"Loading vision model from {self.vision_model_path}...")
        if os.path.exists(self.vision_model_path):
            self.vision_model = tf.keras.models.load_model(self.vision_model_path)
            print("Vision model loaded successfully.")
        else:
            print(f"Error: Vision model not found at {self.vision_model_path}")

        print(f"Loading yield model from {self.yield_model_path}...")
        if os.path.exists(self.yield_model_path):
            self.yield_model = joblib.load(self.yield_model_path)
            print("Yield model loaded successfully.")
        else:
            print(f"Error: Yield model not found at {self.yield_model_path}")

    def predict_leaf_quality(self, image_bytes):
        """
        Predicts leaf quality from image bytes.
        Returns: (class_name, confidence)
        """
        if self.vision_model is None:
            raise Exception("Vision model not loaded.")
            
        # Preprocessing
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0  # Simple normalization, similar to MobileNetV2
        img_array = np.expand_dims(img_array, axis=0)
        
        # Inference
        predictions = self.vision_model.predict(img_array)
        class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][class_idx])
        
        # Map to class names (Assuming 3 classes based on original src/model_vision.py)
        # Placeholder mapping - might need refinement based on training labels
        classes = ["Healthy", "Infected", "Nutrient Deficient"] 
        return classes[class_idx], confidence

    def predict_yield(self, avg_quality, temperature, humidity):
        """
        Predicts cocoon yield based on parameters.
        Args: [Avg_Quality_Score, Temperature, Humidity]
        """
        if self.yield_model is None:
            raise Exception("Yield model not loaded.")
            
        features = np.array([[avg_quality, temperature, humidity]])
        prediction = self.yield_model.predict(features)
        return float(prediction[0])

# Global instance
ml_service = MLService()
