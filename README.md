# DermAI Scanner: Multimodal Skin Cancer Diagnostic System

## Overview
DermAI Scanner is a full-stack, multimodal artificial intelligence application designed to classify and diagnose skin lesions. Built as an academic project, the system utilizes Transfer Learning via a ResNet18 Convolutional Neural Network (CNN) to analyze dermoscopic images, videos, and GIFs. 

The application operates entirely locally, ensuring 100% data sovereignty and patient privacy without reliance on external cloud APIs.

## Key Features
*   **Multimodal Inference:** Processes static images (`.jpg`, `.png`) and extracts sequential keyframes from video formats (`.mp4`, `.gif`) for temporal analysis.
*   **Hardware Acceleration:** Configured for local GPU acceleration utilizing CUDA for high-speed tensor processing.
*   **Privacy-First Architecture:** All data processing, inference, and routing occur strictly on the local loopback address (`127.0.0.1`).
*   **Modern User Interface:** Features a responsive, dark-mode dashboard built with React and Tailwind CSS v4.

## Technology Stack
*   **Machine Learning Engine:** PyTorch, Torchvision, OpenCV, Pandas
*   **Backend API:** FastAPI, Uvicorn, Python 3
*   **Frontend UI:** React, Vite, Tailwind CSS v4
*   **Dataset:** Trained on the HAM10000 (Human Against Machine) dataset comprising 10,015 high-resolution dermatoscopic images.

## Project Structure
```text
dermai-scanner/
│
├── backend/                  # AI Model and API Server
│   ├── data_set/             # HAM10000 dataset (Ignored in Git)
│   ├── api.py                # FastAPI routing and server
│   ├── dataset.py            # PyTorch custom dataset loader
│   ├── predict.py            # Inference engine and frame extraction
│   ├── train.py              # ResNet18 training pipeline
│   ├── requirements.txt      # Python dependencies
│   └── skin_cancer_model.pth # Compiled model weights (Generated post-training)
│
├── frontend/                 # React User Interface
│   ├── src/                  # React components (App.jsx, etc.)
│   ├── package.json          # Node dependencies
│   └── vite.config.js        # Vite + Tailwind v4 configuration
│
├── run_app.py                # Unified launch script
└── README.md                 # Project documentation

Installation & Setup
Prerequisites
Python 3.11+ (64-bit)

Node.js & npm (Latest LTS)

NVIDIA GPU (Highly recommended for CUDA acceleration)

1. Backend Environment Setup
Navigate to the backend directory and install the necessary Python dependencies:
cd backend
pip install -r requirements.txt
Here is a complete, formal README.md for your project. It is structured to look highly professional for your college submission and GitHub repository.

You can create a file named README.md in your main root folder and paste this directly into it.

Markdown
# DermAI Scanner: Multimodal Skin Cancer Diagnostic System

## Overview
DermAI Scanner is a full-stack, multimodal artificial intelligence application designed to classify and diagnose skin lesions. Built as an academic project, the system utilizes Transfer Learning via a ResNet18 Convolutional Neural Network (CNN) to analyze dermoscopic images, videos, and GIFs. 

The application operates entirely locally, ensuring 100% data sovereignty and patient privacy without reliance on external cloud APIs.

## Key Features
*   **Multimodal Inference:** Processes static images (`.jpg`, `.png`) and extracts sequential keyframes from video formats (`.mp4`, `.gif`) for temporal analysis.
*   **Hardware Acceleration:** Configured for local GPU acceleration utilizing CUDA for high-speed tensor processing.
*   **Privacy-First Architecture:** All data processing, inference, and routing occur strictly on the local loopback address (`127.0.0.1`).
*   **Modern User Interface:** Features a responsive, dark-mode dashboard built with React and Tailwind CSS v4.

## Technology Stack
*   **Machine Learning Engine:** PyTorch, Torchvision, OpenCV, Pandas
*   **Backend API:** FastAPI, Uvicorn, Python 3
*   **Frontend UI:** React, Vite, Tailwind CSS v4
*   **Dataset:** Trained on the HAM10000 (Human Against Machine) dataset comprising 10,015 high-resolution dermatoscopic images.

## Project Structure
```text
dermai-scanner/
│
├── backend/                  # AI Model and API Server
│   ├── data_set/             # HAM10000 dataset (Ignored in Git)
│   ├── api.py                # FastAPI routing and server
│   ├── dataset.py            # PyTorch custom dataset loader
│   ├── predict.py            # Inference engine and frame extraction
│   ├── train.py              # ResNet18 training pipeline
│   ├── requirements.txt      # Python dependencies
│   └── skin_cancer_model.pth # Compiled model weights (Generated post-training)
│
├── frontend/                 # React User Interface
│   ├── src/                  # React components (App.jsx, etc.)
│   ├── package.json          # Node dependencies
│   └── vite.config.js        # Vite + Tailwind v4 configuration
│
├── run_app.py                # Unified launch script
└── README.md                 # Project documentation
Installation & Setup
Prerequisites
Python 3.11+ (64-bit)

Node.js & npm (Latest LTS)

NVIDIA GPU (Highly recommended for CUDA acceleration)

1. Backend Environment Setup
Navigate to the backend directory and install the necessary Python dependencies:


cd backend
pip install -r requirements.txt
Note: Ensure you download and extract the HAM10000 dataset into the backend/data_set/archive/ directory before initiating training.

2. Frontend Environment Setup
Navigate to the frontend directory and install the Node modules:

cd frontend
npm install

Model Training
Before running the application, you must compile the neural network weights. Navigate to the backend folder and execute the training script:

python train.py
Upon successful completion, this will generate the skin_cancer_model.pth file required for the prediction engine.

Running the Application
The system features a unified launch script to start both the FastAPI backend and the React frontend simultaneously.

From the root directory, execute:
python run_app.py
Backend API: Automatically binds to http://127.0.0.1:8000

Frontend UI: Automatically binds to http://localhost:5173 (Open this in your browser)

Diagnostic Classes Supported
The model is trained to classify the following lesion types:

Melanocytic nevi

Melanoma (Malignant)

Benign keratosis-like lesions

Basal cell carcinoma (Malignant)

Actinic keratoses

Vascular lesions

Dermatofibroma

Disclaimer
This application was developed strictly for academic and educational purposes. It is not an FDA-approved medical device and should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult a certified dermatologist for medical concerns.