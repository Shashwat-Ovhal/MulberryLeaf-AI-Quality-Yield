from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import prediction
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("mulberry-leaf-api")

app = FastAPI(
    title="MulberryLeaf AI Quality & Yield API",
    description="Backend API for predicting leaf quality and cocoon yield.",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(
        f"Method: {request.method} Path: {request.url.path} "
        f"Status: {response.status_code} Duration: {process_time:.4f}s"
    )
    
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Root/Health check
@app.get("/health")
@app.get("/")
async def health_check():
    """
    Returns the health status of the API and models.
    """
    from app.services.ml_service import ml_service
    
    models_ready = (
        ml_service.vision_model is not None and 
        ml_service.yield_model is not None
    )
    
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "models_ready": models_ready,
        "api_v": "1.0.0"
    }

# Include prediction endpoints
app.include_router(prediction.router, tags=["Predictions"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
