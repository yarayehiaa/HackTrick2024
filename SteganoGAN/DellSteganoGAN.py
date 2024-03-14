from utils import *
import numpy as np
import torch
from torchvision import transforms
from PIL import Image
from decoders import DenseDecoder


def stegano_solver() -> str:
    input_image_path = "SteganoGAN\sample_example\encoded.png"
    input_image = Image.open(input_image_path).convert("RGB")
    H, W = 256, 256

    # Preprocess the image
    transform = transforms.Compose([
    transforms.Resize((H, W)),  # Resize to match the model's input size
    transforms.ToTensor(),       # Convert to tensor
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize
    ])
    input_tensor = transform(input_image).unsqueeze(0)  # Add batch dimension

    # Instantiate the decoder
    data_depth = 5  # Example depth, adjust as needed
    hidden_size = 64  # Example hidden size, adjust as needed
    decoder = DenseDecoder(data_depth, hidden_size)

    # Decode the image
    with torch.no_grad():
        output_tensor = decoder(input_tensor)

    # Convert the output tensor to a numpy array
    output_array = output_tensor.squeeze(0).numpy()
    print(output_array)

    # Assuming the text is encoded as integers, convert them to characters
    text = "".join([(int(value)) for value in output_array.flatten()])

  
    print("The decoded message is: ", text)
    
stegano_solver()