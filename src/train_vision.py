import os
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from src.model_vision import LeafQualityModel

def train_model():
    try:
        # settings
        DATA_DIR = "data/synthetic_leaves"
        CSV_PATH = os.path.join(DATA_DIR, "labels.csv")
        MODEL_SAVE_PATH = "models/leaf_quality_model.h5"
        BATCH_SIZE = 4 # Reduced batch
        EPOCHS = 1 # Reduced epochs for testing
        
        if not os.path.exists(CSV_PATH):
            print(f"Error: Data not found at {CSV_PATH}. Run src/data_generator.py first.")
            return
    
        # Load labels
        df = pd.read_csv(CSV_PATH)
        
        # Stratified split
        train_df, val_df = train_test_split(df, test_size=0.2, stratify=df['quality'], random_state=42)
        
        # Data Generators
        datagen = ImageDataGenerator(
            preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input,
            rotation_range=20,
            horizontal_flip=True
        )
        
        print("Preparing Data Generators...")
        train_generator = datagen.flow_from_dataframe(
            dataframe=train_df,
            directory=DATA_DIR,
            x_col="filename",
            y_col="quality",
            target_size=(224, 224),
            batch_size=BATCH_SIZE,
            class_mode="categorical",
            shuffle=True
        )
        
        val_generator = datagen.flow_from_dataframe(
            dataframe=val_df,
            directory=DATA_DIR,
            x_col="filename",
            y_col="quality",
            target_size=(224, 224),
            batch_size=BATCH_SIZE,
            class_mode="categorical",
            shuffle=False
        )
        
        # Initialize Model
        class_indices = train_generator.class_indices
        print(f"Class mapping: {class_indices}")
        
        lq_model = LeafQualityModel(num_classes=len(class_indices))
        lq_model.compile()
        
        # Train
        print("Starting training...")
        lq_model.model.fit(
            train_generator,
            validation_data=val_generator,
            epochs=EPOCHS
        )
        
        # Save
        if not os.path.exists("models"):
            os.makedirs("models")
            
        lq_model.save(MODEL_SAVE_PATH)
        print(f"Model saved to {MODEL_SAVE_PATH}")

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    train_model()
