import os
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# -------------------------------------------------------------------------
# 1. Synthetic Image Generator (Simulates Real Leaf Images)
# -------------------------------------------------------------------------
def generate_synthetic_images(output_dir="data/synthetic_leaves", num_samples=100):
    """
    Generates dummy leaf images and a labels.csv file.
    
    Args:
        output_dir: Directory where images will be saved.
        num_samples: Number of images to generate.
    """
    ensure_dir(output_dir)
    
    data = []
    classes = ["Excellent", "Moderate", "Poor"]
    
    print(f"Generating {num_samples} synthetic images in '{output_dir}'...")

    for i in range(num_samples):
        # Randomly assign a class
        label = np.random.choice(classes)
        filename = f"leaf_{i:04d}.jpg"
        filepath = os.path.join(output_dir, filename)
        
        # Create a simple image (224x224 RGB)
        # Background: White (per user requirement "white background")
        img_array = np.full((224, 224, 3), 255, dtype=np.uint8)
        img = Image.fromarray(img_array)
        draw = ImageDraw.Draw(img)
        
        # Draw a simple "leaf" (ellipse)
        # Color logic to differentiate classes slightly for "learning" (optional)
        if label == "Excellent":
            # Deep green, large
            color = (34, 139, 34) 
            bbox = [50, 20, 170, 200]
        elif label == "Moderate":
            # Lighter green/yellowish, medium
            color = (154, 205, 50)
            bbox = [60, 40, 160, 180]
        else: # Poor
            # Brownish/dry, small or irregular
            color = (139, 69, 19)
            bbox = [70, 60, 150, 160]

        # Add some random noise/variation to bbox
        jitter = np.random.randint(-10, 10, size=4)
        final_bbox = [b + j for b, j in zip(bbox, jitter)]
        
        draw.ellipse(final_bbox, fill=color, outline=None)
        
        img.save(filepath)
        data.append({"filename": filename, "quality": label})
    
    csv_path = os.path.join(output_dir, "labels.csv")
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
    print(f"Saved image labels to '{csv_path}'.")

# -------------------------------------------------------------------------
# 2. Synthetic Yield Data Generator (Simulates Batch Yield Data)
# -------------------------------------------------------------------------
def generate_yield_data(output_path="data/cocoon_yield.csv", num_batches=50):
    """
    Generates synthetic yield data.
    Input features: Leaf Quality (Encoded), Temperature, Humidity
    Output: Yield (grams)
    """
    ensure_dir(os.path.dirname(output_path))
    
    print(f"Generating {num_batches} synthetic yield records...")
    
    # 0=Poor, 1=Moderate, 2=Excellent (Just for simulation logic math)
    # In real pipeline, the regression model will take numerical probs or encoded labels
    
    records = []
    
    for _ in range(num_batches):
        # Simulate environmental conditions
        temp = np.random.uniform(20.0, 35.0) # Celsius
        humidity = np.random.uniform(50.0, 90.0) # %
        
        # Simulate 'Average Batch Quality' (0.0 to 2.0 scale for calculation)
        avg_quality_score = np.random.uniform(0.0, 2.0) 
        
        # Simulate Yield Formula (just for correlation):
        # Base yield 50g
        # + 20g * average quality (better leaves = more silk)
        # - penalty for extreme temp (ideal is ~25)
        # - penalty for extreme humidity (ideal is ~70)
        
        yield_val = 50 + (25 * avg_quality_score) 
        yield_val -= abs(temp - 25.0) * 1.5
        yield_val -= abs(humidity - 70.0) * 0.5
        
        # Add noise
        yield_val += np.random.normal(0, 2.0)
        yield_val = max(10.0, yield_val) # Min yield
        
        # For the dataset, we might want discrete categorical inputs if the user 
        # enters "Excellent" in the app, but typically regression wants numbers.
        # Let's start with a scenario where the regression model takes 
        # (Avg_Quality_Score, Temp, Humidity). 
        # We can also store the 'dominant class' for reference.
        
        records.append({
            "avg_quality_score": round(avg_quality_score, 2), # 0-2 scale (derived from Classification)
            "temperature": round(temp, 1),
            "humidity": round(humidity, 1),
            "cocoon_yield": round(yield_val, 2)
        })
        
    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)
    print(f"Saved yield data to '{output_path}'.")

if __name__ == "__main__":
    generate_synthetic_images()
    generate_yield_data()
