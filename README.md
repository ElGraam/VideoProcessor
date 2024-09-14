# VideoProcessor

VideoProcessor is a client-server application for uploading and processing MP4 video files. The server efficiently handles multiple client connections and file operations using Python's asyncio and aiofile libraries. The client is a command-line tool that allows users to upload MP4 files to the server.

## Features

- MP4 file upload from client to server
- File format validation before upload
- Progress bar display during file upload
- Server-side available disk space check before accepting files
- Uploaded files saved on the server with unique filenames
- Status messages sent from server to client indicating upload success or failure
- Server logging of critical events and errors
- Server support for multiple client connections using multiprocessing

## Requirements

- Python 3.9 or higher
- aiofile library
- tqdm library

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/LuxGram/VideoProcessor.git
   ```

2. Install the required libraries:
   ```bash
   pip install aiofile tqdm
   ```

## Usage

### Server

1. Navigate to the server directory:
   ```bash
   cd VideoProcessor
   ```

2. Start the server:
   ```bash
   python3 server.py
   ```

   The default port number for the server is 65432. You can specify a different port:

   ```bash
   python3 server.py --port 65432
   ```

   The server will start listening on the specified port.

### Client

1. Navigate to the client directory:
   ```bash
   cd VideoProcessor
   ```

2. Run the client:
   ```bash
   python3 client.py path/to/video.mp4
   ```

   Replace `path/to/video.mp4` with the actual path to the MP4 file you want to upload.

   The client will connect to the server, upload the file, and display a progress bar. Once the upload is complete, the server will send a status message indicating the success or failure of the upload.

## Configuration

- `SERVER_HOST`: Hostname or IP address of the server (default: 'localhost')
- `SERVER_PORT`: Port number the server listens on (default: 65432)
- `BUFFER_SIZE`: Size of the buffer used for file transfer (default: 1400 bytes)
- `TIMEOUT`: Timeout for client connections (default: 10 seconds)
- `STORAGE_DIR`: Directory where the server stores uploaded files (default: './uploads')

