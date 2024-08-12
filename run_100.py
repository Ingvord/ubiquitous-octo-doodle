import threading
from concurrent.futures import ProcessPoolExecutor

import zmq
import time
from PIL import Image
import numpy as np
import io

# Function to simulate a single client sending an image
def client_thread(image_data, server_address):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(server_address)

    rps_counter = []

    for i in range(100):
        # Send the image data to the server
        print("Client sending image data")
        socket.send(image_data)

        # Wait for the server's response
        reply = socket.recv_pyobj()
        print(f"Client received reply.")
        rps_counter.append(1)  # Count this request as completed

    socket.close()

    return len(rps_counter)


def load_image_as_bytes(image_path):
    with Image.open(image_path) as img:
        img = img.convert("L")  # Convert to grayscale if needed
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        return img_bytes.getvalue()

def run_test(image_path, server_address, num_clients=100):
    image = Image.open(image_path)

    # Read the 2D image data
    img_data = np.array(image.convert("L"))

    # Serialize the image data
    # For example, converting numpy array to bytes
    img_bytes = img_data.tobytes()
    # Load the image once to reduce IO operations

    # Use ProcessPoolExecutor to manage multiple client processes
    with ProcessPoolExecutor(max_workers=num_clients) as executor:
        futures = [executor.submit(client_thread, img_bytes, server_address) for _ in range(num_clients)]
        results = [future.result() for future in futures]

    return len(results) * 100 # if there is no error we expect each array element to have 100 nested elements, see rps_counter

if __name__ == "__main__":
    image_path = "random_512x512.png"
    server_address = "tcp://localhost:5555"
    num_clients = 100  # Number of concurrent client threads

    start_time = time.time()
    completed_requests = run_test(image_path, server_address, num_clients)
    end_time = time.time()

    print(f"Test completed in {end_time - start_time} seconds.")

    # Calculate and print RPS
    total_time = end_time - start_time
    rps = completed_requests / total_time
    print(f"Test completed in {total_time:.2f} seconds.")
    print(f"Total Requests Completed: {completed_requests}")
    print(f"Requests Per Second (RPS): {rps:.2f}")