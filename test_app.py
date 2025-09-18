import pytest
import sys
import os

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fake_news_api import app, preprocess_text
from fastapi.testclient import TestClient

client = TestClient(app)

def test_home_page():
    """Test the home page loads correctly"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Fake News Detector" in response.text

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "uptime" in data

def test_metrics_endpoint():
    """Test the metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "fake_news_predictions_total" in response.text
    assert "fake_news_uptime_seconds" in response.text

def test_preprocess_text():
    """Test text preprocessing function"""
    text = "This is a TEST! With 123 numbers and punctuation..."
    processed = preprocess_text(text)
    expected = "this is a test with  numbers and punctuation"
    assert processed == expected

def test_predict_endpoint():
    """Test the prediction endpoint"""
    response = client.post("/predict", data={"text": "Government announces new policy"})
    assert response.status_code == 200
    assert "Analysis Result" in response.text

def test_test_model_endpoint():
    """Test the model testing endpoint"""
    response = client.get("/test-model")
    assert response.status_code == 200
    assert "Model Test Results" in response.text

if __name__ == "__main__":
    pytest.main([__file__])
