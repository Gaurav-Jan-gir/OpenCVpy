import os
import face_recognition
import numpy as np
import cv2 as cv
from MatchData import matchData

class saveData:
    def __init__(self,imag, load_data=None):
        self.name = ""
        self.id = ""
        self.flag = False
        self.load_data = load_data
        self.dno = 0
        self.path = ""
        self.imag = imag
        self.encode()
    
    def save_img(self,encoding):
        data_dir = os.path.join(os.getcwd(), 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        while True:
            self.path = os.path.join(data_dir, f'{self.name}_{self.id}_{self.dno}.npy')
            if not os.path.exists(self.path):
                break
            self.dno += 1
        
        np.save(self.path, encoding)


    def faceLocation(self, image):
        face_locations = face_recognition.face_locations(image)
        encodings = face_recognition.face_encodings(image, face_locations)
        if len(face_locations) != len(encodings):
            print("Error: Number of face locations and encodings do not match.")
            return None, None
        if not encodings:
            print("Error: No face detected.")
            return None, None
        return face_locations, encodings


    def encode(self):
        image = face_recognition.load_image_file(self.imag)
        face_locations, encodings = self.faceLocation(image)
        if face_locations is None or encodings is None:
            self.flag = False
            return
        
        # Convert RGB to BGR for OpenCV display
        image_bgr = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        for face_location, encoding in zip(face_locations, encodings):
            top, right, bottom, left = face_location
            # add margin to crop the face
            margin = 10
            top = max(0, top - margin)
            left = max(0, left - margin)
            bottom = min(image.shape[0], bottom + margin)
            right = min(image.shape[1], right + margin)
            cropped_face = image[top:bottom, left:right]
            cropped_face_bgr = cv.cvtColor(cropped_face, cv.COLOR_RGB2BGR)
            cropped_face_path = os.path.join(os.getcwd(), 'data','cropped_face.jpg')
            cv.imwrite(cropped_face_path, cropped_face_bgr)
            matcher = matchData(cropped_face_path, load_data=self.load_data)
            if matcher.result is not None:
                choice = self.interfaceSaveData(matcher.result[0], matcher.result[1]) 
                if choice == 1:
                    self.name = matcher.result[0]
                    self.id = matcher.result[1]
                    self.save_img(encoding)
                    self.flag = True
                    continue
                elif choice == 2 or choice == 3:
                    cv.rectangle(image_bgr, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv.imshow("Face Detected", image_bgr)
                    cv.waitKey(1)
                    self.name = input("Enter User Name for the face detected: ")
                    self.id = input("Enter User ID for the face detected: ")
                    cv.destroyWindow("Face Detected")
                    if choice == 3:
                        self.changeAllMatchData(matcher.result[0], matcher.result[1])
                    self.save_img(encoding)
                    self.flag = True
                elif choice == 0:
                    print("Aborting saving current data.")
                    self.flag = False
                    continue
            else:
                # No match found, ask for new name and ID
                cv.rectangle(image_bgr, (left, top), (right, bottom), (0, 255, 0), 2)
                cv.imshow("Face Detected", image_bgr)
                cv.waitKey(1)
                self.name = input("Enter User Name for the face detected: ")
                self.id = input("Enter User ID for the face detected: ")
                cv.destroyWindow("Face Detected")
                self.save_img(encoding)
                self.flag = True

    def changeAllMatchData(self, name, id):
        data_dir = os.path.join(os.getcwd(), 'data')
        if os.path.exists(data_dir):
            for file in os.listdir(data_dir):
                if file.startswith(f'{name}_{id}_'):
                    old_path = os.path.join(data_dir, file)
                    new_path = os.path.join(data_dir, f'{self.name}_{self.id}_{file.split("_")[-1]}')
                    os.rename(old_path, new_path)

    def interfaceSaveData(self, name, id):
        print(f'User already exists with\nName: {name} and ID: {id}')
        print('Press 1 to Save Current data with existing Name and ID')
        print('Press 2 to Save current data with new Name and ID')
        print('Press 3 to Update existing data with new Name and ID')
        print('Press any other key to abort saving current data')
        choice = input()
        if(choice=='1'):
            return 1
        elif(choice=='2'):
            return 2
        elif(choice=='3'):
            return 3
        else:
            return 0
        
            