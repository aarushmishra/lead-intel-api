"""
Tests for the Lead Intelligence API.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "lead-intel-api"}


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Lead Intelligence API is running" in response.json()["message"]


def test_enrich_lead_happy_path():
    """Test successful lead enrichment with college."""
    lead_data = {
        "college": "ADYPU",
        "city": "Ghaziabad",
        "state": "Uttar Pradesh",
        "course": "BBA",
        "language": "Hindi"
    }
    
    response = client.post("/enrich_lead", json=lead_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["college"] == "ADYPU"
    assert data["city"] == "Ghaziabad"
    assert data["state"] == "Uttar Pradesh"
    assert data["course"] == "BBA"
    assert data["language"] == "Hindi"
    assert "caller_name" in data
    assert "pitch_text" in data
    assert "tts_languages" in data
    assert isinstance(data["tts_languages"], list)
    assert "English" in data["tts_languages"]


def test_enrich_lead_city_only():
    """Test lead enrichment with city but no college."""
    lead_data = {
        "college": "",
        "city": "Ghaziabad",
        "state": "Uttar Pradesh",
        "course": "BBA",
        "language": "Hindi"
    }
    
    response = client.post("/enrich_lead", json=lead_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["college"] == ""
    assert data["city"] == "Ghaziabad"
    assert "caller_name" in data
    assert "pitch_text" in data
    assert "tts_languages" in data


def test_enrich_lead_nurture_fallback():
    """Test lead enrichment with no college and no city (nurture fallback)."""
    lead_data = {
        "college": "",
        "city": "",
        "state": "Uttar Pradesh",
        "course": "BBA",
        "language": "Hindi"
    }
    
    response = client.post("/enrich_lead", json=lead_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["college"] == ""
    assert data["city"] == ""
    assert "caller_name" in data
    assert "pitch_text" in data
    assert "tts_languages" in data


def test_enrich_lead_missing_state():
    """Test lead enrichment with missing required state field."""
    lead_data = {
        "college": "ADYPU",
        "city": "Ghaziabad",
        "course": "BBA",
        "language": "Hindi"
    }
    
    response = client.post("/enrich_lead", json=lead_data)
    assert response.status_code == 422


def test_enrich_lead_missing_course():
    """Test lead enrichment with missing required course field."""
    lead_data = {
        "college": "ADYPU",
        "city": "Ghaziabad",
        "state": "Uttar Pradesh",
        "language": "Hindi"
    }
    
    response = client.post("/enrich_lead", json=lead_data)
    assert response.status_code == 422


def test_enrich_lead_unknown_college():
    """Test lead enrichment with unknown college."""
    lead_data = {
        "college": "Unknown College",
        "city": "Ghaziabad",
        "state": "Uttar Pradesh",
        "course": "BBA",
        "language": "Hindi"
    }
    
    response = client.post("/enrich_lead", json=lead_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "caller_name" in data
    assert "pitch_text" in data
    assert "Unknown College" in data["pitch_text"]


def test_enrich_lead_language_fallback():
    """Test lead enrichment with unsupported language."""
    lead_data = {
        "college": "ADYPU",
        "city": "Ghaziabad",
        "state": "Uttar Pradesh",
        "course": "BBA",
        "language": "Marathi"  # This language is disabled in our stub data
    }
    
    response = client.post("/enrich_lead", json=lead_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "tts_languages" in data
    # Should fallback to Hindi (as per bot_language_support.json)
    assert "Hindi" in data["tts_languages"]
    assert "English" in data["tts_languages"]


def test_enrich_lead_state_language_derivation():
    """Test lead enrichment with language derived from state."""
    lead_data = {
        "college": "ADYPU",
        "city": "Ghaziabad",
        "state": "Uttar Pradesh",
        "course": "BBA",
        "language": ""  # Empty language should derive from state
    }
    
    response = client.post("/enrich_lead", json=lead_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "tts_languages" in data
    # Should use Hindi (primary language for Uttar Pradesh)
    assert "Hindi" in data["tts_languages"]
    assert "English" in data["tts_languages"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
