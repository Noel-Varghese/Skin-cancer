import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import cv2
import sys

# 1. Initialize hardware environment and load model architecture
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Rebuild the base ResNet18 structure
model = models.resnet18(weights=None)
model.fc = nn.Linear(model.fc.in_features, 7)

# Load the compiled model weights
try:
    model.load_state_dict(torch.load('skin_cancer_model.pth', map_location=device, weights_only=True))
except FileNotFoundError:
    print("Error: 'skin_cancer_model.pth' not found. Please execute the training script prior to inference.")
    sys.exit()

model = model.to(device)
model.eval() # Engage evaluation mode to disable gradient calculation

# Define the standard spatial transformations for inference
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) 
])

# Define the diagnostic classes corresponding to the dataset
classes = [
    'Melanocytic nevi', 'Melanoma (DANGER)', 'Benign keratosis-like lesions', 
    'Basal cell carcinoma (DANGER)', 'Actinic keratoses', 'Vascular lesions', 'Dermatofibroma'
]

def predict_single_frame(image_pil):
    """Executes a forward pass of a single image frame through the network."""
    input_tensor = transform(image_pil).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
    return probabilities

def analyze_file(file_path):
    """Processes multimodal inputs (images, video, GIFs) and returns diagnostic metrics."""
    print(f"\nProcessing File: {file_path}")
    
    # Evaluate sequential data formats
    if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.gif')):
        print("Sequential media detected. Extracting keyframes...")
        cap = cv2.VideoCapture(file_path)
        frame_count = 0
        cumulative_probs = torch.zeros(7).to(device)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: 
                break
            
            # Sample frames at a 1-second interval (assuming ~30 FPS)
            if frame_count % 30 == 0:
                # Convert BGR (OpenCV standard) to RGB (PIL standard)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(frame_rgb)
                
                probs = predict_single_frame(pil_img)
                cumulative_probs += probs
                
            frame_count += 1
            
        cap.release()
        
        # Calculate the mean probability across all evaluated frames
        frames_analyzed = (frame_count // 30) + 1
        final_probs = cumulative_probs / frames_analyzed
        print(f"Total keyframes evaluated: {frames_analyzed}")

    # Evaluate static image formats
    else:
        print("Static image detected.")
        image = Image.open(file_path).convert('RGB')
        final_probs = predict_single_frame(image)

    # Extract the highest probability class
    top_prob, top_class = torch.max(final_probs, 0)
    
    diagnosis_text = classes[top_class.item()]
    confidence_score = top_prob.item() * 100

    print("====================================")
    print(f"DIAGNOSIS: {diagnosis_text}")
    print(f"CONFIDENCE: {confidence_score:.2f}%")
    print("====================================\n")

    # Transmit the payload to the API layer
    return {"diagnosis": diagnosis_text, "confidence": confidence_score}

# ==========================================
# Independent Execution / Verification Block
# ==========================================
if __name__ == "__main__":
    # Specify a local test file path for manual verification
    test_file = r'data_set\archive\HAM10000_images_part_1\ISIC_0024306.jpg' 
    try:
        analyze_file(test_file)
    except Exception as e:
        print(f"Verification failed: {e}")