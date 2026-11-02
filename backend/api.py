import os
import shutil
import tempfile

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from predict import predict_image


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="Smartphone Skin Lesion Detection API",
    version="1.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def root():

    return {
        "status": "running",
        "message": "Smartphone Skin Lesion Detection API"
    }


# ============================================================
# PREDICTION
# ============================================================

@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=os.path.splitext(
            file.filename
        )[1]
    )

    temp_file_path = temp_file.name

    temp_file.close()

    try:

        with open(
            temp_file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        result = predict_image(
            temp_file_path
        )

        return {
            "diagnosis": result["diagnosis"],
            "description": result["description"],
            "confidence": result["confidence"]
        }

    finally:

        if os.path.exists(
            temp_file_path
        ):

            os.remove(
                temp_file_path
            )
