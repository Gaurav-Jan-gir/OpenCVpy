import os
import face_recognition
import numpy as np
from MatchData import matchData

class saveData:
    def __init__(self,name,id,imag, load_data=None):
        self.name = name
        self.id = id
        self.flag = True
        matcher = matchData(imag, load_data)
        if matcher.result is not None:
            self.matchNameId(matcher.result)
        self.dno = 0
        self.path = os.path.join(os.getcwd(), 'data\\', f'{name}_{id}_{self.dno}.npy')
        self.imag = imag
        if self.flag:
            self.save_img()
    
    def save_img(self):
        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))
        
        encoding = self.encode(self.imag)
        if encoding is None:
            print("Error: Could not encode face. Aborting save.")
            self.flag = False
            return
        
        while os.path.exists(self.path):
            self.dno = str(int(self.dno) + 1)
            self.path = os.path.join(os.getcwd(), 'data\\', f'{self.name}_{self.id}_{self.dno}.npy')
        
        np.save(self.path, encoding)


    def encode(self, image_path):
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if not encodings:
            print("Error: No face detected.")
            return None
        return encodings[0]
    
    def matchNameId(self, result):
        choice = self.interfaceSaveData(result[0], result[1])
        if choice == 1:
            self.name = result[0]
            self.id = result[1]
            return
        elif choice == 2:
            return
        elif choice == 3:
            self.changeAllMatchData(result[0], result[1])
            return
        elif choice == 0:
            print('Aborting saving current data')
            self.flag = False
            return
    
    def changeAllMatchData(self, name, id):
        for file in os.listdir(os.path.join(os.getcwd(), 'data')):
            if file.startswith(f'{name}_{id}_'):
                old_path = os.path.join(os.getcwd(), 'data', file)
                new_path = os.path.join(os.getcwd(), 'data', f'{self.name}_{self.id}_{file.split("_")[-1]}')
                os.rename(old_path, new_path)

    def interfaceSaveData(self, name, id):
        if name == self.name and id == self.id:
            print(f'User already exists with same Name and Id \nName: {name} and ID: {id}')
            print('Press 1 to save Current data or any other key to abort saving current data')
            if(input()=='1'):
                print('Saving Current data')
                return 1
            else:
                print('Abort Saving Current data')
                return 0
        else:
            print(f'User already exists with different Name and Id \nName: {name} and ID: {id}')
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
        
            