from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# 🔑 Paste your OpenRouter API key here directly
API_KEY = " API key"  # Replace with your real key

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    if request.method == "POST":
        notes = request.form["notes"]
        prompt = f"Summarize the following text in 5 bullet points:\n{notes}"

        # 🧠 Send to OpenRouter using mistral model
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/mistral-7b-instruct",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that summarizes notes."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.5,
                "max_tokens": 200
            }
        )

        result = response.json()
        try:
            summary = result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            summary = f"Error: {result}"

    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(debug=True)





