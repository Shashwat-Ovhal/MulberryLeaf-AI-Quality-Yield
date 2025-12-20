# MulberryLeaf AI Quality & Yield Backend

Production-ready FastAPI backend for leaf quality classification and cocoon yield prediction.

## 🚀 Quick Start (Local)

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the API:**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Access API Docs:**
   Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.

## 🐳 Docker Setup

Build and run the container:
```bash
docker build -t mulberry-backend .
docker run -p 8000:8000 mulberry-backend
```

## ☁️ Deployment (Render/Railway/Fly.io)

This backend is ready for deployment. 
- **Root Directory:** `backend`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port 8000`

### Environment Variables
Set these in your deployment platform:
- `SUPABASE_URL`: Your Supabase Project URL
- `SUPABASE_KEY`: Your Supabase Service Role Key

## 🛠 Supabase Integration

1. Run the SQL in `supabase_schema.sql` in your Supabase SQL Editor.
2. Create a bucket named `mulberry-leaf-images` in Supabase Storage.

## 📱 Mobile API Endpoints

- `GET /health`: Health check and model readiness.
- `POST /predict/leaf-quality`: Upload image (`multipart/form-data`) to get classification.
- `POST /predict/yield`: Send JSON with `avg_quality`, `temperature`, and `humidity`.
