import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import random  # For generating a fake accuracy score
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
CORS(app)

# Function to search Google News
def search_google_news(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={SEARCH_ENGINE_ID}&key={GOOGLE_API_KEY}"
    response = requests.get(url)

    try:
        results = response.json()
        news_links = []
        if "items" in results:
            for item in results["items"]:
                # Extract the domain name (source)
                parsed_url = urlparse(item["link"])
                source = parsed_url.netloc.replace("www.", "")

                # Generate a fake accuracy score for demonstration
                accuracy = round(random.uniform(50, 99), 2)

                news_links.append({
                    "title": item["title"],
                    "link": item["link"],
                    "source": source,
                    "accuracy": f"{accuracy}%"
                })
        return news_links
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()  # Expect JSON input
        if not data or 'news_text' not in data:
            return jsonify({"error": "No news text provided"}), 400
        
        news_text = data['news_text']

        # Search Google News for verification
        news_results = search_google_news(news_text[:50])

        return jsonify({
            "News_Verification": news_results if news_results else "No matching news found"
        })

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

