import os
import face_recognition
import numpy as np

class saveData:
    def __init__(self,name,id,imag):
        self.name = name
        self.id = id
        self.path = os.path.join(os.getcwd(), 'data\\', f'{name}_{id}.npy')
        self.imag = imag
        self.save_img()
    
    def save_img(self):
        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))
        np.save(self.path, self.encode(self.imag))
        print(f"Data saved to {self.path}")

    def encode(self, image_path):
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if not encodings:
            print("Error: No face detected.")
            return None
        return encodings[0]


class loadData:
    def __init__(self):
        self.data = []
        self.labels = []
        self.load()
    
    def load(self):
        # Load all the data from the data directory
        for filename in os.listdir(os.path.join(os.getcwd(), 'data')):
            if filename.endswith('.npy'):
                path = os.path.join(os.getcwd(), 'data', filename)
                self.data.append(np.load(path))
                name, id = os.path.splitext(filename)[0].split('_')
                self.labels.append((name, id))