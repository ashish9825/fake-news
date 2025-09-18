from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import VotingClassifier
import pandas as pd
import requests
import uvicorn
from gnews import GNews
import re
import string
import time
import psutil
from datetime import datetime

app = FastAPI()

# Initialize GNews
google_news = GNews(language='en', country='US', period='1d', max_results=15)

# Metrics storage
metrics = {
    'total_predictions': 0,
    'fake_predictions': 0,
    'real_predictions': 0,
    'api_calls': 0,
    'start_time': time.time()
}

# Text preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# Enhanced training data with more examples
train_data = {
    'text': [
        'The government has announced a new policy for economic growth',
        'Breaking: Aliens landed in New York City yesterday evening',
        'COVID-19 vaccine shows 95% effectiveness in clinical trials',
        'Scientists discovered magical cure for aging using unicorn tears',
        'Election results officially announced by electoral commission',
        'Chocolate found to cure cancer in groundbreaking study',
        'President signs new healthcare bill into law',
        'Local man grows 50-foot tall vegetables using alien technology',
        'Stock market reaches new record high amid economic recovery',
        'Doctors hate this one weird trick that cures everything',
        'University researchers publish peer-reviewed climate study',
        'Celebrity claims to have met time travelers from 2050',
        'New smartphone technology improves battery life significantly',
        'Woman loses 100 pounds eating only ice cream for breakfast',
        'Tech company announces breakthrough in renewable energy',
        'Scientists confirm that water is actually dangerous to humans'
    ],
    'label': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]  # 0: Real, 1: Fake
}

df = pd.DataFrame(train_data)
df['text'] = df['text'].apply(preprocess_text)

# Create ensemble model for better accuracy
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2))
X = vectorizer.fit_transform(df['text'])
y = df['label']

# Ensemble of classifiers
lr_clf = LogisticRegression(random_state=42)
rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
nb_clf = MultinomialNB()

ensemble_model = VotingClassifier(
    estimators=[('lr', lr_clf), ('rf', rf_clf), ('nb', nb_clf)],
    voting='soft'
)
ensemble_model.fit(X, y)

@app.get('/', response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Fake News Detector</title>
        <style>
            body { font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 20px; }
            .container { max-width: 800px; margin: 50px auto; background: #fff; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
            h2 { color: #333; text-align: center; margin-bottom: 30px; }
            input[type=text] { width: 100%; padding: 15px; margin: 10px 0; border: 2px solid #ddd; border-radius: 8px; font-size: 16px; }
            button { padding: 15px 25px; background: #007bff; color: #fff; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; margin: 10px 5px; }
            button:hover { background: #0056b3; }
            .news-item { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #007bff; }
            .fake { border-left-color: #dc3545; }
            .real { border-left-color: #28a745; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🔍 AI-Powered Fake News Detector</h2>
            <form method="post" action="/predict">
                <input type="text" name="text" placeholder="Enter news headline or article text to analyze..." required />
                <button type="submit">🔎 Analyze News</button>
            </form>
            <form method="get" action="/realtime-news">
                <button type="submit">📰 Get Latest News & Analysis</button>
            </form>
            <form method="get" action="/test-model">
                <button type="submit">🧪 Test Model</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.get('/test-model', response_class=HTMLResponse)
def test_model():
    """Test endpoint to verify model is working"""
    test_texts = [
        "Scientists discover cure for all diseases using magic potion",
        "Government announces new economic policy for growth",
        "Celebrity claims to have superpowers from alien DNA"
    ]
    
    html = """
    <html>
    <head>
        <style>
            body { font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 20px; }
            .container { max-width: 800px; margin: 50px auto; background: #fff; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
            .test-item { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #007bff; }
            .fake { border-left-color: #dc3545; background: #ffe6e6; }
            .real { border-left-color: #28a745; background: #e6ffe6; }
            a { display: inline-block; padding: 15px 25px; background: #007bff; color: white; text-decoration: none; border-radius: 8px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class='container'>
            <h2>🧪 Model Test Results</h2>
    """
    
    for text in test_texts:
        processed_text = preprocess_text(text)
        vect_text = vectorizer.transform([processed_text])
        pred = ensemble_model.predict(vect_text)[0]
        confidence = max(ensemble_model.predict_proba(vect_text)[0])
        result = 'Fake' if pred == 1 else 'Real'
        
        html += f"""
            <div class='test-item {"fake" if pred == 1 else "real"}'>
                <p><strong>Text:</strong> "{text}"</p>
                <p><strong>Prediction:</strong> {result} (Confidence: {confidence:.1%})</p>
            </div>
        """
    
    html += """
            <a href='/'>🔙 Back to Home</a>
        </div>
    </body>
    </html>
    """
    return html

@app.get('/metrics', response_class=PlainTextResponse)
def get_metrics():
    """Prometheus metrics endpoint"""
    uptime = time.time() - metrics['start_time']
    
    try:
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
    except:
        cpu_percent = 0
        memory_percent = 0
    
    prometheus_metrics = f"""# HELP fake_news_predictions_total Total number of predictions made
# TYPE fake_news_predictions_total counter
fake_news_predictions_total {metrics['total_predictions']}

# HELP fake_news_fake_predictions_total Total number of fake news predictions
# TYPE fake_news_fake_predictions_total counter
fake_news_fake_predictions_total {metrics['fake_predictions']}

# HELP fake_news_real_predictions_total Total number of real news predictions
# TYPE fake_news_real_predictions_total counter
fake_news_real_predictions_total {metrics['real_predictions']}

# HELP fake_news_api_calls_total Total number of API calls
# TYPE fake_news_api_calls_total counter
fake_news_api_calls_total {metrics['api_calls']}

# HELP fake_news_uptime_seconds Application uptime in seconds
# TYPE fake_news_uptime_seconds gauge
fake_news_uptime_seconds {uptime}

# HELP system_cpu_usage_percent CPU usage percentage
# TYPE system_cpu_usage_percent gauge
system_cpu_usage_percent {cpu_percent}

# HELP system_memory_usage_percent Memory usage percentage
# TYPE system_memory_usage_percent gauge
system_memory_usage_percent {memory_percent}
"""
    return prometheus_metrics

@app.get('/health')
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "uptime": time.time() - metrics['start_time']
    }

@app.post('/predict', response_class=HTMLResponse)
def predict_news(text: str = Form(...)):
    # Update metrics
    metrics['total_predictions'] += 1
    metrics['api_calls'] += 1
    
    processed_text = preprocess_text(text)
    vect_text = vectorizer.transform([processed_text])
    pred = ensemble_model.predict(vect_text)[0]
    confidence = max(ensemble_model.predict_proba(vect_text)[0])
    result = 'Fake' if pred == 1 else 'Real'
    
    # Update prediction metrics
    if pred == 1:
        metrics['fake_predictions'] += 1
    else:
        metrics['real_predictions'] += 1
    
    color = 'red' if pred == 1 else 'green'
    
    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 20px; }}
            .container {{ max-width: 800px; margin: 50px auto; background: #fff; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }}
            .result {{ text-align: center; padding: 20px; border-radius: 8px; margin: 20px 0; }}
            .fake {{ background: #ffe6e6; border: 2px solid #ff4444; color: #cc0000; }}
            .real {{ background: #e6ffe6; border: 2px solid #44ff44; color: #008800; }}
            a {{ display: inline-block; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class='container'>
            <h2>Analysis Result</h2>
            <div class='result {"fake" if pred == 1 else "real"}'>
                <h3>This news appears to be: {result}</h3>
                <p>Confidence: {confidence:.2%}</p>
                <p><strong>Original Text:</strong> "{text}"</p>
            </div>
            <a href='/'>🔙 Analyze Another News</a>
        </div>
    </body>
    </html>
    """

@app.get('/realtime-news', response_class=HTMLResponse)
def realtime_news():
    # Update metrics
    metrics['api_calls'] += 1
    
    try:
        # Get latest news from GNews
        news_results = google_news.get_news('latest news')
        
        html = """
        <html>
        <head>
            <style>
                body { font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 20px; }
                .container { max-width: 1000px; margin: 50px auto; background: #fff; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
                .news-item { background: #f8f9fa; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 6px solid #007bff; }
                .fake { border-left-color: #dc3545; background: #ffe6e6; }
                .real { border-left-color: #28a745; background: #e6ffe6; }
                .title { font-weight: bold; font-size: 18px; margin-bottom: 10px; }
                .prediction { font-weight: bold; font-size: 16px; padding: 8px 15px; border-radius: 20px; display: inline-block; }
                .fake-pred { background: #dc3545; color: white; }
                .real-pred { background: #28a745; color: white; }
                a { display: inline-block; padding: 15px 25px; background: #007bff; color: white; text-decoration: none; border-radius: 8px; margin-top: 20px; }
                .published { color: #666; font-size: 14px; margin: 5px 0; }
            </style>
        </head>
        <body>
            <div class='container'>
                <h2>📰 Latest News Analysis</h2>
        """
        
        if not news_results:
            html += "<p>No news articles found. Please try again later.</p>"
        else:
            for i, article in enumerate(news_results[:10]):  # Limit to 10 articles
                title = article.get('title', 'No Title Available')
                publisher = article.get('publisher', {}).get('title', 'Unknown Source')
                published_date = article.get('published date', 'Unknown Date')
                url = article.get('url', '#')
                
                # Analyze the news title
                processed_title = preprocess_text(title)
                vect_text = vectorizer.transform([processed_title])
                pred = ensemble_model.predict(vect_text)[0]
                confidence = max(ensemble_model.predict_proba(vect_text)[0])
                result = 'Fake' if pred == 1 else 'Real'
                
                html += f"""
                    <div class='news-item {"fake" if pred == 1 else "real"}'>
                        <div class='title'>{title}</div>
                        <p><strong>Source:</strong> {publisher}</p>
                        <p class='published'><strong>Published:</strong> {published_date}</p>
                        <p><a href='{url}' target='_blank'>Read Full Article</a></p>
                        <span class='prediction {"fake-pred" if pred == 1 else "real-pred"}'>
                            {result} News (Confidence: {confidence:.1%})
                        </span>
                    </div>
                """
        
        html += """
                <a href='/'>🔙 Back to Home</a>
            </div>
        </body>
        </html>
        """
        return html
        
    except Exception as e:
        return f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 20px; }}
                .container {{ max-width: 800px; margin: 50px auto; background: #fff; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }}
                a {{ display: inline-block; padding: 15px 25px; background: #007bff; color: white; text-decoration: none; border-radius: 8px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class='container'>
                <h2>Error fetching news</h2>
                <p>Unable to fetch latest news. Error: {str(e)}</p>
                <p>This might be due to network issues or API limitations. Please try again later.</p>
                <a href='/'>🔙 Back to Home</a>
            </div>
        </body>
        </html>
        """

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
