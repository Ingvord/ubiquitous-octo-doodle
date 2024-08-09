import argparse
from PIL import Image
import zmq
import numpy as np
import io

def read_image_file(filepath):
    # Open the image file
    with Image.open(filepath) as img:
        # Convert the image to grayscale (if needed) and then to a numpy array
        img_array = np.array(img.convert("L"))
    return img_array

def main(filepath):
    # Initialize ZeroMQ context and socket
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    # Read the 2D image data
    img_data = read_image_file(filepath)

    # Serialize the image data
    # For example, converting numpy array to bytes
    img_bytes = img_data.tobytes()

    # Send the image data to the server
    socket.send(img_bytes)

    # Receive the response from the server
    histogram = socket.recv_pyobj()
    print("Received Histogram:", histogram)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Client to send an image file to the server.')
    parser.add_argument('--image', type=str, required=True, help='The path to the image file')

    # Parse the arguments
    args = parser.parse_args()

    # Call the main function with the image path
    main(args.image)
