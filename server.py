import zmq
import multiprocessing
import numpy as np

def process_image_data(image_data_bytes, shape):
    # Convert bytes back to numpy array
    img_array = np.frombuffer(image_data_bytes, dtype=np.uint8).reshape(shape)
    # Example: Calculate histogram
    histogram = np.histogram(img_array, bins=256)[0]
    return histogram

def worker(worker_id, server_address):
    print(f"Worker {worker_id} is starting.")
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(server_address)

    # Send a ready signal to the server
    socket.send_json({"worker_id": worker_id, "status": "ready"})
    print(f"Worker {worker_id} is ready.")

    print("Starting worker loop")
    while True:
        # Wait for a job from the server
        image_data_bytes = socket.recv()
        print("Got bytes")
        # Example shape, replace with actual dimensions passed as metadata if needed
        shape = (225, 225)

        # Process the image data
        result = process_image_data(image_data_bytes, shape)

        # Send the result back to the server
        socket.send_pyobj(result)

def server():
    context = zmq.Context.instance()
    frontend = context.socket(zmq.ROUTER)
    frontend.bind("tcp://*:5555")

    backend = context.socket(zmq.DEALER)
    backend.bind("ipc://backend")

    # Start workers
    worker_count = 4  # Adjust based on your system's cores and needs
    for i in range(worker_count):
        multiprocessing.Process(target=worker, args=(i, "ipc://backend")).start()

    zmq.proxy(frontend, backend)

    frontend.close()
    backend.close()
    context.term()

if __name__ == "__main__":
    server()
