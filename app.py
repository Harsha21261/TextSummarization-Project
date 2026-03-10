import sys
import os
import traceback

# Add src to the Python path to allow absolute imports from 'src'
sys.path.append(os.path.abspath('src'))

from fastapi import FastAPI
import uvicorn
from starlette.responses import RedirectResponse
from textsummarizer.pipeline.prediction import PredictionPipeline

app = FastAPI()

# Global predictor - created once, model loads lazily on first predict call
predictor = PredictionPipeline()

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def training():
    try:
        os.system("python main.py")
        return {"message": "Training successful !!"}
    except Exception as e:
        return {"error": f"Error Occurred! {e}"}

@app.post("/predict")
async def predict_route(text: str):
    try:
        output = predictor.predict(text)
        return {"summary": output}
    except Exception as e:
        error_details = traceback.format_exc()
        return {"error": str(e), "details": error_details}

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
