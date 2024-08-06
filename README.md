# Face Recognition System

## Overview

The Face Recognition System is a sophisticated application designed to perform real-time face recognition using a webcam. This project incorporates a variety of features, including the ability to add new faces, start and stop the recognition process, and maintain attendance logs. The interface is built using PyQt5 to ensure a professional and user-friendly experience.

## Features

- **Add Face**: Capture and add a new face to the system.
- **Start Recognition**: Begin the face recognition process using the webcam.
- **Stop Recognition**: Halt the face recognition process.
- **About**: View information about the application.
- **Attendance Logs**: View and manage attendance records.
- **Responsive UI**: Built with PyQt5, the interface is designed to be responsive and visually appealing.
- **Real-time Face Recognition**: Utilizes the `face_recognition` library for accurate and efficient face detection and recognition.
- **CSV Attendance Logging**: Logs attendance data to a CSV file with timestamps. <br>
![Screenshot 2024-08-03 111428](https://github.com/user-attachments/assets/cea365d0-e3fa-4f4d-83a8-c01f67ff93b8)

## Installation

### Prerequisites



- Python 3.7+
- `pip` package manager

### Dependencies

Install the required packages using pip:

```bash
pip install opencv-python face-recognition numpy PyQt5
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
