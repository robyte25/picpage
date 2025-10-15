import os
import base64
from io import BytesIO
from flask import Flask, request, render_template_string
from g4f.client import Client
from PIL import Image

app = Flask(__name__)

# =============================
# HTML Vorlage
# =============================
HTML_PAGE = """
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>🎨 KI Bildgenerator</title>
<style>
  body {
    background: linear-gradient(135deg, #000010, #001a33);
    color: #fff;
    font-family: Arial, sans-serif;
    text-align: center;
    padding: 2rem;
  }
  h1 { color: #26d07b; }
  form {
    margin: 1.5rem auto;
    max-width: 500px;
  }
  input[type=text] {
    width: 90%;
    padding: 0.8rem;
    border-radius: 8px;
    border: none;
    font-size: 1rem;
    margin-bottom: 1rem;
  }
  button {
    background: #26d07b;
    border: none;
    padding: 0.8rem 1.5rem;
    border-radius: 8px;
    font-size: 1rem;
    color: #000;
    cursor: pointer;
  }
  button:hover {
    background: #1aa868;
  }
  img {
    margin-top: 2rem;
    max-width: 90%;
    border-radius: 12px;
    box-shadow: 0 0 20px rgba(255,255,255,0.15);
  }
</style>
</head>
<body>
  <h1>🎨 KI Bildgenerator</h1>
  <p>Gib einen Prompt ein, und ich male dein Bild aus reiner Vorstellungskraft.</p>
  <form method="POST">
    <input type="text" name="prompt" placeholder="z. B. Ein Fuchs im Neonwald bei Nacht" required>
    <br>
    <button type="submit">Bild generieren</button>
  </form>
  {% if image_data %}
    <img src="data:image/png;base64,{{ image_data }}" alt="Generiertes Bild">
  {% elif error %}
    <p style="color:red;">⚠️ {{ error }}</p>
  {% endif %}
</body>
</html>
"""

# =============================
# Bildgenerierung
# =============================
def generiere_bild(prompt: str):
    client = Client()
    try:
        result = client.images.generate(
            model="flux",
            prompt=prompt,
            response_format="b64_json"
        )
        image_data = result.data[0].b64_json
        return image_data
    except Exception as e:
        raise RuntimeError(f"Fehler bei der Bildgenerierung: {e}")

# =============================
# Flask Routes
# =============================
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        prompt = request.form.get("prompt")
        try:
            image_data = generiere_bild(prompt)
            return render_template_string(HTML_PAGE, image_data=image_data)
        except Exception as e:
            return render_template_string(HTML_PAGE, error=str(e))
    return render_template_string(HTML_PAGE)

# =============================
# Start
# =============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
