import os
from numpy import save as np_save
from MatchData import matchData
import interFace_msg as interFace
from camera import Camera

class saveData:
    def __init__(self,imag, load_data=None, showConfidence = False ,threshold_confidence=0.7):
        self.name = ""
        self.id = ""
        self.flag = False
        self.load_data = load_data
        self.dno = 0
        self.path = ""
        self.imag = imag
        self.showConfidence = showConfidence  
        self.threshold_confidence = threshold_confidence  
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
        
        np_save(self.path, encoding)

    def encode(self):

        cropped_faces, face_locations = Camera.crop_face(self.imag)
        encodings = Camera.get_face_encodings(self.imag,face_locations)
        if face_locations is None or encodings is None:
            self.flag = False
            return
        
        for i,(cropped_face,face_location, encoding) in enumerate(zip(cropped_faces,face_locations, encodings)):
            cropped_face_path = os.path.join(os.getcwd(), 'data','cropped_face.jpg')
            Camera.img_write(cropped_face,cropped_face_path, convert_to_bgr=True)
            matcher = matchData(cropped_face_path, load_data=self.load_data)
            Camera.put_rectangle(self.imag, face_location, "","")
            if matcher.result is not None and matcher.result[3] < self.threshold_confidence:
                choice = interFace.interfaceSaveData(matcher.result[0], matcher.result[1], matcher.result[3],showConfidence=self.showConfidence) 
                if choice == 1:
                    self.name = matcher.result[0]
                    self.id = matcher.result[1]
                    self.save_img(encoding)
                    self.flag = True
                    continue
                elif choice == 2 or choice == 3:
                    self.name , self.id = interFace.input_data()
                    if choice == 3:
                        self.changeAllMatchData(matcher.result[0], matcher.result[1])
                    self.save_img(encoding)
                    self.flag = True
                elif choice == 0:
                    interFace.message("Aborting saving current data.")
                    self.flag = False
                    continue
            elif( matcher.result is not None and matcher.result[3] >= self.threshold_confidence):
                # No match found, ask for new name and ID
                self.name , self.id = interFace.input_data()
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

    
        
            