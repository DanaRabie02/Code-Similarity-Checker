from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import torch
import os
from transformers import AutoTokenizer, AutoConfig, AutoModelForSequenceClassification

app = Flask(__name__)
CORS(app)

# === Load models & tokenizer from local folders ===
tokenizer = AutoTokenizer.from_pretrained("binary_model")

config_bin = AutoConfig.from_pretrained("binary_model")
model_bin = AutoModelForSequenceClassification.from_pretrained("binary_model", config=config_bin)

config_mul = AutoConfig.from_pretrained("multiclass_model")
model_mul = AutoModelForSequenceClassification.from_pretrained("multiclass_model", config=config_mul)

@app.route("/")
def home():
    return send_file("index.html")

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

    # === Stage 2: Multi-Class Classification ===
    with torch.no_grad():
        logits_mul = model_mul(**inputs).logits
    pred_mul = torch.argmax(logits_mul, dim=-1).item()

    return jsonify({"type": f"Type {pred_mul}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
