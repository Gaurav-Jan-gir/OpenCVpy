import numpy as np
import os

class Save:
    def __init__(self, path: str):
        self.path = path

    def save(self, data: np.ndarray, filename: str):
        if data is None or not isinstance(data, np.ndarray) or data.shape != (128,):
            raise ValueError("Invalid encoding data.")
        full_path = os.path.join(self.path, filename)
        try:
            np.save(full_path, data)
        except Exception as e:
            print(f"Failed to save data: {e}")

    def get_filename(self, name: str, id: str) -> str:
        if not name or not id:
            raise ValueError("Name and ID must be provided.")
        dno = 0
        file_name = f"{name}_{id}_{dno}.npy"
        while os.path.exists(os.path.join(self.path, file_name)):
            dno += 1
            file_name = f"{name}_{id}_{dno}.npy"
        return file_name
    
    @staticmethod
    def get_nameid() -> str|str:
        name = input("Enter the name: ").strip()
        if not name:
            raise ValueError("Name cannot be empty.")
        id = input("Enter the ID: ").strip()
        if not id:
            raise ValueError("ID cannot be empty.")
        return name, id
    
    def update_existing_user(self, encoding: np.ndarray, name: str, id: str):
        if not encoding or not isinstance(encoding, np.ndarray) or encoding.shape != (128,):
            raise ValueError("Invalid encoding data.")
        filename = self.get_filename(name, id)
        self.save(encoding, filename)
        print(f"User {name} with ID {id} updated successfully.")
    

