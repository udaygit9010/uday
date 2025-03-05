from openai import OpenAI
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import random  # For generating a fake accuracy score
import os
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

# Initialize OpenAI client
client = OpenAI()

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
                news_links.append({"title": item["title"], "link": item["link"]})
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

        # Step 1: Ask ChatGPT for an analysis
        try:
            response = client.chat.completions.create( 
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Analyze this news and tell me if it's fake or real: {news_text}"}]
            )
            ai_result = response.choices[0].message.content  
        except Exception as e:
            return jsonify({"error": f"AI analysis failed: {str(e)}"}), 500  

        # Step 2: Generate a fake accuracy score (for demo purposes)
        accuracy = round(random.uniform(50, 99), 2)  # Fake accuracy between 50% and 99%

        # Step 3: Search Google News for verification
        news_results = search_google_news(news_text[:50])

        return jsonify({
            "AI_Analysis": ai_result,
            "Accuracy": f"{accuracy}%",
            "Trusted_News_Links": news_results if news_results else "No matching news found"
        })

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
