#################################################
# This is the source code for recognizing face #
###############################################

import cv2
import numpy as np
import face_recognition
import os
import pickle
import threading
import keyboard
from datetime import datetime
import sys


class FaceRecognitionAttendance:
    def __init__(self, dataset_path, attendance_path):
        self.dataset_path = dataset_path
        self.attendance_path = attendance_path
        encoded_file = dataset_path+"encoded_faces.pkl"
        self.encoded_file = encoded_file
        self.encoded_list = []
        self.classNames = []

        print("\n")
        # Ensure attendance folder exists
        if os.path.exists(self.dataset_path):
            if not os.listdir(self.dataset_path):
                print("\tPlease add face data to the directory to use face recognition.")
                sys.exit("\tExiting program. Dataset directory created.")
            else:
                print("\tFace data found in the directory.")
        else:
            print(f"\tDirectory '{self.dataset_path}' not found. Creating it now...")
            os.makedirs(self.dataset_path, exist_ok=True)
            print("\tPlease add face data to the directory to use face recognition.")
            sys.exit("\tExiting program. Dataset directory created.")

        os.makedirs(self.attendance_path, exist_ok=True)

    def load_or_create_encodings(self):
        if os.path.exists(self.encoded_file):
            with open(self.encoded_file, 'rb') as file:
                self.encoded_list, self.classNames = pickle.load(file)
            print("\tLoaded encodings from file.")
        else:
            images, self.classNames = [], []
            for element in os.listdir(self.dataset_path):
                if element.endswith(("jpg", "jpeg")):
                    img = cv2.imread(os.path.join(self.dataset_path, element))
                    images.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                    self.classNames.append(element.split("_")[0])

            # Encode and save to file
            self.encoded_list = [face_recognition.face_encodings(img)[0] for img in images]
            with open(self.encoded_file, 'wb') as file:
                pickle.dump((self.encoded_list, self.classNames), file)
            print("\tEncodings created and saved.")

    def record_attendance(self, name):
        current_date = datetime.now().strftime("%d-%m-%Y")
        file_path = os.path.join(self.attendance_path, f"{current_date}.csv")

        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write("Name,Time\n")

        with open(file_path, "r+") as f:
            name_list = [line.split(",")[0] for line in f.readlines()]
            if name not in name_list:
                f.write(f"{name},{datetime.now().strftime('%H:%M:%S')}\n")
                print(f"\t{name} recorded in attendance.")

    def threaded_attendance(self, name):
        if name != "Unknown Person":
            threading.Thread(target=self.record_attendance, args=(name,)).start()

    @staticmethod
    def render_distance(value):
        if value == "close":
            return 0.25, 4
        elif value == "mid":
            return 0.5, 2
        return 1, 1

    def start_recognition(self, q_lty, mup, frame_skip=3):
        capture_video = cv2.VideoCapture(0)
        frame_count = 0

        while True:
            if keyboard.is_pressed('q'):
                print("\tProgram closed.")
                break

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
                cv2.rectangle(img_original, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cv2.rectangle(img_original, (x1, y2 + 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img_original, name, (x1 + 6, y2 + 14), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)

                if name != "Unknown Person":
                    cv2.putText(img_original, f"{round(face_distances[match_index], 10)}", (x1 + 6, y2 + 28),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

            cv2.imshow("Webcam", img_original)
            if cv2.waitKey(1) == ord('q'):
                break

        capture_video.release()
        cv2.destroyAllWindows()


def main():
    batch = "CSE_batch_41"
    dataset_path = "Data_set/Face_recognition/"+batch+"/"
    attendance_path = "Attendance/"+batch+"/"
    face_recognition_system = FaceRecognitionAttendance(dataset_path, attendance_path)
    face_recognition_system.load_or_create_encodings()

    q_lty, mup = FaceRecognitionAttendance.render_distance("far")  # close, mid, far
    face_recognition_system.start_recognition(q_lty, mup)


if __name__ == "__main__":
    main()
