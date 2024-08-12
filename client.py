import argparse
from PIL import Image
import zmq
import numpy as np
import io
import termplotlib as tpl
import matplotlib.pyplot as plt

def read_image_file(filepath):
    # Open the image file
    with Image.open(filepath) as img:
        # Convert the image to grayscale (if needed) and then to a numpy array
        img_array = np.array(img.convert("L"))
    return img_array

def show_histogram_plot(histogram_data):
    bins = np.arange(len(histogram_data))

    # Create a plot
    fig = tpl.figure()
    fig.hist(histogram_data, bins, orientation='vertical', force_ascii=False)
    fig.show()

def save_histogram_plot(histogram_data, output_path="histogram_plot.png"):
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(histogram_data)), histogram_data, color='blue')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.title('Histogram of Image')
    plt.savefig(output_path)
    plt.close()
    print(f"Histogram plot saved to {output_path}")

async def main(filepath, server_url, histogram_path):
    # Initialize ZeroMQ context and socket
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(server_url)

    image = Image.open(filepath)

    # Read the 2D image data
    img_data = np.array(image.convert("L"))

    # Serialize the image data
    # For example, converting numpy array to bytes
    img_bytes = img_data.tobytes()

    # Send the image data to the server
    socket.send(img_bytes)

    # Receive the response from the server
    histogram = socket.recv_pyobj()

    show_histogram_plot(histogram)

    save_histogram_plot(histogram, histogram_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Client to send an image file to the server.')
    parser.add_argument('--image', type=str, required=True, help='The path to the image file')
    parser.add_argument('--url', type=str, required=True, help='URL of the processing endpoint')
    parser.add_argument('--histogram', type=str, required=True, help='The path to the output histogram file')

    # Parse the arguments
    print("Parsing arguments...")
    args = parser.parse_args()
    url = args.url
    image_path = args.image
    histogram_path = args.histogram
    print("Done.")



    # Call the main function with the image path
    main(image_path, url, histogram_path)
