from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import torch
import os
import zipfile
import requests
from transformers import AutoTokenizer, AutoConfig, AutoModelForSequenceClassification

app = Flask(__name__)
CORS(app)

# === Download & Extract models only if needed ===
def download_and_extract_model(url, zip_name, extract_to):
    if not os.path.exists(extract_to):
        print(f"Downloading {zip_name}...")
        r = requests.get(url)
        zip_path = f"/tmp/{zip_name}"
        with open(zip_path, "wb") as f:
            f.write(r.content)
        print("Extracting...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
        os.remove(zip_path)
        print(f"{extract_to} is ready.")

# === Pull models from GitHub Releases ===
download_and_extract_model(
    "https://github.com/DanaRabie02/Code-Similarity-Checker/releases/download/v1/binary_model.zip",
    "binary_model.zip",
    "/tmp/binary_model"
)

download_and_extract_model(
    "https://github.com/DanaRabie02/Code-Similarity-Checker/releases/download/v1/multiclass_model.zip",
    "multiclass_model.zip",
    "/tmp/multiclass_model"
)

# === Load models & tokenizer ===
tokenizer = AutoTokenizer.from_pretrained("/tmp/binary_model", local_files_only=True)

config_bin = AutoConfig.from_pretrained("/tmp/binary_model", local_files_only=True)
model_bin = AutoModelForSequenceClassification.from_pretrained("/tmp/binary_model", config=config_bin, local_files_only=True)

config_mul = AutoConfig.from_pretrained("/tmp/multiclass_model", local_files_only=True)
model_mul = AutoModelForSequenceClassification.from_pretrained("/tmp/multiclass_model", config=config_mul, local_files_only=True)

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_file(os.path.join("static", filename))

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json or {}
    code1 = data.get("code1", "")
    code2 = data.get("code2", "")

    inputs = tokenizer(code1, code2,
                       padding="max_length",
                       truncation=True,
                       max_length=512,
                       return_tensors="pt")

    with torch.no_grad():
        logits_bin = model_bin(**inputs).logits
    pred_bin = torch.argmax(logits_bin, dim=-1).item()

    if pred_bin == 0:
        return jsonify({"type": "Type 0"})

    with torch.no_grad():
        logits_mul = model_mul(**inputs).logits
    pred_mul = torch.argmax(logits_mul, dim=-1).item()

    return jsonify({"type": f"Type {pred_mul}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
