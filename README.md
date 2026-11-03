# DermAI Scanner

## Smartphone-Based Skin Lesion Classification System

DermAI Scanner is a full-stack artificial intelligence application developed as an academic research project for **skin lesion classification using smartphone-captured images**.

The system uses a deep learning model based on **EfficientNet-B0** and transfer learning to classify skin lesions into six categories. A **FastAPI backend** handles model inference, while a **React + Vite frontend** provides the user interface for image submission and result visualization.

The application is designed to run locally, allowing images to be processed without sending them to external cloud inference services.

> **Important:** This project is intended for academic and research purposes. It is not a medical diagnostic device and must not be used as a substitute for evaluation by a qualified medical professional.

---

## Features

- **Smartphone Image Classification**
  - Accepts normal RGB images captured using smartphones.
  - Does not require a dermatoscope for basic inference.

- **Deep Learning Classification**
  - Uses an EfficientNet-B0 convolutional neural network.
  - Uses transfer learning from pretrained ImageNet weights.

- **Six Skin Lesion Classes**
  - Actinic Keratosis
  - Basal Cell Carcinoma
  - Melanoma
  - Nevus
  - Squamous Cell Carcinoma
  - Seborrheic Keratosis

- **Confidence Score**
  - Displays the model's predicted class and confidence score.

- **Plain-English Explanation**
  - Each medical classification is accompanied by a short description intended for users without a medical background.

- **GPU Acceleration**
  - Supports NVIDIA CUDA acceleration through PyTorch when a compatible GPU is available.

- **Local Processing**
  - The FastAPI backend runs locally.
  - Images are processed on the local machine rather than being uploaded to an external inference service.

- **Web-Based Interface**
  - React-based frontend.
  - Vite development environment.
  - Responsive dark-themed interface.

---

## System Architecture

```text
                    ┌─────────────────────────┐
                    │       User / Camera     │
                    │   Smartphone Image      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      React Frontend     │
                    │     Vite + Tailwind     │
                    └────────────┬────────────┘
                                 │
                                 │ HTTP POST
                                 ▼
                    ┌─────────────────────────┐
                    │      FastAPI Backend     │
                    │        /predict          │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      predict.py          │
                    │     Image Preprocessing │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    EfficientNet-B0       │
                    │  SmartphoneSkinModel     │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │  Predicted Class +      │
                    │  Description + Confidence│
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      React Frontend     │
                    │       Result Display    │
                    └─────────────────────────┘
```

---

## Technology Stack

### Machine Learning

- Python
- PyTorch
- Torchvision
- EfficientNet-B0
- CUDA
- Pillow
- Pandas

### Backend

- FastAPI
- Uvicorn
- Python

### Frontend

- React
- Vite
- Tailwind CSS

### Development

- Git
- GitHub
- Virtual environments
- NVIDIA CUDA

---

## Dataset

The current smartphone-oriented model is trained using the **PAD-UFES-20 dataset**.

PAD-UFES-20 contains clinical skin lesion images captured using smartphones and associated clinical information. This makes it more relevant to the project's objective of investigating skin lesion classification from ordinary smartphone images rather than relying exclusively on dermoscopic imagery.

The dataset used in the project contains:

```text
Total images:       2298
Training images:    1828
Validation images:   470
```

The dataset is divided on a **patient-level basis** to reduce the possibility of images from the same patient appearing in both training and validation sets.

### Dataset Classes

| Code | Class | Description |
|---|---|---|
| ACK | Actinic Keratosis | Sun-damaged skin lesion |
| BCC | Basal Cell Carcinoma | Common type of skin cancer |
| MEL | Melanoma | Serious type of skin cancer |
| NEV | Nevus | Common mole / usually non-cancerous |
| SCC | Squamous Cell Carcinoma | Type of skin cancer |
| SEK | Seborrheic Keratosis | Common non-cancerous skin growth |

The dataset is **not included in the Git repository**.

---

## Model

The project uses **EfficientNet-B0** as its backbone.

The pretrained classifier is replaced with a six-class classification layer corresponding to the six target lesion categories.

```text
Input Image
    │
    ▼
Resize to 224 × 224
    │
    ▼
ImageNet Normalization
    │
    ▼
EfficientNet-B0
    │
    ▼
Fully Connected Layer
    │
    ▼
6 Class Probabilities
    │
    ▼
Predicted Class
```

### Training Configuration

```text
Architecture:       EfficientNet-B0
Transfer Learning:  ImageNet pretrained weights
Optimizer:           AdamW
Learning Rate:       0.0001
Batch Size:          32
Epochs:              15
Loss Function:       Cross Entropy Loss
Input Resolution:    224 × 224
```

### Current Baseline Result

The current baseline training run achieved:

```text
Best validation accuracy: 71.91%
Best epoch:               8
Final training accuracy:  93.44%
Final validation accuracy: 71.70%
```

These results represent the current academic baseline and should **not** be interpreted as clinical diagnostic performance.

The validation set contains relatively few melanoma samples, so accuracy alone is not sufficient to evaluate the model reliably. Future experimentation should include metrics such as:

- Precision
- Recall / Sensitivity
- Specificity
- F1 Score
- Macro F1
- Balanced Accuracy
- Confusion Matrix

---

## Model Files

The trained smartphone model is stored at:

```text
backend/models/smartphone_skin_model.pth
```

The model architecture is defined in:

```text
backend/model.py
```

Inference is handled by:

```text
backend/predict.py
```

---

## Project Structure

```text
skin-cancer/
│
├── backend/
│   │
│   ├── data_set/
│   │   ├── archive/
│   │   ├── archive.zip
│   │   ├── data/
│   │   ├── DermatoNet-TelessaudeRS/
│   │   ├── fitzpatrick17k.csv
│   │   └── zr7vgbcyr2-1/
│   │
│   ├── models/
│   │   └── smartphone_skin_model.pth
│   │
│   ├── api.py
│   ├── dataset.py
│   ├── model.py
│   ├── predict.py
│   ├── train.py
│   └── req.txt
│
├── frontend/
│   │
│   ├── src/
│   │   ├── App.jsx
│   │   ├── Landing.jsx
│   │   ├── Scanner.jsx
│   │   ├── Field.jsx
│   │   └── index.css
│   │
│   ├── package.json
│   └── vite.config.js
│
├── run_app.py
├── README.md
└── .gitignore
```

---

## Requirements

### Hardware

The system can run on CPU, but GPU acceleration is recommended for model inference and training.

Recommended:

```text
NVIDIA GPU
8 GB+ RAM
Modern multi-core CPU
```

The current development environment has been tested with an NVIDIA GPU using CUDA-enabled PyTorch.

### Software

```text
Python 3.11+
Node.js
npm
Git
NVIDIA CUDA-compatible PyTorch
```

---

## Installation

### 1. Clone the Repository

```bash
git clone git@github.com:Noel-Varghese/Skin-cancer.git
cd Skin-cancer
```

---

### 2. Create the Python Virtual Environment

```bash
python -m venv venv
```

Activate it on Linux:

```bash
source venv/bin/activate
```

On Windows:

```powershell
venv\Scripts\activate
```

---

### 3. Install Backend Dependencies

```bash
cd backend
pip install -r req.txt
```

Return to the project root:

```bash
cd ..
```

---

### 4. Install Frontend Dependencies

```bash
cd frontend
npm install
```

Return to the project root:

```bash
cd ..
```

---

## Running the Application

The project includes a unified launcher that starts both the backend and frontend.

From the project root:

```bash
python run_app.py
```

The backend will run at:

```text
http://127.0.0.1:8000
```

The frontend will run at:

```text
http://localhost:5173
```

Open the frontend URL in a web browser.

---

## Backend API

The primary inference endpoint is:

```text
POST /predict
```

The endpoint accepts an uploaded image and returns the model prediction.

Example response:

```json
{
    "diagnosis": "Actinic Keratosis",
    "description": "Sun-damaged skin lesion",
    "confidence": 0.8291
}
```

The confidence value is returned as a decimal between `0` and `1`.

For example:

```text
0.8291 → 82.91%
```

---

## Command-Line Prediction

The model can also be tested directly without the frontend.

From the backend directory:

```bash
cd backend
```

Run:

```bash
python predict.py path/to/image.jpg
```

Example:

```bash
python predict.py data_set/zr7vgbcyr2-1/images/imgs_part_1/PAT_104_1755_320.png
```

Example output:

```text
==================================================
SKIN LESION ANALYSIS
==================================================
Prediction: Actinic Keratosis
Meaning: Sun-damaged skin lesion
Confidence: 82.91%
==================================================

This is a research/educational model and is not a medical diagnosis.
```

---

## GPU Verification

The project automatically detects whether CUDA is available.

The inference device is selected using:

```python
torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)
```

To verify CUDA support:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

A working CUDA installation should return:

```text
True
```

The model can therefore use an NVIDIA GPU when available and fall back to CPU otherwise.

---

## Training

Training is performed using:

```text
backend/train.py
```

Before training, ensure that the required dataset files are available in the expected `backend/data_set/` structure.

Run:

```bash
cd backend
python train.py
```

The training pipeline:

1. Loads the dataset metadata.
2. Locates the corresponding image files.
3. Filters the required six lesion classes.
4. Splits the data at the patient level.
5. Applies image preprocessing.
6. Loads the pretrained EfficientNet-B0 model.
7. Replaces the classifier with a six-class output layer.
8. Trains using AdamW.
9. Evaluates on the validation set.
10. Saves the trained model.

The trained model is saved as:

```text
backend/models/smartphone_skin_model.pth
```

---

## Inference Pipeline

For an uploaded smartphone image, the system performs the following steps:

```text
Image Upload
     │
     ▼
Read Image
     │
     ▼
Convert to RGB
     │
     ▼
Resize to 224 × 224
     │
     ▼
Convert to Tensor
     │
     ▼
Normalize
     │
     ▼
EfficientNet-B0
     │
     ▼
Softmax
     │
     ▼
Highest Probability Class
     │
     ├── Diagnosis
     ├── Description
     └── Confidence
```

---

## Supported Classes

### Actinic Keratosis

A sun-damaged skin lesion that can sometimes be considered precancerous.

### Basal Cell Carcinoma

A common type of skin cancer.

### Melanoma

A serious type of skin cancer.

### Nevus

A common mole that is usually non-cancerous.

### Squamous Cell Carcinoma

A type of skin cancer.

### Seborrheic Keratosis

A common non-cancerous skin growth.

---

## Privacy

The application is designed around local processing.

The current development configuration uses:

```text
Frontend → 127.0.0.1:8000 → Local Model
```

No external cloud inference API is required for the prediction pipeline.

This architecture is useful for academic experimentation where maintaining local control over uploaded images is important.

However, local execution alone does not automatically guarantee complete privacy or security. Proper handling of uploaded files, temporary files, logs, operating-system permissions, and deployment configuration is still required for production use.

---

## Limitations

This project is an academic research prototype and has several limitations.

### Dataset Limitations

The model is trained using a limited dataset and may not generalize to every population, camera, lighting condition, or skin type.

### Smartphone Domain Shift

The model is intended for smartphone-based images, but real-world smartphone images can differ substantially from training images due to:

- Lighting
- Camera hardware
- Image compression
- Distance from the lesion
- Focus and motion blur
- Skin tone
- Background information
- Multiple lesions in one image
- Hair or other visual obstructions

### Class Imbalance

The dataset contains significantly different numbers of samples across lesion classes, particularly for melanoma.

Therefore, overall accuracy alone does not provide a complete picture of model performance.

### Confidence Is Not Certainty

A high model confidence score does not mean that the prediction is medically correct.

For example:

```text
Confidence: 90%
```

does **not** mean:

```text
90% medically certain
```

It represents the model's probability output for its predicted class.

---

## Future Work

Potential future improvements include:

- Class-weighted training
- Focal loss
- Better handling of class imbalance
- Macro F1 and balanced accuracy evaluation
- Confusion matrix analysis
- Sensitivity and specificity analysis
- External smartphone-image validation
- Data augmentation
- Model calibration
- Additional clinical metadata integration
- Knowledge transfer using additional dermatology datasets
- Improved lesion localization
- Mobile application integration
- More robust image-quality checking
- Explainable AI techniques such as Grad-CAM

---

## Academic Purpose

The project is intended to demonstrate the application of:

- Computer vision
- Deep learning
- Transfer learning
- Medical image classification
- Full-stack machine learning deployment
- Local GPU acceleration
- REST API development
- React-based machine learning interfaces

The project also investigates the feasibility of using **ordinary smartphone images** as input for skin lesion classification.

---

## Disclaimer

This software is an **academic and research prototype**.

It is **not a certified medical device**, is not intended to provide a medical diagnosis, and should not be used to make medical decisions.

The predictions produced by the model should not replace examination or advice from a qualified dermatologist or other healthcare professional.

If a skin lesion is concerning, changing, painful, bleeding, or otherwise unusual, seek evaluation from a qualified healthcare professional regardless of the model's prediction.

---

## License

This project is intended for academic and educational use.

Dataset licensing and usage restrictions remain subject to the original dataset providers and their respective terms.

---

## Authors

**Noel Varghese**

Computer Science Engineering  
Academic Research Project — Skin Lesion Classification
