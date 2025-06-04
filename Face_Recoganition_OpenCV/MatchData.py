from face_recognition import face_encodings, face_distance
from interFace_msg import message


def match(image,match_data):
    encoding = face_encodings(image)
    if not encoding:
        message("No face encodings found in the image.")
        return None
    # Compare the image with the data
    confidence_scores = face_distance(match_data.data, encoding[0])
    if len(confidence_scores) == 0:
        message("Comparison failed — no confidence scores generated.")
        return None
    max_confidence_index = 0
    max_confidence_score = confidence_scores[0]
    for i, score in enumerate(confidence_scores):
        if score < max_confidence_score:
            max_confidence_score = score
            max_confidence_index = i
    name,id,dno=match_data.labels[max_confidence_index]
    return (name,id,dno,max_confidence_score)
        