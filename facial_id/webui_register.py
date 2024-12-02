import sys
import cv2
import mediapipe as mp
import time
import json
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QLineEdit, QFormLayout
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from face_mesh import draw_landmarks_on_camera


# Worker Thread for capturing video feed
class VideoCaptureThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                continue

            # Convert the frame to RGB
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert it to QImage
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # Emit the signal with the new image
            self.change_pixmap_signal.emit(q_image)

    def stop(self):
        self.cap.release()
        self.quit()


# Main Window for the PyQt UI
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Facial Registration and Verification')

        # Allow the window to be resizable by setting minimum size (optional)
        self.setMinimumSize(400, 300)

        # Set layout for the window
        self.layout = QVBoxLayout()

        # Add a label for instructions
        self.instruction_label = QLabel('Fill out the form and click "Register" or "Verify" to start the process.', self)
        self.layout.addWidget(self.instruction_label)

        # Create the form layout for input fields
        self.form_layout = QFormLayout()

        # Input fields for campusID, name, email, and department
        self.campus_id_input = QLineEdit(self)
        self.name_input = QLineEdit(self)
        self.email_input = QLineEdit(self)
        self.department_input = QLineEdit(self)

        self.form_layout.addRow('Campus ID:', self.campus_id_input)
        self.form_layout.addRow('Name:', self.name_input)
        self.form_layout.addRow('Email:', self.email_input)
        self.form_layout.addRow('Department:', self.department_input)

        # Add the form layout to the main layout
        self.layout.addLayout(self.form_layout)

        # Video feed display label
        self.video_label = QLabel(self)
        self.layout.addWidget(self.video_label)

        # Register button
        self.register_button = QPushButton('Register', self)
        self.register_button.clicked.connect(self.register_face)
        self.layout.addWidget(self.register_button)

        # Verify button
        self.verify_button = QPushButton('Verify', self)
        self.verify_button.clicked.connect(self.verify_face)
        self.layout.addWidget(self.verify_button)

        # Set the layout of the window
        self.setLayout(self.layout)

        # Start the video capture thread
        self.thread = VideoCaptureThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    def update_image(self, q_image):
        self.video_label.setPixmap(QPixmap.fromImage(q_image))

    def register_face(self):
        form_data = self.get_form_data()
        print(form_data)
        campus_id = self.campus_id_input.text()
        if not campus_id:
            QMessageBox.warning(self, "Input Error", "Please enter your Campus ID.")
            return

        # Display instruction only during registration
        self.instruction_label.setText(f"Registration in progress for {campus_id}. Please look at the camera.")

        # Call your function to capture the image for registration
        output_path = f"{campus_id}_registered_face.jpg"
        draw_landmarks_on_camera(countdown=5, output_path=output_path, task="registration")

        # Save form data to a file
        self.save_form_data(form_data)

        QMessageBox.information(self, "Registration", "Registration Completed!")
        self.instruction_label.setText(f"Registration completed for {campus_id}. You can now verify your face.")

    def verify_face(self):
        # Display instruction only during verification
        self.instruction_label.setText(f"Verification in progress. Please look at the camera.")

        # Call your function to capture the image for verification
        output_path = f"verified_face.jpg"
        draw_landmarks_on_camera(countdown=5, output_path=output_path, task="verification")

        QMessageBox.information(self, "Verification", "Verification Completed!")
        self.instruction_label.setText(f"Verification completed. You can now try again or exit.")

    def save_form_data(self, form_data):
        """
        Save the form data to a JSON file.
        """
        file_name = "form_data.json"

        # Check if the file exists and load existing data
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                existing_data = json.load(file)
        else:
            existing_data = []

        # Append the new form data
        existing_data.append(form_data)

        # Save back to the file
        with open(file_name, "w") as file:
            json.dump(existing_data, file, indent=4)

    def get_form_data(self):
        # Create a dictionary with the form input values
        form_data = {
            'Campus ID': self.campus_id_input.text(),
            'Name': self.name_input.text(),
            'Email': self.email_input.text(),
            'Department': self.department_input.text()
        }
        return form_data

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
