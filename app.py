from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import torch
import os
import zipfile
import requests
from transformers import AutoTokenizer, AutoConfig
from transformers.models.bert.modeling_bert import BertForSequenceClassification as ModernBertForSequenceClassification

app = Flask(__name__)
CORS(app)

# === Download & Extract Models from Dropbox ===

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

# === Replace with your Dropbox direct download links (dl=1)
download_and_extract_model(
    "https://www.dropbox.com/scl/fi/7546xgiiz54z7sx9jnj3n/binary_model.zip?rlkey=f34hv64mvp9hy09fj20w9yg3z&st=j6abfurj&dl=1",
    "binary_model.zip",
    "binary_model"
)

download_and_extract_model(
    "https://www.dropbox.com/scl/fi/j4djgtfp5rr0mdd329665/multiclass_model.zip?rlkey=f66xdidjwxzghmcfjiqjhpc4y&st=oes5rm8j&dl=1",
    "multiclass_model.zip",
    "multiclass_model"
)

# === Load models & tokenizer ===
tokenizer = AutoTokenizer.from_pretrained("binary_model")

config_bin = AutoConfig.from_pretrained("binary_model")
model_bin = ModernBertForSequenceClassification.from_pretrained("binary_model", config=config_bin)

config_mul = AutoConfig.from_pretrained("multiclass_model")
model_mul = ModernBertForSequenceClassification.from_pretrained("multiclass_model", config=config_mul)

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
