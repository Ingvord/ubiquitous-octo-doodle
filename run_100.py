import threading
import zmq
import time
from PIL import Image
import numpy as np
import io

# Function to simulate a single client sending an image
def client_thread(image_data, server_address, rps_counter):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(server_address)

    # Send the image data to the server
    print("Client sending image data")
    socket.send(image_data)

    # Wait for the server's response
    reply = socket.recv_json()
    print(f"Client received reply.")
    rps_counter.append(1)  # Count this request as completed

def load_image_as_bytes(image_path):
    with Image.open(image_path) as img:
        img = img.convert("L")  # Convert to grayscale if needed
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        return img_bytes.getvalue()

def run_test(image_path, server_address, num_clients=100):
    # Load the image once to reduce IO operations
    image_data = load_image_as_bytes(image_path)

    rps_counter = []

    threads = []
    for i in range(num_clients):
        thread = threading.Thread(target=client_thread, args=(image_data, server_address, rps_counter))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    return len(rps_counter)

if __name__ == "__main__":
    image_path = "random_512x512px.png"
    server_address = "tcp://localhost:5555"
    num_clients = 1  # Number of concurrent client threads

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