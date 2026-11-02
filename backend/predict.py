import sys

import torch

from PIL import Image

from torchvision import transforms

from model import SmartphoneSkinModel


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_PATH = "models/smartphone_skin_model.pth"

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# ============================================================
# CLASS INFORMATION
# ============================================================

CLASS_NAMES = [
    "Actinic Keratosis",
    "Basal Cell Carcinoma",
    "Melanoma",
    "Nevus",
    "Squamous Cell Carcinoma",
    "Seborrheic Keratosis"
]


CLASS_DESCRIPTIONS = [
    "Sun-damaged skin lesion",
    "Common type of skin cancer",
    "Serious type of skin cancer",
    "Common mole / usually non-cancerous",
    "Type of skin cancer",
    "Common non-cancerous skin growth"
]


# ============================================================
# TRANSFORM
# ============================================================

transform = transforms.Compose([

    transforms.Resize(
        (224, 224)
    ),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# ============================================================
# LOAD MODEL
# ============================================================

print("Loading model...")

model = SmartphoneSkinModel(
    num_classes=6
)

model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=DEVICE
    )
)

model = model.to(DEVICE)

model.eval()

print("Model loaded.")


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def predict_image(image_path):

    image = Image.open(
        image_path
    ).convert("RGB")

    image = transform(image)

    image = image.unsqueeze(0)

    image = image.to(DEVICE)

    with torch.no_grad():

        outputs = model(image)

        probabilities = torch.softmax(
            outputs,
            dim=1
        )

        confidence, prediction = torch.max(
            probabilities,
            dim=1
        )

    index = prediction.item()

    predicted_class = CLASS_NAMES[index]

    description = CLASS_DESCRIPTIONS[index]

    confidence = confidence.item()

    return {
        "diagnosis": predicted_class,
        "description": description,
        "confidence": confidence
    }


# ============================================================
# COMMAND LINE TEST
# ============================================================

if __name__ == "__main__":

    if len(sys.argv) < 2:

        print()
        print(
            "Usage:"
        )

        print(
            "python predict.py path/to/image.jpg"
        )

        sys.exit(1)

    image_path = sys.argv[1]

    try:

        result = predict_image(
            image_path
        )

        print()
        print("=" * 50)
        print("SKIN LESION ANALYSIS")
        print("=" * 50)

        print(
            "Prediction:",
            result["diagnosis"]
        )

        print(
            "Meaning:",
            result["description"]
        )

        print(
            "Confidence:",
            f"{result['confidence'] * 100:.2f}%"
        )

        print("=" * 50)

        print()
        print(
            "This is a research/educational model "
            "and is not a medical diagnosis."
        )

    except Exception as e:

        print()
        print(
            "Prediction failed:"
        )

        print(e)
