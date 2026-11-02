import os

import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim

from torch.utils.data import DataLoader

from torchvision import transforms

from dataset import PADUFES20Dataset
from model import SmartphoneSkinModel


# ============================================================
# CONFIGURATION
# ============================================================

CSV_FILE = "data_set/zr7vgbcyr2-1/metadata.csv"

IMAGE_ROOT = "data_set/zr7vgbcyr2-1/images"

MODEL_DIR = "models"

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "smartphone_skin_model.pth"
)

BATCH_SIZE = 32

EPOCHS = 15

LEARNING_RATE = 0.0001

IMAGE_SIZE = 224

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# ============================================================
# IMAGE TRANSFORMS
# ============================================================

train_transform = transforms.Compose([

    transforms.Resize(
        (IMAGE_SIZE, IMAGE_SIZE)
    ),

    transforms.RandomHorizontalFlip(),

    transforms.RandomVerticalFlip(),

    transforms.RandomRotation(15),

    transforms.ColorJitter(
        brightness=0.2,
        contrast=0.2,
        saturation=0.2
    ),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


val_transform = transforms.Compose([

    transforms.Resize(
        (IMAGE_SIZE, IMAGE_SIZE)
    ),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# ============================================================
# FIND ALL PAD-UFES IMAGES
# ============================================================

def find_image_paths():

    print()
    print("Searching for PAD-UFES images...")

    image_map = {}

    for root, directories, files in os.walk(IMAGE_ROOT):

        for filename in files:

            extension = os.path.splitext(
                filename
            )[1].lower()

            if extension in [
                ".jpg",
                ".jpeg",
                ".png"
            ]:

                image_map[filename] = os.path.join(
                    root,
                    filename
                )

    print(
        "Images found on disk:",
        len(image_map)
    )

    return image_map


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("SMARTPHONE SKIN LESION MODEL")
    print("=" * 60)

    print(
        "Device:",
        DEVICE
    )

    if DEVICE.type == "cuda":

        print(
            "GPU:",
            torch.cuda.get_device_name(0)
        )

    print()

    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )

    # ========================================================
    # FIND IMAGES
    # ========================================================

    image_map = find_image_paths()

    # ========================================================
    # LOAD METADATA
    # ========================================================

    print()
    print("Loading metadata...")

    dataframe = pd.read_csv(
        CSV_FILE
    )

    print(
        "Metadata records:",
        len(dataframe)
    )

    # ========================================================
    # KEEP SIX CLASSES
    # ========================================================

    valid_classes = [
        "ACK",
        "BCC",
        "MEL",
        "NEV",
        "SCC",
        "SEK"
    ]

    dataframe = dataframe[
        dataframe["diagnostic"].isin(
            valid_classes
        )
    ].copy()

    print(
        "Records after class filtering:",
        len(dataframe)
    )

    # ========================================================
    # MAP IMAGE NAMES TO ACTUAL FILE PATHS
    # ========================================================

    dataframe["image_path"] = (
        dataframe["img_id"].map(
            image_map
        )
    )

    missing = dataframe[
        dataframe["image_path"].isna()
    ]

    if len(missing) > 0:

        print()
        print(
            "WARNING:",
            len(missing),
            "metadata images could not be found."
        )

        print(
            "First missing files:"
        )

        print(
            missing["img_id"]
            .head(10)
            .to_string(index=False)
        )

    dataframe = dataframe[
        dataframe["image_path"].notna()
    ].copy()

    print()
    print(
        "Images matched with metadata:",
        len(dataframe)
    )

    # ========================================================
    # CHECK
    # ========================================================

    if len(dataframe) == 0:

        raise RuntimeError(
            "No images were matched with metadata. "
            "Check the dataset path."
        )

    # ========================================================
    # PATIENT-LEVEL SPLIT
    # ========================================================

    print()
    print(
        "Creating patient-level train/validation split..."
    )

    patients = dataframe[
        "patient_id"
    ].unique()

    generator = torch.Generator().manual_seed(
        42
    )

    permutation = torch.randperm(
        len(patients),
        generator=generator
    ).numpy()

    patients = patients[
        permutation
    ]

    split_index = int(
        0.8 * len(patients)
    )

    train_patients = set(
        patients[:split_index]
    )

    val_patients = set(
        patients[split_index:]
    )

    train_df = dataframe[
        dataframe["patient_id"].isin(
            train_patients
        )
    ].copy()

    val_df = dataframe[
        dataframe["patient_id"].isin(
            val_patients
        )
    ].copy()

    print(
        "Training patients:",
        len(train_patients)
    )

    print(
        "Validation patients:",
        len(val_patients)
    )

    print(
        "Training images:",
        len(train_df)
    )

    print(
        "Validation images:",
        len(val_df)
    )

    # ========================================================
    # CLASS DISTRIBUTION
    # ========================================================

    print()
    print(
        "Training class distribution:"
    )

    print(
        train_df[
            "diagnostic"
        ].value_counts().sort_index()
    )

    print()
    print(
        "Validation class distribution:"
    )

    print(
        val_df[
            "diagnostic"
        ].value_counts().sort_index()
    )

    # ========================================================
    # DATASETS
    # ========================================================

    train_dataset = PADUFES20Dataset(
        dataframe=train_df,
        image_dir=IMAGE_ROOT,
        transform=train_transform
    )

    val_dataset = PADUFES20Dataset(
        dataframe=val_df,
        image_dir=IMAGE_ROOT,
        transform=val_transform
    )

    # ========================================================
    # DATALOADERS
    # ========================================================

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=4,
        pin_memory=True
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=4,
        pin_memory=True
    )

    # ========================================================
    # MODEL
    # ========================================================

    print()
    print(
        "Loading EfficientNet-B0..."
    )

    model = SmartphoneSkinModel(
        num_classes=6
    )

    model = model.to(
        DEVICE
    )

    # ========================================================
    # LOSS
    # ========================================================

    criterion = nn.CrossEntropyLoss()

    # ========================================================
    # OPTIMIZER
    # ========================================================

    optimizer = optim.AdamW(
        model.parameters(),
        lr=LEARNING_RATE,
        weight_decay=1e-4
    )

    # ========================================================
    # TRAINING
    # ========================================================

    best_val_accuracy = 0.0

    print()
    print("=" * 60)
    print(
        "STARTING TRAINING"
    )
    print("=" * 60)

    for epoch in range(EPOCHS):

        # ----------------------------------------------------
        # TRAIN
        # ----------------------------------------------------

        model.train()

        running_loss = 0.0

        train_correct = 0
        train_total = 0

        for images, labels in train_loader:

            images = images.to(
                DEVICE,
                non_blocking=True
            )

            labels = labels.to(
                DEVICE,
                non_blocking=True
            )

            optimizer.zero_grad()

            outputs = model(
                images
            )

            loss = criterion(
                outputs,
                labels
            )

            loss.backward()

            optimizer.step()

            running_loss += loss.item()

            predictions = outputs.argmax(
                dim=1
            )

            train_total += labels.size(0)

            train_correct += (
                predictions == labels
            ).sum().item()

        train_accuracy = (
            100.0 *
            train_correct /
            train_total
        )

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        model.eval()

        val_correct = 0
        val_total = 0

        with torch.no_grad():

            for images, labels in val_loader:

                images = images.to(
                    DEVICE,
                    non_blocking=True
                )

                labels = labels.to(
                    DEVICE,
                    non_blocking=True
                )

                outputs = model(
                    images
                )

                predictions = outputs.argmax(
                    dim=1
                )

                val_total += labels.size(0)

                val_correct += (
                    predictions == labels
                ).sum().item()

        val_accuracy = (
            100.0 *
            val_correct /
            val_total
        )

        average_loss = (
            running_loss /
            len(train_loader)
        )

        # ----------------------------------------------------
        # PRINT
        # ----------------------------------------------------

        print(
            f"Epoch {epoch + 1:02d}/{EPOCHS} | "
            f"Loss: {average_loss:.4f} | "
            f"Train: {train_accuracy:.2f}% | "
            f"Val: {val_accuracy:.2f}%"
        )

        # ----------------------------------------------------
        # SAVE BEST MODEL
        # ----------------------------------------------------

        if val_accuracy > best_val_accuracy:

            best_val_accuracy = val_accuracy

            torch.save(
                model.state_dict(),
                MODEL_PATH
            )

            print(
                "  -> Best model saved."
            )

    print()
    print("=" * 60)
    print(
        "TRAINING COMPLETE"
    )
    print("=" * 60)

    print(
        f"Best validation accuracy: "
        f"{best_val_accuracy:.2f}%"
    )

    print(
        f"Model saved to: "
        f"{MODEL_PATH}"
    )


if __name__ == "__main__":
    main()
