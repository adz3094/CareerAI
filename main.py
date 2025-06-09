# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from ml_logic import CareerRecommender
import uvicorn

# Initialize FastAPI app
app = FastAPI()

# Allow requests from any frontend (React, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the recommender
recommender = CareerRecommender("careers.json")

@app.post("/recommend")
async def recommend(request: Request):
    """
    Receives user input JSON and returns top 3 career recommendations
    """
    try:
        user_input = await request.json()
        recommendations = recommender.get_recommendations(user_input, top_k=3)
        return {"recommendations": recommendations}
    except Exception as e:
        return {"error": str(e)}
