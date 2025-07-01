import numpy as np
from face_recognition import face_distance

def match(encoding : np.ndarray, data):

    if not isinstance(encoding, np.ndarray):
        print(f"{type(encoding)}")
        raise ValueError("Encoding must be np.ndarray")
    
    conf_scores = face_distance(data.data, encoding)
    if len(conf_scores) == 0:
        return None
    min_score = np.min(conf_scores)
    min_index = np.argmin(conf_scores)
    return data.labels[min_index], min_score