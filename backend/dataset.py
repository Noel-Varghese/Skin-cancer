import pandas as pd

from PIL import Image
from torch.utils.data import Dataset


class PADUFES20Dataset(Dataset):

    CLASS_NAMES = [
        "Actinic Keratosis",
        "Basal Cell Carcinoma",
        "Melanoma",
        "Nevus",
        "Squamous Cell Carcinoma",
        "Seborrheic Keratosis"
    ]

    LABEL_MAP = {
        "ACK": 0,
        "BCC": 1,
        "MEL": 2,
        "NEV": 3,
        "SCC": 4,
        "SEK": 5
    }

    def __init__(
        self,
        dataframe,
        image_dir=None,
        transform=None
    ):

        self.data = dataframe.reset_index(
            drop=True
        )

        self.transform = transform

    def __len__(self):

        return len(
            self.data
        )

    def __getitem__(self, index):

        row = self.data.iloc[index]

        image_path = row["image_path"]

        image = Image.open(
            image_path
        ).convert("RGB")

        label = self.LABEL_MAP[
            row["diagnostic"]
        ]

        if self.transform:

            image = self.transform(
                image
            )

        return image, label
