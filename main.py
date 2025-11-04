import os
import base64
from io import BytesIO
from flask import Flask, request, render_template_string, send_file

from g4f.client import Client
from PIL import Image

app = Flask(__name__)

# =============================
# HTML Template
# =============================
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta name="monetag" content="0247d398eb0826192314b034aa3033e7">
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Free AI Image Generator – Create Stunning Art from Text</title>
  <meta name="description" content="Free AI image generator – Create stunning artwork from text prompts using open models.">
  <meta name="keywords" content="AI image generator, free AI art, picpage, text to image, flux model, generate images, online art tool">
  <meta name="author" content="Free AI Art Generator">
  <meta property="og:title" content="Free AI Image Generator">
  <meta property="og:description" content="Create stunning AI-generated images from text prompts – completely free.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://picpage.onrender.com/">
  <meta property="og:image" content="https://picpage.onrender.com/static/preview.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Free AI Image Generator">
  <meta name="twitter:description" content="Create stunning AI-generated images from text prompts – completely free.">
  <meta name="twitter:image" content="https://picpage.onrender.com/static/preview.png">
  <link rel="canonical" href="https://picpage.onrender.com/">
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "Free AI Art Generator",
    "url": "https://picpage.onrender.com",
    "description": "Create stunning AI-generated images from text prompts using open models – completely free.",
    "creator": {
      "@type": "Organization",
      "name": "Free AI Art Generator"
    }
  }
  </script>
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1636994236720420"
     crossorigin="anonymous"></script>
  <style>
    body {
      background: linear-gradient(135deg, #000010, #001a33);
      color: #fff;
      font-family: Arial, sans-serif;
      text-align: center;
      padding: 2rem;
    }
    h1 { color: #26d07b; }
    form { margin: 1.5rem auto; max-width: 500px; }
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
      margin: 0.5rem;
    }
    button:hover { background: #1aa868; }
    img {
      margin-top: 2rem;
      max-width: 90%;
      border-radius: 12px;
      box-shadow: 0 0 20px rgba(255,255,255,0.15);
    }
    footer {
      margin-top: 3rem;
      font-size: 0.9rem;
      color: #ccc;
    }
  </style>
</head>
<body>
  <h1>🎨 AI Image Generator</h1>
  <p>Enter a prompt, and I’ll paint your vision straight from imagination.</p>
  <p><strong>This service is completely free — supported by ads.</strong></p>
  <form method="POST">
    <input type="text" name="prompt" placeholder="e.g. A fox in a neon forest at night" required>
    <br>
    <button type="submit">Generate Image</button>
  </form>
  {% if image_data %}
    <img src="data:image/png;base64,{{ image_data }}" alt="Generated Image">
    <form method="POST" action="/download">
      <input type="hidden" name="image_data" value="{{ image_data }}">
      <button type="submit">⬇️ Download Image</button>
    </form>
  {% elif error %}
    <p style="color:red;">⚠️ {{ error }}</p>
  {% endif %}
  <h2>If something goes wrong, please get in touch with me at rvkdrive@gmail.com</h2>
  <h3>Feel free to share any feedback — I’d love to hear it!</h3>
  <footer>
    <p>© 2025 Free AI Art Generator — Powered by Open Models & Ad Revenue</p>
  </footer>
</body>
</html>
"""

# =============================
# Image Generation
# =============================
def generate_image(prompt: str):
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
        raise RuntimeError(f"Error during image generation: {e}")

# =============================
# Flask Routes
# =============================
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        prompt = request.form.get("prompt")
        try:
            image_data = generate_image(prompt)
            return render_template_string(HTML_PAGE, image_data=image_data)
        except Exception as e:
            return render_template_string(HTML_PAGE, error=str(e))
    return render_template_string(HTML_PAGE)

@app.route("/download", methods=["POST"])
def download():
    image_data = request.form.get("image_data")
    if not image_data:
        return "No image available for download", 400
    img_bytes = BytesIO(base64.b64decode(image_data))
    img_bytes.seek(0)
    return send_file(
        img_bytes,
        mimetype="image/png",
        as_attachment=True,
        download_name="ai_image.png"
    )

@app.route("/robots.txt")
def robots():
    return send_file("robots.txt", mimetype="text/plain")

@app.route("/sitemap.xml")
def sitemap():
    return send_file("sitemap.xml", mimetype="application/xml")

# =============================
# Start Server
# =============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
