import argparse
import numpy as np
from PIL import Image

def generate_random_image(image_path="random_512x512.png", width=512, height=512):
    # Generate random pixel values between 0 and 255
    random_data = np.random.randint(0, 256, (height, width), dtype=np.uint8)

    # Convert the numpy array to a PIL Image object
    img = Image.fromarray(random_data, 'L')

    # Save the image
    img.save(image_path)

    return img

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Random image generator.')

    parser.add_argument('--image', type=str, required=True, help='The path to the output image file')

    args = parser.parse_args()

    generate_random_image(args.image)