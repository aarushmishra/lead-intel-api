# Lead Intelligence API

A FastAPI microservice for enriching raw lead data with calling intelligence, language mapping, and campus-specific information.

## 🚀 Quick Start

### Local Development
```bash
cd lead-intel-api
source ../venv/bin/activate
uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
```

### Production Deployment

#### Option 1: Render (Recommended)
1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository: `aarushmishra/lead-intel-api`
4. Configure:
   - **Name**: `lead-intel-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Click "Create Web Service"

Your production URL will be: `https://lead-intel-api.onrender.com`

#### Option 2: Railway
Currently experiencing deployment issues. Use Render for now.

## 📡 API Endpoints

### Health Check
```bash
GET /health
```

### Enrich Lead
```bash
POST /enrich_lead
Content-Type: application/json

{
  "college": "IIT Delhi",
  "city": "Delhi", 
  "state": "Delhi",
  "course": "Computer Science",
  "language": "Hindi"
}
```

## 🧪 Testing

```bash
# Run tests
python -m pytest tests/ -v

# Test API locally
curl -X GET "http://localhost:8000/health"
curl -X POST "http://localhost:8000/enrich_lead" \
  -H "Content-Type: application/json" \
  -d '{"college": "IIT Delhi", "city": "Delhi", "state": "Delhi", "course": "Computer Science", "language": "Hindi"}'
```

## 📊 Features

- **Language Mapping**: State-based language preferences with fallbacks
- **Campus Intelligence**: Real campus data with proximity calculations
- **Brand Registry**: College-specific caller names and pitch details
- **TTS Support**: Multi-language text-to-speech language selection
- **Comprehensive Coverage**: 200+ colleges across India

## 🔧 Configuration

The API uses several data files in `app/dist/`:
- `state_language_map.json` - Language preferences by state
- `campus_coverage.json.gz` - College data with coordinates
- `brand_registry.json` - Caller names and brand categories
- `bot_language_support.json` - TTS language support
- `pitch_templates.json` - Pitch templates (future use)

## 📈 Performance

- **Response Time**: < 100ms average
- **Success Rate**: 100% (tested with 200 samples)
- **Coverage**: All major Indian states and colleges
- **Fallbacks**: Robust fallback mechanisms for edge cases

## 🚀 Production Status

- ✅ **Local Development**: Working perfectly
- ❌ **Railway**: Deployment issues (502 errors)
- 🔄 **Render**: Ready for deployment (recommended)

For production use, deploy on Render using the instructions above.
