from app.services.ml_service import ml_service
from app.services.cache_service import cache_service
from app.utils.image_utils import get_image_hash
import time

router = APIRouter()

class YieldPredictionRequest(BaseModel):
    avg_quality: float
    temperature: float
    humidity: float

@router.post("/predict/leaf-quality")
async def predict_leaf_quality(file: UploadFile = File(...)):
    """
    Endpoint to predict leaf quality from an uploaded image.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")
    
    start_time = time.time()
    image_bytes = await file.read()
    image_hash = get_image_hash(image_bytes)
    
    # Check cache first
    cached_result = cache_service.get(image_hash)
    if cached_result:
        prediction_time = time.time() - start_time
        return {
            **cached_result,
            "prediction_time": round(prediction_time, 4),
            "cached": True
        }
    
    try:
        class_name, confidence = ml_service.predict_leaf_quality(image_bytes)
        prediction_time = time.time() - start_time
        
        result = {
            "prediction_type": "leaf_quality",
            "class_name": class_name,
            "confidence": round(confidence, 4),
            "image_hash": image_hash
        }
        
        # Save to cache
        cache_service.set(image_hash, result)
        
        return {
            **result,
            "prediction_time": round(prediction_time, 4),
            "cached": False
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict/yield")
async def predict_yield(request: YieldPredictionRequest):
    """
    Endpoint to predict cocoon yield based on parameters.
    """
    start_time = time.time()
    try:
        yield_prediction = ml_service.predict_yield(
            request.avg_quality, 
            request.temperature, 
            request.humidity
        )
        prediction_time = time.time() - start_time
        
        return {
            "prediction_type": "cocoon_yield",
            "estimated_yield": round(yield_prediction, 4),
            "prediction_time": round(prediction_time, 4)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
