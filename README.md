# FastAPI Object Detection and Image Processing

This repository contains a FastAPI application that demonstrates object detection using YOLOv5 and various image processing functionalities. The application provides endpoints to perform object detection, draw bounding boxes on images, convert images to base64, and more.

## Table of Contents

- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Usage](#usage)
  - [Object Detection and JSON Result](#object-detection-and-json-result)
  - [Object Detection and Image with Bounding Boxes](#object-detection-and-image-with-bounding-boxes)
  - [Image Conversion](#image-conversion)
  - [Image Decoding and Bounding Boxes](#image-decoding-and-bounding-boxes)
- [Contributing](#contributing)

## Getting Started

### Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/fastapi-object-detection/fastapi-object-detection.git
   cd fastapi-object-detection
## running the application
1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
3. Running the Application
To run the FastAPI application, execute the following command:
```bash
uvicorn main:app --reload
```
The application will start, and you can access the Swagger documentation at http://localhost:8000/docs to explore and test the available endpoints.

## Usage
### Object Detection and JSON Result
Send an image file to the /object-to-json endpoint to perform object detection and receive JSON results containing detected object information.

### Object Detection and Image with Bounding Boxes
Use the /object-to-img endpoint to perform object detection and receive an image with bounding boxes drawn around detected objects.

### Image Conversion
The /convert_image endpoint converts an image file to a base64-encoded string and returns it as JSON.

### Image Decoding and Bounding Boxes
The /decode_image endpoint accepts an image file and a JSON file containing bounding box information. It decodes the image, draws bounding boxes on it, and returns the modified image.

## Contributing
Contributions to this repository are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.
