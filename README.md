<<<<<<< HEAD
---
title: Code Similarity Checker
emoji: 🧠
colorFrom: indigo
colorTo: blue
sdk: docker
app_file: app.py
pinned: false
---

# 💻 Code Similarity Checker

An AI-powered web tool that detects similarity between two code snippets and classifies them into specific **code clone types** using deep learning.

This tool was developed by **Computer Engineering students** as part of a graduation project. It uses a custom-trained language model based on [Hugging Face Transformers](https://huggingface.co/transformers/) to semantically and syntactically analyze code pairs.

---

## 🧠 What It Does

1. **Compares two code snippets**
2. **Runs binary classification** to check if they are similar
3. **If similar**, it performs **multi-class classification** to determine the clone type:
   - `Type 0`: Completely different codes
   - `Type 1`: Identical except for whitespace/comments
   - `Type 2`: Same code structure with renamed variables/functions
   - `Type 3`: Same algorithm, different implementation
   - `Type 4`: Different algorithm, same functionality

---

## 🚀 How It Works

- Built with **Flask** backend and a lightweight **HTML/CSS/JS** frontend
- Loads two Hugging Face models (binary + multi-class)
- Accepts user input via the web UI and returns predictions instantly

---

## 🛠️ Technologies Used

- Python · Flask
- Hugging Face Transformers
- PyTorch
- HTML · CSS · JavaScript
- Hugging Face Spaces

---

## 📦 Model Files

Two pre-trained models are included:
- `binary_model/` – For similarity detection
- `multiclass_model/` – For clone type classification (1–4)

Both models are stored locally in the Space and loaded at runtime.

---

## 📝 Disclaimer

> This tool is for academic/demo use only. While great care was taken to train and validate the models, **predictions may occasionally vary** due to dataset limitations or model bias. Please do not rely on results for critical systems without proper validation.

---

## 🧑‍🎓 Authors

Developed by:
- **Dana Rabie**  
- **Leen Abderrahman**  

Computer Engineering Students  
University of Jordan – Class of 2025

---

## 🌐 Demo

Check it out live 👉 [Insert your Hugging Face Space link here]
=======
# Code-Similarity-Checker
 Code Similarity Checker
>>>>>>> ce8be2b424992ac19685c1e303784871c4a85789
