import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import cv2
import sys

# 1. Setup device and load the saved model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Rebuild the ResNet18 structure
model = models.resnet18(weights=None)
model.fc = nn.Linear(model.fc.in_features, 7)

# Load your trained weights
try:
    model.load_state_dict(torch.load('skin_cancer_model.pth', map_location=device, weights_only=True))
except FileNotFoundError:
    print("Error: 'skin_cancer_model.pth' not found. Run train.py first!")
    sys.exit()

model = model.to(device)
model.eval() # Set to evaluation mode (turns off training mechanics)

# Standard image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) 
])

# HAM10000 Class Labels
classes = ['Melanocytic nevi', 'Melanoma (DANGER)', 'Benign keratosis-like lesions', 
           'Basal cell carcinoma (DANGER)', 'Actinic keratoses', 'Vascular lesions', 'Dermatofibroma']

def predict_single_frame(image_pil):
    """Passes a single image through the AI."""
    input_tensor = transform(image_pil).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
    return probabilities

def analyze_file(file_path):
    print(f"\nAnalyzing: {file_path}")
    
    # Check if it's a video or GIF
    if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.gif')):
        print("Video/GIF detected. Extracting frames...")
        cap = cv2.VideoCapture(file_path)
        frame_count = 0
        cumulative_probs = torch.zeros(7).to(device)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            # Analyze 1 frame every second (assuming 30fps) to save time
            if frame_count % 30 == 0:
                # Convert OpenCV frame (BGR) to PIL Image (RGB)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(frame_rgb)
                
                probs = predict_single_frame(pil_img)
                cumulative_probs += probs
                
            frame_count += 1
            
        cap.release()
        
        # Average the predictions across all extracted frames
        frames_analyzed = (frame_count // 30) + 1
        final_probs = cumulative_probs / frames_analyzed
        print(f"Analyzed {frames_analyzed} keyframes.")

    # Otherwise, treat it as a standard static image
    else:
        print("Static image detected.")
        image = Image.open(file_path).convert('RGB')
        final_probs = predict_single_frame(image)

    # Output the final result
    top_prob, top_class = torch.max(final_probs, 0)
    print("====================================")
    print(f"DIAGNOSIS: {classes[top_class.item()]}")
    print(f"CONFIDENCE: {top_prob.item() * 100:.2f}%")
    print("====================================\n")

# ==========================================
# TEST SCRIPT 
# ==========================================
if __name__ == "__main__":
    # Test it by pointing it to one of your dataset images
    # Replace this with any .jpg, .gif, or .mp4 file path on your computer!
    test_file = r'data_set\archive\HAM10000_images_part_1\ISIC_0024306.jpg' 
    analyze_file(test_file)