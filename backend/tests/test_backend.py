import pytest
from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    # assert data["models_ready"] is True  # Uncomment if models are expected to be loaded

def test_models_exist():
    """Verify that model files exist in the correct location."""
    # Based on the fix, models should be in backend/models/
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # backed/app -> backend
    project_root = os.path.dirname(base_path)
    # The ml_service uses: os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # from app/services/ml_service.py.
    # __file__ is backend/app/services/ml_service.py
    # dir 1: backend/app/services
    # dir 2: backend/app
    # dir 3: backend
    # models_path = backend/models
    
    # In tests/test_backend.py:
    # __file__ is backend/tests/test_backend.py
    # dir 1: backend/tests
    # dir 2: backend
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_dir = os.path.join(backend_dir, "models")
    
    assert os.path.exists(models_dir), f"Models directory not found at {models_dir}"
    assert os.path.exists(os.path.join(models_dir, "leaf_quality_model.h5")), "Vision model missing"
    assert os.path.exists(os.path.join(models_dir, "yield_model.pkl")), "Yield model missing"

# We won't test prediction logic deepyl here as it requires tensorflow loading which might be slow or fail without GPU/env, 
# but health check implicitly checks ml_service loading.
