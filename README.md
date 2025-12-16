# Mulberry Leaf AI: Quality Assessment & Yield Prediction

## 📌 Project Overview
The **Mulberry Leaf AI** system is an intelligent application designed to modernize sericulture (silk production). It leverages Machine Learning and Computer Vision to:
1.  **Assess Mulberry Leaf Quality**: Classify leaves as *Excellent*, *Moderate*, or *Poor* using deep learning.
2.  **Predict Cocoon Yield**: Estimate silk cocoon yield based on environmental factors (Temperature, Humidity) and leaf quality data.

This project aims to help farmers maximize their yield by providing precise, data-driven recommendations.

## 🏗️ System Architecture
The system consists of three main components:

### 1. Vision Module (Leaf Quality)
*   **Algorithm**: **MobileNetV2** (Transfer Learning)
*   **Input**: Images of mulberry leaves.
*   **Output**: Quality Classification (3 Classes).
*   **Framework**: TensorFlow/Keras.
*   **Performance**: Optimized for speed and accuracy on standard hardware.

### 2. Yield Prediction Module
*   **Algorithm**: **Random Forest Regressor**.
*   **Input**: 
    *   Average Leaf Quality Score (derived from vision or manual input).
    *   Temperature (°C).
    *   Humidity (%).
*   **Output**: Expected Cocoon Yield (kg).
*   **Framework**: Scikit-Learn.

### 3. Application Interface
*   **Framework**: **Streamlit**.
*   **Features**:
    *   Real-time image upload & camera capture.
    *   Instant visual quality feedback.
    *   Interactive yield calculator.
    *   Professional, user-friendly UI.

---

## 🚀 Getting Started

### Prerequisites
*   OS: Windows (Recommended), Linux, or macOS.
*   **Python Version**: **3.10** (Strict requirement).

### Installation
1.  Clone the repository:
    ```bash
    git clone https://github.com/YourUsername/MulberryLeaf-AI-Quality-Yield.git
    cd MulberryLeaf-AI-Quality-Yield
    ```

2.  Create a Virtual Environment (Recommended):
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  Install Dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### 🧠 Model Training (Important)
**Note**: Trained model binary files (`*.h5`, `*.pkl`) are excluded from this repository to keep it clean and within size limits. You **must** retrain the models locally before running the app.

1.  **Train Vision Model**:
    ```bash
    python src/train_vision.py
    ```
    *   This generates `models/leaf_quality_model.h5`.

2.  **Train Yield Model**:
    ```bash
    python src/train_yield.py
    ```
    *   This generates `models/yield_model.pkl`.

### 🖥️ Running the Application
Once models are trained, launch the interface:
```bash
streamlit run app/app.py
```
The app will open in your browser at `http://localhost:8501`.

---

## 📁 Project Structure
```
MulberryLeaf-AI-Quality-Yield/
├── app/
│   └── app.py              # Main Application Entry Point
├── data/
│   ├── cocoon_yield.csv    # Yield training data
│   └── synthetic_leaves/   # Vision training images
├── src/
│   ├── model_vision.py     # CNN Architecture Definition
│   ├── model_yield.py      # Regression Model Definition
│   ├── train_vision.py     # Vision Training Script
│   └── train_yield.py      # Yield Training Script
├── requirements.txt        # Python Dependencies
└── README.md               # Project Documentation
```

## 📝 License
This project is for academic/research purposes.
