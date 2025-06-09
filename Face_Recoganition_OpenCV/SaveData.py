import os
import sys
from numpy import save as np_save
from MatchData import match
import interFace_msg as interFace
from camera import Camera

def get_data_dir():
        base_path = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
        data_dir = os.path.join(base_path, 'data')
        os.makedirs(data_dir, exist_ok=True)
        return data_dir
class saveData:
    def __init__(self,imag, load_data=None, showConfidence = False ,threshold_confidence=0.7):
        self.name = ""
        self.id = ""
        self.flag = 0
        self.load_data = load_data
        self.dno = 0
        self.path = ""
        self.imag = imag
        self.showConfidence = showConfidence  
        self.threshold_confidence = threshold_confidence 
        self.new_data = []
        self.new_labels = [] 
    
    def save_img(self,encoding,name = None, id = None):
        if name is not None:
            self.name = name
        if id is not None:
            self.id = id
        self.dno = 0
        data_dir = get_data_dir()
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        while True:
            self.path = os.path.join(data_dir, f'{self.name}_{self.id}_{self.dno}.npy')
            if not os.path.exists(self.path):
                break
            self.dno += 1
        self.new_data.append(encoding)
        self.new_labels.append((self.name, self.id, self.dno))
        np_save(self.path, encoding)

    def encode(self):
        self.new_data = []
        self.new_labels = []
        cropped_faces, face_locations = Camera.crop_face(self.imag)
        encodings = Camera.get_face_encodings(self.imag,face_locations)
        if face_locations is None or encodings is None:
            self.flag = False
            return
        res = []
        for i,(cropped_face,face_location, encoding) in enumerate(zip(cropped_faces,face_locations, encodings)):
            cropped_face = Camera.convert_to_bgr(cropped_face)
            matcher_result = match(Camera.convert_to_rgb(cropped_face),self.load_data)
            Camera.put_rectangle(self.imag, face_location, "","")
            res.append((matcher_result,encoding))
        return res
            
    def create_labels(self,res):
        for matcher_result,encoding in res:
            if matcher_result is not None and matcher_result[3] < self.threshold_confidence:
                choice = interFace.interfaceSaveData(matcher_result[0], matcher_result[1], matcher_result[3],showConfidence=self.showConfidence) 
                if choice == 1:
                    self.name = matcher_result[0]
                    self.id = matcher_result[1]
                    self.save_img(encoding)
                elif choice == 2 or choice == 3:
                    self.name , self.id = interFace.input_data()
                    if choice == 3:
                        self.changeAllMatchData(matcher_result[0], matcher_result[1])
                    self.save_img(encoding)
                elif choice == 0:
                    interFace.message("Aborting saving current data.")
                self.flag = choice
            else:
                # No match found, ask for new name and ID
                self.name , self.id = interFace.input_data()
                self.save_img(encoding)
                self.flag = 1
    

    def changeAllMatchData(self, name, id):
        data_dir = get_data_dir()
        if os.path.exists(data_dir):
            for file in os.listdir(data_dir):
                if file.startswith(f'{name}_{id}_'):
                    old_path = os.path.join(data_dir, file)
                    new_path = os.path.join(data_dir, f'{self.name}_{self.id}_{file.split("_")[-1]}')
                    os.rename(old_path, new_path)


    
        
            