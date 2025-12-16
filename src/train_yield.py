import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from src.model_yield import YieldModel

def train_yield_model():
    DATA_PATH = "data/cocoon_yield.csv"
    MODEL_SAVE_PATH = "models/yield_model.pkl"
    
    if not os.path.exists(DATA_PATH):
        print(f"Error: {DATA_PATH} not found.")
        return
        
    df = pd.read_csv(DATA_PATH)
    
    # Feature columns: avg_quality_score, temperature, humidity
    X = df[['avg_quality_score', 'temperature', 'humidity']]
    y = df['cocoon_yield']
    
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Yield Model...")
    model = YieldModel()
    model.train(X_train, y_train)
    
    # Evaluate
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    print(f"Yield Model Evaluation:\n  MSE: {mse:.4f}\n  R2 : {r2:.4f}")
    
    # Save
    if not os.path.exists("models"):
        os.makedirs("models")
        
    model.save(MODEL_SAVE_PATH)
    print(f"Yield model saved to {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    train_yield_model()
