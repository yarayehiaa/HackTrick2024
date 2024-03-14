import torch
from torch import nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image


class BasicCritic(nn.Module):
    """
    The BasicCritic module takes an image and predicts whether it is a cover
    image or a steganographic image (N, 1).

    Input: (N, 3, H, W)
    Output: (N, 1)
    """
    def _name(self):
        return "BasicCritic"

    def _conv2d(self, in_channels, out_channels):
        return nn.Conv2d(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=3
        )

    def _build_models(self):
        self.conv1 = nn.Sequential(
            self._conv2d(3, self.hidden_size),
            nn.LeakyReLU(inplace=True),
            nn.BatchNorm2d(self.hidden_size),
        )
        self.conv2 = nn.Sequential(
            self._conv2d(self.hidden_size, self.hidden_size),
            nn.LeakyReLU(inplace=True),
            nn.BatchNorm2d(self.hidden_size),
        )
        self.conv3 = nn.Sequential(
            self._conv2d(self.hidden_size, self.hidden_size),
            nn.LeakyReLU(inplace=True),
            nn.BatchNorm2d(self.hidden_size),
        )  
        self.conv4 = nn.Sequential(
            self._conv2d(self.hidden_size, 1)
        )         

        return self.conv1, self.conv2, self.conv3, self.conv4

    def __init__(self, hidden_size):
        super().__init__()
        self.hidden_size = hidden_size
        self._models = self._build_models()
        self.name = self._name()

    def forward(self, image):
        x = self._models[0](image)
        x_1 = self._models[1](x)
        x_2 = self._models[2](x_1)
        x_3 = self._models[3](x_2)
        return torch.mean(x_3.view(x_3.size(0), -1), dim=1)
    
    
    
""" hidden_size = 64  # Example hidden size, adjust as needed
critic = BasicCritic(hidden_size)

# Generate example images (you can replace these with actual images)
transform = transforms.Compose([
    transforms.Resize((256, 256)),  # Resize to match the model's input size
    transforms.ToTensor(),           # Convert to tensor
])

# Load the example cover and steganographic images
#cover_image_path = "path_to_cover_image.jpg"
steganographic_image_path = "SteganoGAN\sample_example\encoded.png"
#cover_image = transform(Image.open(cover_image_path).convert("RGB")).unsqueeze(0)
steganographic_image = transform(Image.open(steganographic_image_path).convert("B")).unsqueeze(0)

# Classify the images using the critic
critic.eval()  # Set the critic to evaluation mode
#cover_classification = critic(cover_image)
steganographic_classification = critic(steganographic_image)

# Print the classification results
#print("Cover Image Classification:", cover_classification.item())
print("Steganographic Image Classification:", steganographic_classification.item()) """