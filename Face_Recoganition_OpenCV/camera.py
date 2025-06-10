import cv2 as cv
from face_recognition import face_locations, face_encodings
from interFace_msg import message
import os
import sys

def get_safe_data_path():
    base_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'data')
    os.makedirs(data_path, exist_ok=True)
    return data_path
class Camera:
    def __init__(self):
        self.path = get_safe_data_path()
        os.makedirs(self.path, exist_ok=True)  # Ensure folder exists
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
                self.isSaved = False
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
    def img_read(path, convert_to_bgr=False):
        if not os.path.exists(path):
            message(f"Error: Image file {path} does not exist.")
            return None
        image = cv.imread(path)
        if image is None:
            message(f"Error: Could not read image from {path}.")
            return None
        if convert_to_bgr:
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        return image

    @staticmethod
    def resize_image(image, width=None, height=None):
        if image is None:
            message("Error: No image provided for resizing.")
            return None
        if width is None and height is None:
            message("Error: At least one of width or height must be specified.")
            return image
        h, w = image.shape[:2]
        if width is None:
            width = int((height / h) * w)
        elif height is None:
            height = int((width / w) * h)
        resized_image = cv.resize(image, (width, height))
        return resized_image

    @staticmethod
    def img_write(image, path , convert_to_bgr=False):
        if convert_to_bgr:
            image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        if os.path.dirname(path) and not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        cv.imwrite(path, image)
        
    @staticmethod
    def put_rectangle(image_path, location, name, id,convert_to_bgr=False,embedding=False):
        if isinstance(image_path, str):
            image = cv.imread(image_path)
        else:
            image = image_path
        if image is None:
            message(f"Error: Could not load image from {image_path}")
            return
        if convert_to_bgr:
            image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        top, right, bottom, left = location
        cv.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        if name and id:
            cv.putText(image, f"{name} (ID: {id})", (left, top - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        if embedding:
            return image
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
    
    def process_frame_in_memory(self, frame):
        # Process frame directly without saving to disk
        face_locations_list = face_locations(frame)
        face_encodings_list = face_encodings(frame, face_locations_list)
        return face_encodings_list, face_locations_list
    
    @staticmethod
    def convert_to_bgr(image):
        if image is None:
            message("Error: No image provided for conversion.")
            return None
        return cv.cvtColor(image, cv.COLOR_RGB2BGR) if len(image.shape) == 3 else image
    
    @staticmethod
    def convert_to_rgb(image):
        if image is None:
            message("Error: No image provided for conversion.")
            return None
        return cv.cvtColor(image, cv.COLOR_BGR2RGB) if len(image.shape) == 3 else image