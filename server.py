from time import sleep

import zmq
import multiprocessing
import threading
import numpy as np

def process_image_data(image_data_bytes):
    # Convert bytes back to numpy array
    img_array = np.frombuffer(image_data_bytes, dtype=np.uint8)
    # Example: Calculate histogram
    histogram = np.histogram(img_array, bins=512)[0]
    return histogram

def worker(worker_id, server_address):
    print(f"Worker {worker_id} is starting.")
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    print(f"Worker {worker_id} is connecting to {server_address}")
    socket.connect(server_address)

    # Send a ready signal to the server
    # socket.send_json({"worker_id": worker_id, "status": "ready"})
    print(f"Worker {worker_id} is ready.")


    sleep(1)
    print(f"Starting worker loop {worker_id}")
    #socket.send_json({"worker_id": worker_id, "status": "ready"})
    try:
        while True:
            # Wait for a job from the server
            image_data_bytes = socket.recv()
            print("Got bytes")
            # Process the image data
            result = process_image_data(image_data_bytes)

            # Send the result back to the server
            socket.send_pyobj(result)
    finally:
        socket.close()
        context.term()

def peer_run(ctx, capture_server):
    """ this is the run method of the PAIR thread that logs the messages
    going through the broker """
    sock = ctx.socket(zmq.PAIR)
    sock.connect(capture_server) # connect to the caller
    sock.send(b"") # signal the caller that we are ready
    while True:
        try:
            topic = sock.recv_string()
            obj = sock.recv_pyobj()
        except Exception:
            topic = None
            obj = sock.recv()
        print(f"\n !!! peer_run captured message with topic {topic}, obj {obj}. !!!\n")

def server():
    context = zmq.Context.instance()
    cap = context.socket(zmq.PAIR)
    cap.bind("inproc://capture")
    cap_th = threading.Thread(target=peer_run, args=(context, "inproc://capture"), daemon=True)
    cap_th.start()
    cap.recv() # wait for signal from peer thread

    frontend = context.socket(zmq.ROUTER)
    frontend.bind("tcp://*:5555")

    backend = context.socket(zmq.DEALER)
    backend.bind("ipc://backend")

    # Start workers
    worker_count = 16  # Adjust based on your system's cores and needs
    for i in range(worker_count):
        multiprocessing.Process(target=worker, args=(i, "ipc://backend")).start()

    try:
        zmq.proxy(frontend, backend)
    finally:
        frontend.close()
        backend.close()
        context.term()



if __name__ == "__main__":
    server()
