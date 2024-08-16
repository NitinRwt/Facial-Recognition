import sys
import cv2
import numpy as np
import face_recognition
import os
import csv
import time
from deepface import DeepFace

from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit,
    QHBoxLayout, QStatusBar, QMenuBar, QAction, QTableWidget, QTableWidgetItem, QMessageBox,
    QStackedWidget, QGroupBox, QGraphicsView, QGraphicsScene, QSizePolicy, QGridLayout,
    QScrollArea
)
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from stylesheet import get_dark_stylesheet, get_stylesheet
from anti_spoofing import detect_blinks, shape_to_np

class ClickableUserPhoto(QLabel):
    clicked = pyqtSignal(str)

    def __init__(self, user_name, image_path):
        super().__init__()
        self.user_name = user_name
        self.setPixmap(QPixmap(image_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 2px solid gray; margin: 5px;")
        self.setFixedSize(110, 110)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.user_name)

    def setSelected(self, selected):
        if selected:
            self.setStyleSheet("border: 2px solid green; margin: 5px;")
        else:
            self.setStyleSheet("border: 2px solid gray; margin: 5px;")

class FaceRecognitionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.blink_counter = 0
        self.blink_threshold = 2  # Reduced to 2 blinks
        self.blink_start_time = None
        self.blink_timeout = 5  # 5 seconds to detect required blinks
        self.verified_users = set()   
             
        self.setWindowTitle("Face Recognition System")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon("icons/app_icon.png"))

        self.allowed_users = []
        self.user_photos = {}
        self.classNames = []

        self.init_face_recognition()
        self.init_ui()
        self.init_camera()

        self.apply_stylesheet()
        self.last_attendance_time = {}
        
    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        main_layout = QHBoxLayout()
        self.central_widget.setLayout(main_layout)
    
        # Sidebar
        sidebar = QVBoxLayout()
        self.home_btn = QPushButton(QIcon("icons/home.png"), "Home")
        self.logs_btn = QPushButton(QIcon("icons/logs.png"), "Logs")
        self.settings_btn = QPushButton(QIcon("icons/settings.png"), "Settings")
        
        sidebar.addWidget(self.home_btn)
        sidebar.addWidget(self.logs_btn)
        sidebar.addWidget(self.settings_btn)
        sidebar.addStretch()
    
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar)
        sidebar_widget.setFixedWidth(200)
    
        # Main content
        self.stacked_widget = QStackedWidget()
        
        # Home page
        home_page = QWidget()
        home_layout = QVBoxLayout()
        
        self.date_time_label = QLabel()
        self.date_time_label.setAlignment(Qt.AlignCenter)
        
        self.graphics_view = QGraphicsView()
        self.graphics_scene = QGraphicsScene()
        self.graphics_view.setScene(self.graphics_scene)
        self.graphics_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        input_group = QGroupBox("Capture")
        input_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        self.capture_button = QPushButton("Capture Photo")
        self.capture_button.setIcon(QIcon("icons/camera.png"))
        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.capture_button)
        input_group.setLayout(input_layout)
    
        # User selection area
        self.allowed_users_group = QGroupBox("Select Users")
        self.allowed_users_layout = QGridLayout()
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.allowed_users_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        allowed_users_main_layout = QVBoxLayout()
        allowed_users_main_layout.addWidget(scroll_area)
        self.allowed_users_group.setLayout(allowed_users_main_layout)
        self.allowed_users_group.setFixedHeight(200)  # Set fixed height to make it smaller
    
        home_layout.addWidget(self.date_time_label)
        home_layout.addWidget(self.graphics_view)
        home_layout.addWidget(input_group)
        home_layout.addWidget(self.allowed_users_group)
        
        home_page.setLayout(home_layout)
        
        # Logs page
        self.logs_page = QWidget()
        logs_layout = QVBoxLayout()
        self.table_widget = QTableWidget()
        logs_layout.addWidget(self.table_widget)
        self.logs_page.setLayout(logs_layout)
        
        # Add pages to stacked widget
        self.stacked_widget.addWidget(home_page)
        self.stacked_widget.addWidget(self.logs_page)
    
        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(self.stacked_widget)
    
        # Connect signals
        self.home_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.logs_btn.clicked.connect(self.show_logs)
        self.capture_button.clicked.connect(self.capture_photo)
    
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
    
        # Menu bar
        self.menu_bar = QMenuBar()
        self.setMenuBar(self.menu_bar)
        
        file_menu = self.menu_bar.addMenu("File")
        help_menu = self.menu_bar.addMenu("Help")
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
    
        # Date and time update
        self.date_time_timer = QTimer()
        self.date_time_timer.timeout.connect(self.update_date_time)
        self.date_time_timer.start(1000)
    
        self.update_allowed_users_list()
        
    def init_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)

    def init_face_recognition(self):
        self.path = 'test_images'
        self.images = []
        self.classNames = []
        self.load_images()
        # Initialize the DeepFace model with VGG-Face weights
        self.model = DeepFace.build_model("VGG-Face")
        self.model.load_weights("vgg_face_weight.h5")
        print('VGG-Face model loaded')

    
    def load_images(self):
        myList = os.listdir(self.path)
        for cl in myList:
            curImg = cv2.imread(f'{self.path}/{cl}')
            self.images.append(curImg)
            self.classNames.append(os.path.splitext(cl)[0])

    def check_lighting(self, img, threshold=100):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        avg_brightness = np.mean(gray)
        return avg_brightness >= threshold, avg_brightness

    def update_allowed_users_list(self):
        for i in reversed(range(self.allowed_users_layout.count())): 
            widget = self.allowed_users_layout.itemAt(i).widget()
            if widget is not None: 
                widget.setParent(None)
        
        for i, className in enumerate(self.classNames):
            image_path = f'{self.path}/{className}.jpg'
            user_photo = ClickableUserPhoto(className, image_path)
            user_photo.clicked.connect(self.toggle_user_selection)
            user_photo.setSelected(className in self.allowed_users)
            self.user_photos[className] = user_photo
            self.allowed_users_layout.addWidget(user_photo, i // 4, i % 4)

    def toggle_user_selection(self, user_name):
        if user_name in self.allowed_users:
            self.allowed_users.remove(user_name)
            self.user_photos[user_name].setSelected(False)
        else:
            self.allowed_users.append(user_name)
            self.user_photos[user_name].setSelected(True)
        print("Allowed users:", self.allowed_users)

    def update_date_time(self):
        current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.date_time_label.setText(current_date_time)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        lighting_ok, brightness = self.check_lighting(frame)
        
        if not lighting_ok:
            self.status_bar.showMessage(f"Lighting too low: {brightness:.2f}")
            return

        faces = face_recognition.face_locations(rgb_frame)
        encodings = face_recognition.face_encodings(rgb_frame, faces)
        for face_encoding, (top, right, bottom, left) in zip(encodings, faces):
            matches = face_recognition.compare_faces(self.encodeListKnown, face_encoding)
            face_distances = face_recognition.face_distance(self.encodeListKnown, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.classNames[best_match_index].upper()
                if name in self.allowed_users:
                    if name not in self.last_attendance_time or (datetime.now() - self.last_attendance_time[name]).total_seconds() > 60:
                        self.mark_attendance(name)
                        self.last_attendance_time[name] = datetime.now()
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                else:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.putText(frame, "Unauthorized", (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            else:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, "Unknown", (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                
            # Verify user's presence
            if name in self.allowed_users:
                if self.blink_start_time is None:
                    self.blink_start_time = time.time()
                self.blink_counter += 1

                if self.blink_counter >= self.blink_threshold:
                    blink_duration = time.time() - self.blink_start_time
                    if blink_duration <= self.blink_timeout:
                        self.verified_users.add(name)
                        self.blink_counter = 0
                        self.blink_start_time = None
                        self.status_bar.showMessage(f"{name} verified!")
                    else:
                        self.blink_counter = 0
                        self.blink_start_time = None
            else:
                self.blink_counter = 0
                self.blink_start_time = None
                        
        qimg = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.graphics_scene.clear()
        self.graphics_scene.addPixmap(QPixmap.fromImage(qimg))
    
    def show_logs(self):
        self.stacked_widget.setCurrentIndex(1)
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Name", "Date", "Time"])
        
        with open('attendance.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)
            rows = list(reader)
        
        self.table_widget.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, cell in enumerate(row):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(cell))
                
    def capture_photo(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Warning", "Please enter a name")
            return

        ret, frame = self.cap.read()
        if not ret:
            QMessageBox.warning(self, "Warning", "Failed to capture photo")
            return
        
        frame = cv2.flip(frame, 1)
        cv2.imwrite(f"{self.path}/{name}.jpg", frame)
        self.status_bar.showMessage(f"Photo captured for {name}")
        
        self.load_images()
        self.update_allowed_users_list()
        self.encodeListKnown = [face_recognition.face_encodings(img)[0] for img in self.images]
        
    def mark_attendance(self, name):
        with open('attendance.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M:%S")
            writer.writerow([name, date_str, time_str])
            self.status_bar.showMessage(f"Attendance marked for {name}")

    def show_about_dialog(self):
        QMessageBox.about(self, "About", "Face Recognition System v1.0\nDeveloped by OpenAI")

    def closeEvent(self, event):
        self.cap.release()
        super().closeEvent(event)
        
    def apply_stylesheet(self):
        self.setStyleSheet(get_dark_stylesheet())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FaceRecognitionApp()
    window.show()
    sys.exit(app.exec_())
