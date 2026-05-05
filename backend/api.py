# api.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import shutil
import os
from backend.predict import analyze_file  # We are importing your existing logic!

app = FastAPI()

# Allow React (which runs on a different port) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict_skin_lesion(file: UploadFile = File(...)):
    # 1. Save the uploaded file temporarily
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 2. Run your PyTorch engine on it
    # (You will need to slightly modify your analyze_file function in predict.py 
    # to RETURN the text results instead of just printing them)
    result = analyze_file(temp_file_path) 
    
    # 3. Clean up the temp file
    os.remove(temp_file_path)
    
    # 4. Send the data back to React
    return {"diagnosis": result["diagnosis"], "confidence": result["confidence"]}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)