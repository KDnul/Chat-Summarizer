from flask import Flask, request, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    summary = ""
    if request.method == "POST":
        text = request.form["text"]
        # Call ai summary function here
        summary = summarize_text(text)
    return render_template("index.html", summary=summary)

def summarize_text(text):
    api_key= os.getenv("OPENROUTER_API_KEY")
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "QwenSummarizer"
    }

    prompt = f"Summarize the following text in 3-5 sentences:\n\n{text}"

    data = {
        "model": "qwen/qwen-2.5-72b-instruct:free",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
        "max_tokens": 300
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

if __name__ == "__main__":
    app.run(debug=True)