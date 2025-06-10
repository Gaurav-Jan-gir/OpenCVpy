import camera_embed as ce
from Interface_excel import interFace 
import os
from tkinter import Frame
from camera import Camera
from SaveData import saveData
from MatchData import match
import sys

def get_safe_data_path():
    base_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'data')
    os.makedirs(data_path, exist_ok=True)
    return data_path

def camera_frame(frame, cap ,control_flag, row=0, column=0, padx=0, pady=0 , rowspan=1, columnspan=1):
    frame.grid(row=row, column=column, padx=padx, pady=pady, rowspan=rowspan, columnspan=columnspan)
    latest_frame = [None]  # Use list for mutability
    ce.show_camera_embed(frame, 60, cap, control_flag, latest_frame)
    return frame, latest_frame

def cam_reg_gui_capture(parent_frame, image , row=0, column=0, padx=0, pady=0 , rowspan=1, columnspan=1):
    parent_frame.grid(row=row, column=column, padx=padx, pady=pady, rowspan=rowspan, columnspan=columnspan)
    ce.show_image_embed(parent_frame, image)
    return parent_frame

def get_cropped_faces_locations(image):
    img_path = os.path.join(get_safe_data_path(),'img.jpg')
    if image is None:
        return [None],[None],[None]
    Camera.img_write(image,img_path)
    faces,locations =  Camera.crop_face(img_path)
    encodings = Camera.get_face_encodings(img_path, locations)
    return faces, locations, encodings

def match_image(face,location,existing_data,threshold_confidence,img=None):
    img_path = os.path.join(get_safe_data_path(),'img.jpg')
    if face is not None:
        matched = match(Camera.convert_to_rgb(face),existing_data)
        if matched is not None and matched[3] is not None and matched[3] < threshold_confidence:
            image = Camera.put_rectangle(img_path,location,None,None,embedding=True)
            return image,matched
        elif matched is not None:
            image = Camera.put_rectangle(img,location,None,None,embedding=True)
            return image,None
    return None,None

def check_registration(name, id):
    file_path = os.path.join(get_safe_data_path(), f'{name}_{id}_0.npy')
    if os.path.exists(file_path):
        return True
    return False





def save_image_data(encoding, name=None, id=None,existing_data=None,showConfidence=False, threshold_confidence=0.4):
    if existing_data is None:
        existing_data = []
    save_data = saveData(None, load_data=existing_data,showConfidence=showConfidence, threshold_confidence=threshold_confidence)
    save_data.save_img(encoding, name, id)
    return save_data.new_data,save_data.new_labels


def destroy_camera(cap):
    ce.destroy_camera(cap)

def read_image(image_path,convert_to_bgr = False):
    return Camera.img_read(image_path, convert_to_bgr)

def resize_image(image, width=None, height=None):
    return Camera.resize_image(image, width, height)

