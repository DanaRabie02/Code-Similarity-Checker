from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import torch
import os
import zipfile
import requests
from transformers import AutoTokenizer, AutoModelForSequenceClassification

app = Flask(__name__)
CORS(app)

# === Download & Extract Models from Google Drive ===

def download_and_extract_model(url, zip_name, output_dir):
    if not os.path.exists(output_dir):
        print(f"Downloading {zip_name}...")
        r = requests.get(url)
        with open(zip_name, 'wb') as f:
            f.write(r.content)

        print("Extracting...")
        with zipfile.ZipFile(zip_name, 'r') as zip_ref:
            zip_ref.extractall(output_dir)

        os.remove(zip_name)
        print(f"{output_dir} is ready.")

# Replace these IDs with your actual zipped model file IDs
download_and_extract_model(
    "https://drive.google.com/uc?export=download&id=1GUoqoCfAfVw_XPqenISwOFGGwe5_4VyG",
    "binary_model.zip",
    "binary_model"
)

download_and_extract_model(
    "https://drive.google.com/uc?export=download&id=1C24L5wQypJzu359E2EW4Jgw1NHIJLKkA",
    "multiclass_model.zip",
    "multiclass_model"
)

# === Load models & tokenizer ===
tokenizer = AutoTokenizer.from_pretrained("binary_model")
model_bin = AutoModelForSequenceClassification.from_pretrained("binary_model")
model_mul = AutoModelForSequenceClassification.from_pretrained("multiclass_model")

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
    
    # === Stage 1: Binary Classification ===
    with torch.no_grad():
        logits_bin = model_bin(**inputs).logits
    pred_bin = torch.argmax(logits_bin, dim=-1).item()
    
    if pred_bin == 0:
        return jsonify({"type": "Type 0"})

    # === Stage 2: Multi-Class Clone Type ===
    with torch.no_grad():
        logits_mul = model_mul(**inputs).logits
    pred_mul = torch.argmax(logits_mul, dim=-1).item()
    return jsonify({"type": f"Type {pred_mul}"})

@app.route("/")
def home():
    return send_from_directory("", "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
