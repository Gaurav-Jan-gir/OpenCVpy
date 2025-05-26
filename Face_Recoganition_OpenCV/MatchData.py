import LoadData
import face_recognition

class matchData:
    def __init__(self, imag, load_data=None):
        self.imag = imag
        self.load_data = load_data if load_data else LoadData.loadData()
        self.result = self.match()
    
    def match(self):
        # Load the image
        image = face_recognition.load_image_file(self.imag)
        # Encode the image
        encoding = face_recognition.face_encodings(image)
        if not encoding:
            print("Error: No face detected.")
            return None
        # Compare the image with the data
        results = face_recognition.compare_faces(self.load_data.data, encoding[0])
        for match, (name, id, dno) in zip(results, self.load_data.labels):
            if match:
                return (name, id)
        
        print("No match found.")
        return None