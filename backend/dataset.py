import os
import pandas as pd
from glob import glob
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

class SkinCancerDataset(Dataset):
    def __init__(self, csv_file, root_dir, transform=None):
        """
        csv_file: Path to HAM10000_metadata.csv
        root_dir: Directory containing the part_1 and part_2 image folders
        """
        self.df = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform
        
        # 1. Handle the "Two Parts" issue by mapping every image ID to its exact folder path
        image_paths = glob(os.path.join(root_dir, '*', '*.jpg'))
        imageid_path_dict = {os.path.splitext(os.path.basename(x))[0]: x for x in image_paths}
        
        # Add the exact file path to our dataframe
        self.df['path'] = self.df['image_id'].map(imageid_path_dict)
        
        # Drop any rows where an image wasn't found (just in case of corrupted downloads)
        self.df = self.df.dropna(subset=['path'])

        # 2. Convert text labels (e.g., 'mel', 'bcc') to numeric classes (0 to 6)
        # HAM10000 has 7 distinct skin lesion types
        self.label_mapping = {
            'nv': 0, 'mel': 1, 'bkl': 2, 'bcc': 3, 
            'akiec': 4, 'vasc': 5, 'df': 6
        }
        self.df['target'] = self.df['dx'].map(self.label_mapping)

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        # Grab image path and label for the current row
        img_path = self.df['path'].iloc[idx]
        label = self.df['target'].iloc[idx]
        
        # Open image using Pillow
        image = Image.open(img_path).convert('RGB')
        
        # Apply transformations (resizing, converting to AI tensor)
        if self.transform:
            image = self.transform(image)
            
        return image, torch.tensor(label, dtype=torch.long)

if __name__ == "__main__":
    # Define how the images should be processed
    # 224x224 is the standard size for ResNet and other major CNNs
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) 
    ])

    # Initialize the dataset (Update 'data' to match your folder name if different)
    dataset = SkinCancerDataset(
        csv_file=r'data_set\archive\HAM10000_metadata.csv', 
        root_dir=r'data_set\archive', 
        transform=transform
    )

    # Wrap it in a DataLoader (this handles feeding batches to the GPU later)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    print(f"Successfully loaded {len(dataset)} images.")
    
    # Grab one batch to test
    images, labels = next(iter(dataloader))
    print(f"Batch Image Tensor Shape: {images.shape} (Batch Size, Channels, Height, Width)")
    print(f"Batch Labels: {labels}")