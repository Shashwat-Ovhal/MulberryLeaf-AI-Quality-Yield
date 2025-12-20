-- SQL Schema for MulberryLeaf Prediction History

-- Drop tables if they exist (Be careful in production)
-- DROP TABLE IF EXISTS leaf_quality_predictions;
-- DROP TABLE IF EXISTS yield_predictions;

-- Table for Leaf Quality Predictions
CREATE TABLE IF NOT EXISTS leaf_quality_predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ DEFAULT now(),
    image_hash TEXT NOT NULL,
    image_url TEXT, -- URL to Supabase Storage
    class_name TEXT NOT NULL,
    confidence FLOAT NOT NULL,
    prediction_time FLOAT,
    user_id UUID -- References auth.users(id) if using Supabase Auth
);

-- Table for Yield Predictions
CREATE TABLE IF NOT EXISTS yield_predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ DEFAULT now(),
    avg_quality FLOAT NOT NULL,
    temperature FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    estimated_yield FLOAT NOT NULL,
    prediction_time FLOAT,
    user_id UUID -- References auth.users(id) if using Supabase Auth
);

-- Index for hashing to quickly find repeated images
CREATE INDEX IF NOT EXISTS idx_image_hash ON leaf_quality_predictions(image_hash);
