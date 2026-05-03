import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models, transforms
from torch.utils.data import DataLoader, random_split
from dataset import SkinCancerDataset

# 1. Setup Device (Use your GPU if available, otherwise CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Hardware Check: Using device: {device}")

# 2. Define Transforms & Load Data
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) 
])

# Initialize the dataset
full_dataset = SkinCancerDataset(
    csv_file=r'data_set\archive\HAM10000_metadata.csv', 
    root_dir=r'data_set\archive', 
    transform=transform
)

# Split into Training (80%) and Validation (20%)
train_size = int(0.8 * len(full_dataset))
val_size = len(full_dataset) - train_size
train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])

# Create DataLoaders
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
print(f"Data ready: {len(train_dataset)} training images, {len(val_dataset)} validation images.")

# 3. Build the Model (Transfer Learning with ResNet18)
print("Downloading pre-trained ResNet18...")
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

# HAM10000 has 7 classes, so we replace the final output layer
model.fc = nn.Linear(model.fc.in_features, 7)
model = model.to(device)

# 4. Loss Function and Optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 5. Quick Training Loop (Testing 1 Epoch to ensure pipeline works)
print("Starting engine... kicking off Epoch 1.")
for epoch in range(1):
    model.train()
    
    for i, (inputs, labels) in enumerate(train_loader):
        # Move data to GPU/CPU
        inputs, labels = inputs.to(device), labels.to(device)
        
        # Zero out the gradients
        optimizer.zero_grad()
        
        # Forward pass (make predictions)
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        
        # Backward pass (learn from mistakes)
        loss.backward()
        optimizer.step()
        
        # Print progress every 10 batches
        if i % 10 == 0:  
            print(f"Batch [{i}/{len(train_loader)}] | Current Loss: {loss.item():.4f}")

print("Test run complete. The AI pipeline is fully functional!")
torch.save(model.state_dict(), 'skin_cancer_model.pth')
print("Model saved as skin_cancer_model.pth!")