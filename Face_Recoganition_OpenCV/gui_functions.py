import camera_embed as ce
import os
from tkinter import Frame
from camera import Camera
from save import Save
from match import match
import sys

def get_safe_data_path(folder_name='data'):
    base_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
    data_path = os.path.join(base_dir, folder_name)
    os.makedirs(data_path, exist_ok=True)
    return data_path

def camera_frame(frame, cap ,control_flag, row=0, column=0, padx=0, pady=0 , rowspan=1, columnspan=1, st = [None], path_save=None , camera_frame_size=(640,480),camera_index=0,fps = 30,camera_resolution=(640,480)):
    frame.grid(row=row, column=column, padx=padx, pady=pady, rowspan=rowspan, columnspan=columnspan)
    latest_frame = [None] 
    ce.show_camera_embed(frame, fps, cap, control_flag, latest_frame, st, path_save,camera_frame_size, camera_index=camera_index, resolution = camera_resolution)
    return frame, latest_frame

def cam_reg_gui_capture(parent_frame, image , row=0, column=0, padx=0, pady=0 , rowspan=1, columnspan=1):
    parent_frame.grid(row=row, column=column, padx=padx, pady=pady, rowspan=rowspan, columnspan=columnspan)
    ce.show_image_embed(parent_frame, image)
    return parent_frame

def clear_images(ls):
    for img_path in ls:
        try:
            os.remove(img_path)
        except FileNotFoundError:
            pass
        except Exception as e: 
            print(f"Error removing {img_path}: {e}")

# def get_cropped_faces_locations(image):
#     img_path = os.path.join(get_safe_data_path(),'img.jpg')
#     if image is None:
#         return [None],[None],[None]
#     Camera.img_write(image,img_path)
#     res =  Camera.crop_face(img_path)
#     if res is None:
#         return [None],[None],[None]
#     faces,locations = res
#     encodings = Camera.get_face_encodings(img_path, locations)
#     return faces, locations, encodings

def match_image(encoding, location, existing_data, threshold_confidence, img):
    image1 = img.copy()
    try:
        matched = match(encoding, existing_data)
    except ValueError as e:
        print(f"Error matching image: {e}")
        return None, None
    image1 = Camera.put_rect(image1, location)
    if matched is not None and matched[1] < threshold_confidence:
        return image1, matched
    return  image1, None

def check_registration(name, id):
    file_path = os.path.join(get_safe_data_path(), f'{name}_{id}_0.npy')
    if os.path.exists(file_path):
        return True
    return False

def update_user(path, name, id, new_name, new_id):
    if new_id == id and new_name == name:
        print("No changes made to the user.")
        return
    if not new_name or not new_id:
        print("Name and ID cannot be empty.")
        return
    for file in os.listdir(path):
        if file.startswith(f"{name}_{id}_"):
            try:
                dno = file.split('_')[-1]
                os.rename(os.path.join(path, file), os.path.join(path, f"{new_name}_{new_id}_{dno}"))
            except ValueError as e:
                print(f"Error updating user: {e}")
    print(f"User {name} with ID {id} updated successfully.")

def save_image_data(encoding, save , name=None, id=None):
    filename = save.get_filename(name, id)
    dno = filename.split('_')[-1].split('.')[0]
    save.save(encoding, filename)
    return dno

def destroy_camera(cap):
    ce.destroy_camera(cap)

def read_image(image_path):
    return Camera.img_read(image_path)

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

def get_available_cameras(max_cameras=10):
    cam_list = Camera.get_available_cameras(max_cameras)
    cam_list = [f"Camera {i+1}" for i in cam_list]
    if not cam_list:
        cam_list = ["No cameras found"]
    return cam_list
    
def get_camera_index_from_name(name):
    if name == "No cameras found":
        return None
    try:
        return int(name.split(' ')[-1]) - 1
    except ValueError:
        return None
    
def get_camera_resolution_list(camera_index=0, aspect_ratio="16:9"):
    """
    Returns a list of supported resolutions for a given camera and aspect ratio.
    """
    if not isinstance(camera_index, int):
        return ["Select a camera"]
    if not aspect_ratio:
        return ["Select an aspect ratio"]

    all_resolutions = {
        "16:9": [(320,180), (640,360), (1280,720), (1920,1080), (2560,1440), (3840,2160)],
        "4:3":  [(320,240), (640,480), (800,600), (960,720), (1024,768), (1280,960), (1600,1200)],
        "1:1":  [(320,320), (480,480), (640,640), (720,720), (1080,1080)],
        "21:9": [(1280,540), (1920,810), (2560,1080), (3440,1440)],
        "3:2":  [(360,240), (720,480), (1080,720), (1440,960), (2160,1440)],
        "5:4":  [(640,512), (800,640), (1280,1024)]
    }

    supported_resolutions = []
    resolutions_to_check = all_resolutions.get(aspect_ratio, [])
    config = {'camera_index' : camera_index}
    for (w, h) in resolutions_to_check:
        if(Camera.test_camera_resolution(config, (w, h))):
            supported_resolutions.append(f"{w}x{h}")

    if not supported_resolutions:
        return ["No supported resolution"]
    return supported_resolutions


def get_aspect_ratio_list(camera_index=0):
    aspect_list = [
        "16:9", "4:3", "1:1", "21:9", "3:2", "5:4"
    ]
    return aspect_list

def get_fps_list(camera_index=0, resolution=(1280, 720)):
    fps_list = [5,10,15,24,25,30]
    res = []
    config = {'camera_index' : camera_index, 'camera_resolution': resolution}
    for fps in fps_list:
        if Camera.test_camera_fps(config, fps):
            res.append(fps)
    return res



