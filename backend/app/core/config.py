from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "MulberryLeaf AI API"
    DEBUG: bool = False
    PORT: int = 8000
    
    # Supabase Settings (Optional for initialization, required for integration)
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    SUPABASE_BUCKET: str = "mulberry-leaf-images"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
