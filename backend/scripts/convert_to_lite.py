import tensorflow as tf
import os
import sys

def convert_model():
    # Define paths
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # backend/
    models_dir = os.path.join(base_path, "models")
    h5_path = os.path.join(models_dir, "leaf_quality_model.h5")
    tflite_path = os.path.join(models_dir, "leaf_quality_model.tflite")

    print(f"Checking for model at: {h5_path}")
    if not os.path.exists(h5_path):
        print(f"Error: Model not found at {h5_path}")
        # Create a dummy model for testing if real one doesn't exist (FOR DEBUGGING/PROTOTYPING ONLY)
        print("Creating dummy model for testing purposes...")
        model = tf.keras.Sequential([
            tf.keras.layers.InputLayer(input_shape=(224, 224, 3)),
            tf.keras.layers.Conv2D(16, 3, activation='relu'),
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(3, activation='softmax')
        ])
        model.save(h5_path)
    else:
        print("Loading existing model...")
        model = tf.keras.models.load_model(h5_path)

    print("Converting to TFLite...")
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    
    # Optimization (Quantization)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    
    tflite_model = converter.convert()

    # Save the model
    with open(tflite_path, "wb") as f:
        f.write(tflite_model)
    
    print(f"Success! Model saved to {tflite_path}")
    print(f"Model size: {os.path.getsize(tflite_path) / 1024:.2f} KB")

if __name__ == "__main__":
    convert_model()
