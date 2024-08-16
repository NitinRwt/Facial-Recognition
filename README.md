# Face Recognition System

## Overview

The Face Recognition System is a sophisticated application designed to perform real-time face recognition using a webcam. This project incorporates a variety of features, including the ability to add new faces, start and stop the recognition process, and maintain attendance logs. The interface is built using PyQt5 to ensure a professional and user-friendly experience.

## Features

- This implementation includes all the features:

1. Face recognition 
2. A modern interface with check sufficient ligthing feature
3. Home page with camera feed and capture functionality
4. Logs page to display recognised person data
5. Dark mode toggle
6. Proper error handling 
7. Added only selected user can use the system
 <br>

## Installation

### Prerequisites



- Python 3.7+
- `pip` package manager

### Dependencies

Install the required packages using pip:
```bash
pip install deep face
```
```bash
pip install opencv-python face-recognition numpy PyQt5
```
### download this file
``` bash
https://huggingface.co/RaphaelLiu/EvalCrafter-Models/resolve/main/vgg_face_weights.h5
```
### Clone the Repository

```bash
git clone https://github.com/NitinRwt/Facial-Recognition.git
cd Facial-Recognition
```

### Running the Application

```bash
python main.py
```

## File Structure

```plaintext
face-recognition-system/
├── capture_window.py    # Module for capturing images
├── data.csv             # CSV file to store attendance logs
├── img/                 # Directory to store captured images
├── main.py              # Main application file
├── stylesheet.py        # Stylesheet for the UI
└── README.md            # This README file
```

## Usage

### Adding a New Face

1. Enter the name of the person in the input field.
2. Click the "Add Face" button.
3. The system will capture the image and store it in the `img/` directory.

### Starting and Stopping Recognition

- Click the "Start Recognition" button to begin the face recognition process.
- Click the "Stop Recognition" button to halt the process.

### Viewing Attendance Logs

- Click the "Attendance Logs" button to view the attendance records.

## Customization

### Stylesheet

The visual appearance of the application can be customized by modifying the `stylesheet.py` file. This file contains the CSS-like styles used by PyQt5 to style the UI components.

### Camera Configuration

The default camera used is the system's primary webcam. This can be changed in the `recognition_loop` method of the `FaceRecognitionApp` class if a different camera is required.

## Contributing

Contributions are welcome! Please fork this repository and submit pull requests with improvements or bug fixes.


## Acknowledgements

- The [face_recognition](https://github.com/ageitgey/face_recognition) library for providing robust face detection and recognition capabilities.
- The [PyQt5](https://pypi.org/project/PyQt5/) library for creating the graphical user interface.

## Contact

For any questions or suggestions, please feel free to contact [Nitin Rawat](mailto:nitinrawat2066@gmail.com).

---
