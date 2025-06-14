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

def camera_frame(frame, cap ,control_flag, row=0, column=0, padx=0, pady=0 , rowspan=1, columnspan=1, st = [None], path_save=None):
    frame.grid(row=row, column=column, padx=padx, pady=pady, rowspan=rowspan, columnspan=columnspan)
    latest_frame = [None]  # Use list for mutability
    ce.show_camera_embed(frame, 60, cap, control_flag, latest_frame, st, path_save)
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
    res =  Camera.crop_face(img_path)
    if res is None:
        return [None],[None],[None]
    faces,locations = res
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

def validate_date(date_str):
    if date_str == "":
        return True
    try:
        day, month, year = map(int, date_str.split('/'))
        if 1 <= day <= 31 and 1 <= month <= 12 and year > 0:
            return True
    except ValueError:
        pass
    return False

def validate_time(time_str):
    if time_str == "":
        return True
    try:
        hour, minute , seconds = map(int, time_str.split(':'))
        if 0 <= hour < 24 and 0 <= minute < 60 and 0 <= seconds < 60:
            return True
    except ValueError:
        pass
    return False

def get_all_date_time(ex,c_row,date_in, time_in, date_out,time_out):
    # di_ ti_ do_ to_   - Read all Entries
    # di_ ti_ do_ to    - Read Until last Date under time_out
    # di_ ti_ do  to_   - Read Until Date date_out time 23:59:59
    # di_ ti_ do  to    - Read Until Date date_out time time_out
    # di_ ti  do_ to_   - Read from time time_in Date starting date
    # di_ ti  do_ to    - Read from time time_in Date starting date to date Last Date time time_out
    # di_ ti  do  to_   - Read from time time_in Date starting date to date date_out time 23:59:59
    # di_ ti  do  to    - Read from time time_in Date starting date to date date_out time time_out
    # di  ti_ do_ to_   - Read from date date_in time 00:00:00
    # di  ti_ do_ to    - Read from date date_in time 00:00:00 to date Last Date time time_out
    # di  ti_ do  to_   - Read from date date_in time 00:00:00 to date date_out time 23:59:59
    # di  ti_ do  to    - Read from date date_in time 00:00:00 to date date_out time time_out
    # di  ti  do_ to_   - Read from date date_in time 00:00:00 to date Last date time 23:59:59
    # di  ti  do_ to    - Read from date date_in time 00:00:00 to date Last date time time_out
    # di  ti  do  to_   - Read from date date_in time 00:00:00 to date date_out time 23:59:59
    # di  ti  do  to    - Read from date date_in time 00:00:00 to date date_out time time_out
    if not validate_date(date_in) or not validate_time(time_in):
        return "", "", "", ""
    if not validate_date(date_out) or not validate_time(time_out):
        return "", "", "", ""
    st_date,_ = ex.read_excel(c_row, 5).split(" - ")
    en_date,_ = ex.read_excel(c_row, ex.ws.max_column).split(" - ")
    if date_in == "":
        date_in = st_date
    if time_in == "":
        time_in = "00:00:00"
    if date_out == "":
        date_out = en_date
    if time_out == "":
        time_out = "23:59:59"
    return date_in, time_in, date_out, time_out

def create_new_user_entry(id, name, ex):
    ex.write_to_excel(name, id, 0, 1)
    ex.delete_entry(ex.ws.max_row,5)
    ex.increment_entry_count(ex.ws.max_row, -1)

def delete_user_entries(ex, c_row, entries,list_box):
    
    shift = 0
    mapped_entries = []

    for entry in entries:
        if list_box.get(entry) is not None:
            mapped_entries.append(list_box.get(entry))

    for cl in range(5, ex.ws.max_column + 1):
        ex_val = ex.read_excel(c_row, cl)
        if ex_val is not None and ex_val in mapped_entries:
            shift += 1
        else:
            ex.write_excel(c_row, cl-shift, ex_val)
    max_column = ex.ws.max_column - shift
    for col in range(ex.ws.max_column, max_column, -1):
        ex.write_excel(c_row, col, None)
    ex.increment_entry_count(c_row, -shift)

    
    

