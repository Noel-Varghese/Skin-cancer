import torch.nn as nn

from torchvision.models import (
    efficientnet_b0,
    EfficientNet_B0_Weights
)


class SmartphoneSkinModel(nn.Module):

    def __init__(self, num_classes=6):

        super().__init__()

        self.backbone = efficientnet_b0(
            weights=EfficientNet_B0_Weights.DEFAULT
        )

        num_features = (
            self.backbone.classifier[1].in_features
        )

        self.backbone.classifier[1] = nn.Linear(
            num_features,
            num_classes
        )

    def forward(self, x):

        return self.backbone(x)
