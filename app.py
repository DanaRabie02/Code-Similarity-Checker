import os
os.environ["TORCHINDUCTOR_CACHE_DIR"] = "/tmp/inductor_cache"
os.environ["TORCHINDUCTOR_DISABLE"] = "1"

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import torch
import zipfile
import requests
import time  # Added for sleep

from transformers import AutoConfig, AutoModelForSequenceClassification
from transformers import PreTrainedTokenizerFast

from modernbert.modeling_modernbert import ModernBertForSequenceClassification
from modernbert.configuration_modernbert import ModernBertConfig

# === Register ModernBert ===
AutoConfig.register("modernbert", ModernBertConfig, exist_ok=True)
AutoModelForSequenceClassification.register(ModernBertConfig, ModernBertForSequenceClassification, exist_ok=True)

app = Flask(__name__)
CORS(app)

# === Download & Extract models only if needed ===
def download_and_extract_model(url, zip_name, extract_to):
    if not os.path.exists(extract_to):
        print(f"Downloading {zip_name}...")
        r = requests.get(url)
        with open(zip_name, "wb") as f:
            f.write(r.content)
        print("Extracting...")
        with zipfile.ZipFile(zip_name, "r") as zip_ref:
            zip_ref.extractall(extract_to)
        os.remove(zip_name)
        print(f"{extract_to} is ready.")

# === Pull models from GitHub Releases ===
download_and_extract_model(
    "https://github.com/DanaRabie02/Code-Similarity-Checker/releases/download/v1/binary_model.zip",
    "/tmp/binary_model.zip",
    "/tmp/binary_model"
)

download_and_extract_model(
    "https://github.com/DanaRabie02/Code-Similarity-Checker/releases/download/v1/multiclass_model.zip",
    "/tmp/multiclass_model.zip",
    "/tmp/multiclass_model"
)

# === Load tokenizer (wait until it's fully extracted) ===
tokenizer_path = "/tmp/binary_model/tokenizer.json"

# Wait up to 10 seconds for the file to appear
for _ in range(20):
    if os.path.exists(tokenizer_path):
        break
    time.sleep(0.5)
else:
    raise FileNotFoundError(f"{tokenizer_path} not found after waiting.")

tokenizer = PreTrainedTokenizerFast(tokenizer_file=tokenizer_path)

# === Load models ===
config_bin = AutoConfig.from_pretrained("/tmp/binary_model", local_files_only=True)
model_bin = ModernBertForSequenceClassification.from_pretrained("/tmp/binary_model", config=config_bin, local_files_only=True)

config_mul = AutoConfig.from_pretrained("/tmp/multiclass_model", local_files_only=True)
model_mul = ModernBertForSequenceClassification.from_pretrained("/tmp/multiclass_model", config=config_mul, local_files_only=True)

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
