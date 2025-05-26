import cv2 as cv
import sys
import os
import face_recognition
from MatchData import matchData
from SaveData import saveData
from LoadData import loadData

class interFace:
    def __init__(self):
        self.path = os.path.join(os.getcwd(), 'data')
        self.load_data = loadData()
        self.run()
    
    def run(self):
        while True:
            print("Welcome to the face recognition system")
            print("1. Register a new user via Camera")
            print("2. Register a new user via Image")
            print("3. Recognize a user")
            print("4. Check if User Data exist or not.")
            print("5. Exit")
            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                input("Press any key to continue...")
                self.clear_screen()
                continue

            if choice == 1:
                self.registerViaCamera()
            elif choice == 2:
                imag = input("Enter the path of the image: ")
                self.registerViaImage(imag)
            elif choice == 3:
                self.recognize()
            elif choice == 4:
                if self.is_valid_path(os.path.join(self.path,f'{input("Enter User Name ")}_{input("Enter User ID ")}_0.npy')):
                    print("The User Data Exists. ")
                else:
                    print("The User Data does not exist.")
                print()
                input("Press any key to continue...")
                self.clear_screen()
            elif choice == 5:
                print("Exiting program...")
                sys.exit()
            else:
                print("Invalid choice")
                input("Press any key to continue...")
                self.clear_screen()

        
    

    def registerViaCamera(self):
        cap = cv.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open video.")
            print()
            input("Press any key to continue...")
            self.clear_screen()
            return

        print("Camera warming up... please wait.")
        # Warm-up: grab some frames to let camera adjust
        for _ in range(30):
            ret, frame = cap.read()
            if not ret:
                continue

        print("Press 's' to save the image or 'q' to quit.")
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            cv.imshow('Camera - Press s to save', frame)
            key = cv.waitKey(1) & 0xFF
            if key == ord('s'):
                # Save and break
                if not os.path.exists(self.path):
                    os.makedirs(self.path)
                cv.imwrite(os.path.join(self.path, 'temp.jpg'), frame)
                break
            elif key == ord('q'):
                print("Cancelled by user.")
                break

        cap.release()
        cv.destroyAllWindows()

        if key == ord('s'):
            self.registerViaImage(os.path.join(self.path, 'temp.jpg'))
        else:
            self.clear_screen()

    
    def registerViaImage(self, imag):
        if not os.path.exists(imag):
            print("Error: Could not find image.")
            print()
            input("Press any key to continue...")
            self.clear_screen()
            return
        saveStatus = saveData(imag,self.load_data)
        if saveStatus.flag:
            print("User registered successfully")
            self.load_data = loadData()
        print()
        input("Press any key to continue...")
        self.clear_screen()
        return
    
    def recognize(self):
        cap = cv.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open video.")
            print()
            input("Press any key to continue...")
            self.clear_screen()
            return

        print("Camera warming up... please wait.")
        for _ in range(30):
            ret, frame = cap.read()
            if not ret:
                continue

        print("Press 's' to capture image or 'q' to cancel.")
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            cv.imshow('Camera - Press s to capture', frame)
            key = cv.waitKey(1) & 0xFF
            if key == ord('s'):
                cv.imwrite(os.path.join(self.path, 'temp.jpg'), frame)
                break
            elif key == ord('q'):
                print("Cancelled by user.")
                break

        cap.release()
        cv.destroyAllWindows()

        if key == ord('s'):
            cropped_faces , cropped_faces_locations = self.crop_face(os.path.join(self.path, 'temp.jpg'))
            for cropped_face, location in zip(cropped_faces, cropped_faces_locations):
                top, right, bottom, left = location
                cv.rectangle(cropped_face, (left, top), (right, bottom), (0, 255, 0), 2)
                cropped_face_path = os.path.join(self.path, 'cropped.jpg')
                cv.imwrite(cropped_face_path, cropped_face)
                matcher = matchData(cropped_face_path,load_data=self.load_data)
                matched = matcher.result
                if matched:
                    name, id = matched
                    print(f"User recognized: {name} (ID: {id})")
                    image = cv.imread(os.path.join(self.path, 'temp.jpg'))
                    # Ensure image is loaded
                    if image is None:
                        print(f"Error: Could not load image from {os.path.join(self.path, 'temp.jpg')}")
                        continue # or handle error appropriately
                    cv.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv.putText(image, f"{name} (ID: {id})", (left, top - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    cv.imshow("Recognized Face", image)
                    cv.waitKey(0)
                    cv.destroyAllWindows()
                else:
                    print("No match found.")
        print()
        input("Press any key to continue...")
        self.clear_screen()

    def is_valid_path(self, path):
        return os.path.exists(path) and os.path.isfile(path)
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def crop_face(self, image_path):
        if not os.path.exists(image_path):
            print("Error: Image file does not exist.")
            return None
        image_bgr = cv.imread(image_path)
        if image_bgr is None:
            print("Error: Could not read image.")
            return None
        # Convert the image to RGB
        image_rgb = cv.cvtColor(image_bgr, cv.COLOR_BGR2RGB)
        # Detect faces in the image
        face_locations = face_recognition.face_locations(image_rgb)
        margin = 10
        if not face_locations:
            print("Error: No faces detected in the image.")
            return None
        # Crop the first detected face
        cropped_faces = []
        cropped_faces_locations = []

        for (top, right, bottom, left) in face_locations:
            top = max(0, top - margin)
            left = max(0, left - margin)
            bottom = min(image_bgr.shape[0], bottom + margin)
            right = min(image_bgr.shape[1], right + margin)
            cropped_face = image_bgr[top:bottom, left:right]
            if cropped_face.size == 0:
                print("Error: Cropped face is empty.")
                return None
            cropped_faces.append(cropped_face)
            cropped_faces_locations.append((top, right, bottom, left))
        return cropped_faces, cropped_faces_locations


