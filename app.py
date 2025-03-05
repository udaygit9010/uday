import requests
from flask import Flask, request, jsonify
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
        data = request.get_json()
        if not data or "news_text" not in data:
            return jsonify({"error": "No news text provided"}), 400

        news_text = data["news_text"]
        
        # Fake AI Analysis (Replace with your AI model)
        ai_result = "This news appears to be real."
        news_results = [
            {"title": "NASA Confirms Water on Mars", "link": "https://www.bbc.com/news", "accuracy": "92%", "source": "BBC News"}
        ]

        return jsonify({
            "AI_Analysis": ai_result,
            "Trusted_News_Links": news_results
        })
    
    except Exception as e:
        print("Server Error:", str(e))  # Print error in logs
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# Route to serve static files
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
