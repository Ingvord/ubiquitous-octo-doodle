[![wakatime](https://wakatime.com/badge/user/87464ce7-a479-47b1-b3aa-2548252894d7/project/9b7651aa-41b9-4734-b7ab-cce9cbddd1c8.svg)](https://wakatime.com/badge/user/87464ce7-a479-47b1-b3aa-2548252894d7/project/9b7651aa-41b9-4734-b7ab-cce9cbddd1c8)

# Ubiquitous Octo Doodle

Welcome to the Ubiquitous Octo Doodle repository! This project is a distributed image processing service built using Python and ZeroMQ. The service accepts image files, processes them to generate histograms, and demonstrates the power of parallel processing using ZeroMQ.

The Ubiquitous Octo Doodle project is a scalable, distributed image processing service that allows multiple clients to send images to a server. The server distributes the tasks to worker processes that generate histograms of the images. This project demonstrates the usage of ZeroMQ for efficient inter-process communication in a distributed system.

## Architecture

Client: Sends images to the server using ZeroMQ REQ sockets.

Server: Acts as a broker using ZeroMQ ROUTER and DEALER sockets to forward client requests to workers and return responses.

Workers: Use ZeroMQ REP sockets to receive tasks from the server, process the images, and send the results back.

## Features

Scalable Image Processing: Easily scale the number of workers to handle a large number of concurrent client requests.

ZeroMQ Message Passing: Efficient, asynchronous communication between the server, clients, and workers using ZeroMQ sockets.

Parallel Processing: Distribute image processing tasks across multiple worker processes for improved performance.

## Getting Started
### Prerequisites

Python 3.7+ - Required for running the Python scripts.

ZeroMQ - Required for message passing between clients, server, and workers.

## Installation

Clone the repository:

```
git clone https://github.com/Ingvord/ubiquitous-octo-doodle.git
cd ubiquitous-octo-doodle
```

Install Python Dependencies:

```
pip install -r requirements.txt
```

### Running the Service

Start the Server:

Run the server to start listening for client connections and manage worker processes.

```
python server.py --workers=16
```

Run the Client:

The client sends an image to the server for processing. You can run the client as follows:

```
python client.py --image=lenna.jpeg --url=tcp://localhost:5555 --histogram=out/histogram
```

### Testing

You can simulate multiple clients to test the performance of your ZeroMQ-based service. Use the provided client script to run concurrent requests.

Run Multiple Clients Using Threads:

```
python run_100.py
```


Use the client test script to simulate multiple clients sending images concurrently.

Run Multiple Clients Using ProcessPoolExecutor:

```
python run_100_pool.py
```

### Adjust Server-Worker Communication:

Modify the ZeroMQ communication patterns in server.py and worker.py to fit your specific needs. You can explore different socket types and patterns provided by ZeroMQ.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request to contribute to this project. Ensure your changes are well-documented and tested.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
