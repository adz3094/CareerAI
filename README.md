# ✨ AI-Powered Career Path Recommender
This project is a full-stack AI Career Recommender System that suggests the top 3 career paths based on a user’s selected skills, interests, work preferences, and soft skills.

It combines:

A clean React frontend (form + results UI)

A lightweight FastAPI backend

A simple machine learning recommendation engine using cosine similarity

# 🔍 What It Does
You fill out a form describing yourself (like skills, interests, etc.)

The backend matches your input against a dataset of careers

It returns the top 3 closest careers — personalized to you!

No training or external models — just smart logic + cosine similarity between binary vectors. Great for quick demos, prototypes, or beginner ML learners!

# 🧠 Tech Stack
Frontend: HTML + JavaScript

Backend: FastAPI (Python)

ML Logic: Feature vectorization + cosine similarity (with scikit-learn)

Data: Static JSON dataset of careers with skills/interests

# 📁 Key Features
🧠 Converts user form data into binary vectors

🤖 Recommends careers using cosine similarity

💡 Clear explanations and top-ranked matches

⚡ FastAPI-based backend with CORS support

🖼️ Sleek UI with expandable "View Details" cards

📦 Easily extendable with more careers or model upgrades

# 🚀 Getting Started
Clone the repo

Install backend dependencies (pip install -r requirements.txt)

Run the FastAPI backend (uvicorn main:app --reload)

Open the frontend in your browser

Try it out!
