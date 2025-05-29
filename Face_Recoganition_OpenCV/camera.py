import cv2 as cv
from face_recognition import face_locations, face_encodings
from interFace_msg import message
import os

class Camera:
    def __init__(self):
        self.path = os.path.join(os.getcwd(), 'data')
        self.isSaved = False
        self.cam = cv.VideoCapture(0)
        
    def destroy(self):
        cv.destroyAllWindows()
        if self.cam.isOpened():
            self.cam.release()
        message("Camera closed successfully.")

    def capture(self):
        if not self.cam.isOpened():
            message("Could not open camera. Please check your camera connection.", input_key=True)
            return

        message("Press 's' to save the image or 'q' to quit.")
        while True:
            ret, frame = self.cam.read()
            if not ret:
                message("Error: Could not read frame.")
                break

            cv.imshow('Camera - Press s to save', frame)
            key = cv.waitKey(1) & 0xFF

            if key == ord('s'):
                if not os.path.exists(self.path):
                    os.makedirs(self.path)
                cv.imwrite(os.path.join(self.path, 'temp.jpg'), frame)
                self.isSaved = True
                break
            elif key == ord('q'):
                print("Capture cancelled.")
                break


    @staticmethod
    def crop_face(image_path):
        if not os.path.exists(image_path):
            message("Error: Image file does not exist.")
            return None
        image_bgr = cv.imread(image_path)
        if image_bgr is None:
            message("Error: Could not read image.")
            return None
        # Convert the image to RGB
        image_rgb = cv.cvtColor(image_bgr, cv.COLOR_BGR2RGB)
        # Detect faces in the image
        face_locs = face_locations(image_rgb)
        margin = 10
        if not face_locs:
            message("Error: No faces detected in the image.")
            return None
        # Crop the first detected face
        cropped_faces = []
        cropped_faces_locations = []

        for (top, right, bottom, left) in face_locs:
            top = max(0, top - margin)
            left = max(0, left - margin)
            bottom = min(image_bgr.shape[0], bottom + margin)
            right = min(image_bgr.shape[1], right + margin)
            cropped_face = image_bgr[top:bottom, left:right]
            if cropped_face.size == 0:
                message("Error: Cropped face is empty.")
                return None
            cropped_faces.append(cropped_face)
            cropped_faces_locations.append((top, right, bottom, left))
        return cropped_faces, cropped_faces_locations
    
    @staticmethod
    def img_write(image, path , convert_to_bgr=False):
        if convert_to_bgr:
            image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        if os.path.dirname(path) and not os.path.exists(path):
            os.makedirs(path)
        cv.imwrite(path, image)
        
    @staticmethod
    def put_rectangle(image_path, location, name, id,convert_to_bgr=False):
        image = cv.imread(image_path)
        if image is None:
            message(f"Error: Could not load image from {image_path}")
            return
        if convert_to_bgr:
            image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        top, right, bottom, left = location
        cv.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        if name and id:
            cv.putText(image, f"{name} (ID: {id})", (left, top - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv.imshow("Recognized Face", image)
        cv.waitKey(0)
        cv.destroyAllWindows()

    @staticmethod
    def get_face_encodings(image_path,face_locations, convert_to_bgr=False):
        image = cv.imread(image_path)
        if image is None:
            message(f"Error: Could not load image from {image_path}")
            return None
        if convert_to_bgr:
            image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        encodings = face_encodings(image, face_locations)
        if not encodings:
            message("No face encodings found in the image.")
            return None
        return encodings