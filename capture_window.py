import cv2
import os
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QHBoxLayout, QStatusBar
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtCore import QTimer, Qt, pyqtSignal

import cv2
import os
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QHBoxLayout, QStatusBar
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtCore import QTimer, Qt, pyqtSignal

class CaptureWindow(QMainWindow):
    face_captured = pyqtSignal(str, str)  # Signal to inform main window about the new face

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Capture Photo")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("path/to/icon.png"))

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.captured_image_label = QLabel(self)
        self.captured_image_label.setAlignment(Qt.AlignCenter)

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter your name")

        self.capture_button = QPushButton("Capture Photo", self)
        self.capture_button.setIcon(QIcon("path/to/capture_icon.png"))
        self.capture_button.clicked.connect(self.capture_photo)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.name_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.capture_button)
        self.layout.addLayout(button_layout)

        self.layout.addWidget(self.captured_image_label)

        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)

        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

    def capture_photo(self):
        success, img = self.cap.read()
        if success:
            name = self.name_input.text().strip()
            if name:
                img_path = os.path.join('test_images', f"{name}.jpg")
                cv2.imwrite(img_path, img)
                self.status_bar.showMessage(f"Photo captured and saved as {img_path}", 5000)

                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                qformat = QImage.Format_RGB888
                captured_img = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
                captured_img = captured_img.rgbSwapped()
                self.captured_image_label.setPixmap(QPixmap.fromImage(captured_img))
                self.captured_image_label.setScaledContents(True)

                self.face_captured.emit(name, img_path)  # Emit signal to inform main window
            else:
                self.status_bar.showMessage("Name cannot be empty", 5000)

    def update_frame(self):
        success, img = self.cap.read()
        if success:
            qformat = QImage.Format_RGB888
            img = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
            img = img.rgbSwapped()
            self.image_label.setPixmap(QPixmap.fromImage(img))
            self.image_label.setScaledContents(True)

    def closeEvent(self, event):
        self.cap.release()
        event.accept()
