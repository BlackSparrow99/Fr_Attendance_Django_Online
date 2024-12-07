import cv2
import numpy as np
import face_recognition
import os
import pickle
import threading
from datetime import datetime
from django.conf import settings
import sys


class FaceRecognitionAttendance:
    def __init__(self, classroom_id):
        self.classroom_id = classroom_id

        self.attendance_path = os.path.join(settings.MEDIA_ROOT, "Attendance", classroom_id)
        self.dataset_path = os.path.join(settings.MEDIA_ROOT, "Data_set", "Face_recognition")
        self.encoded_file = os.path.join(settings.MEDIA_ROOT, "Data_set", "Face_recognition", "encoded_faces.pkl")

        self.encoded_list = []
        self.classNames = []

        # Ensure dataset folder exists
        if not os.path.exists(self.dataset_path):
            os.makedirs(self.dataset_path, exist_ok=True)
            sys.exit("Dataset directory created. Please add face data.")
        elif not os.listdir(self.dataset_path):
            sys.exit("Dataset directory is empty. Please add face data.")
        else:
            print("\tFace data found in the directory.")

        # Ensure classroom attendance directory exists
        os.makedirs(self.attendance_path, exist_ok=True)

    def load_or_create_encodings(self):
        if os.path.exists(self.encoded_file):
            # Load the encodings and class names from the file
            with open(self.encoded_file, 'rb') as file:
                self.encoded_list, self.classNames = pickle.load(file)
            print("\tLoaded encodings from file.")
        else:
            # If file does not exist, create encodings from images in the dataset
            images, self.classNames = [], []
            for element in os.listdir(self.dataset_path):
                if element.endswith(("jpg", "jpeg")):
                    img = cv2.imread(os.path.join(self.dataset_path, element))
                    images.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                    self.classNames.append(element.split("_")[0])

            # Encode faces from images
            self.encoded_list = [face_recognition.face_encodings(img)[0] for img in images]

            # Save encodings to file
            with open(self.encoded_file, 'wb') as file:
                pickle.dump((self.encoded_list, self.classNames), file)
            print("\tEncodings created and saved.")

    def record_attendance(self, name):
        from .views import record_attendance_in_CSV, record_attendance_in_database  # Local import

        student_id = name
        classroom_id = self.classroom_id
        status = "Present"

        # Record attendance in CSV file (your existing logic)
        record_attendance_in_CSV(student_id, classroom_id)

        # Record attendance in the database
        attendance_record = record_attendance_in_database(student_id, classroom_id, status)

        # Provide feedback to the user
        if attendance_record[0]:
            print("Success", attendance_record[1])
        else:
            print("Info", attendance_record[1])

    def threaded_attendance(self, name):
        if name != "Unknown Person":
            threading.Thread(target=self.record_attendance, args=(name,)).start()

    @staticmethod
    def render_distance(value):
        """Control face distance rendering for visual feedback."""
        if value == "close":
            return 0.25, 4
        elif value == "mid":
            return 0.5, 2
        return 1, 1

    def start_recognition(self, q_lty, mup, frame_skip=3):
        capture_video = cv2.VideoCapture(0)
        frame_count = 0

        while True:
            success, img_original = capture_video.read()
            if not success:
                break

            frame_count += 1
            if frame_count % frame_skip != 0:
                continue

            img_resized = cv2.resize(img_original, (0, 0), None, q_lty, q_lty)
            img_resized = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(img_resized)
            encode_faces = face_recognition.face_encodings(img_resized, face_locations)

            for face_location, encode_face in zip(face_locations, encode_faces):
                matches = face_recognition.compare_faces(self.encoded_list, encode_face, tolerance=0.5)
                face_distances = face_recognition.face_distance(self.encoded_list, encode_face)
                match_index = np.argmin(face_distances)

                if matches[match_index] and face_distances[match_index] < 0.5:
                    name = self.classNames[match_index]
                    self.threaded_attendance(name)
                else:
                    name = "Unknown Person"

                y1, x2, y2, x1 = [coord * mup for coord in face_location]
                cv2.rectangle(img_original, (x1, y1), (x2, y2), (0, 0, 255), 1)
                cv2.rectangle(img_original, (x1, y2 + 35), (x2, y2), (0, 0, 0), cv2.FILLED)
                cv2.putText(img_original, name, (x1 + 6, y2 + 14), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

                if name != "Unknown Person":
                    cv2.putText(img_original, f"{round(face_distances[match_index], 10)}", (x1 + 6, y2 + 28),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

            _, jpeg = cv2.imencode('.jpg', img_original)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        capture_video.release()
        cv2.destroyAllWindows()
