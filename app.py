import requests
from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
import os
import random  # For generating a fake accuracy score
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

app = Flask(__name__)
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

# Route to serve static files
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
