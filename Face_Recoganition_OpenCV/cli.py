from cli_message import *
from camera import Camera
from logs import Logs
from load import Load
from match import match
from save import Save
import os
import sys
import multiprocessing as mp
import time
from excel_handle import Excel_handle as excel
from datetime import datetime
import json

def get_safe_data_path():
    base_dir = os.path.dirname(sys.executable) if hasattr(sys, 'frozen') else os.path.dirname(__file__)
    data_path = os.path.join(base_dir, 'data')
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    return data_path

class CLI:
    def __init__(self):
        self.path = get_safe_data_path()
        self.cam_defaults = {}
        self.config = self.load_config()
        self.camera_config = {
            'camera_index': self.config['camera_index'] if 'camera_index' in self.config else 0, 
            'camera_resolution': self.config['camera_resolution'] if 'camera_resolution' in self.config else (640, 480),
            'camera_fps': self.config['camera_fps'] if 'camera_fps' in self.config else 30,
            'camera_focus': self.config.get('camera_focus', 0),
            'camera_brightness': self.config['camera_brightness'] if 'camera_brightness' in self.config else 0.5,
            'camera_contrast': self.config['camera_contrast'] if 'camera_contrast' in self.config else 0.5,
            'camera_saturation': self.config['camera_saturation'] if 'camera_saturation' in self.config else 0.5,
            'camera_exposure': self.config['camera_exposure'] if 'camera_exposure' in self.config else 0.5,
            'camera_gain': self.config['camera_gain'] if 'camera_gain' in self.config else 0.5,
            'camera_hue': self.config.get('camera_hue', 0),
            'camera_sharpness': self.config.get('camera_sharpness', 0),
            'camera_gamma': self.config.get('camera_gamma', 0),
            'camera_white_balance': self.config.get('camera_white_balance', 0),
            'camera_color_temperature': self.config.get('camera_color_temperature', 0),
        }
        self.cam = Camera(self.camera_config)
        self.logs = Logs(self.config['show_log'] if 'show_log' in self.config else True)
        self.data = Load(self.path, self.logs)
        self.save = Save(self.path)
        self.tolerance = self.config['tolerance'] if 'tolerance' in self.config else 0.4
        self.ex = excel(os.path.join(self.path, 'user_data.xlsx'))
        self.time_gap = self.config['time_gap'] if 'time_gap' in self.config else 15
        self.show_confidence = self.config['show_confidence'] if 'show_confidence' in self.config else True

    def load_config(self):
        cam0_defaults = Camera.get_defaults(0)
        default_config = {
            "tolerance": 0.4,
            "camera_index": 0,
            "camera_resolution": (640, 480),
            "camera_fps": 30,
            "camera_focus": cam0_defaults.get('camera_focus', 0),
            "camera_brightness": cam0_defaults['camera_brightness'],
            "camera_contrast": cam0_defaults['camera_contrast'],
            "camera_saturation": cam0_defaults['camera_saturation'],
            "camera_exposure": cam0_defaults['camera_exposure'],
            "camera_gain": cam0_defaults['camera_gain'],
            "camera_hue": cam0_defaults.get('camera_hue', 0),
            "camera_sharpness": cam0_defaults.get('camera_sharpness', 0),
            "camera_gamma": cam0_defaults.get('camera_gamma', 0),
            "camera_white_balance": cam0_defaults.get('camera_white_balance', 0),
            "camera_color_temperature": cam0_defaults.get('camera_color_temperature', 0),
            "show_log": True,
            "show_confidence": True,
            "time_gap": 15
        }
        config_path = os.path.join(self.path, 'config.json')
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"Error loading config: {e}")
        else:
            self.save_config(default_config)
        return default_config
    
    def save_config(self,config=None):
        if config is None:
            config = self.camera_config
        config_path = os.path.join(self.path, 'config.json')
        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
            print("Configuration saved successfully.")
        except Exception as e:
            print(f"Error saving configuration: {e}")

    def run(self):
        clear_screen()
        choice = welcome_message()
        if choice == 1:
            self.register_user_camera()
            input("Press any key to continue...")
        elif choice == 2:
            image_path = input("Enter the path to the image file: ").strip()
            self.register_user_image(image_path)
            input("Press any key to continue...")
        elif choice == 3:
            while True:
                choice = recognition_cli()
                if choice == 1:
                    self.real_time_recognition()
                    input("Press any key to continue...")
                elif choice == 2:
                    self.keypress_recognition()
                    input("Press any key to continue...")
                elif choice == 3:
                    break
                
        elif choice == 4:
            name,id = self.save.get_nameid()
            if (name,id,0) in self.data.labels:
                self.logs.append(f"User {name} with ID {id} exists in the database.")
            else:
                self.logs.append(f"User {name} with ID {id} does not exist in the database.")
            input("Press any key to continue...")
        elif choice == 5:
            try:
                tolerance = float(input("Enter the new confidence level in percentage (0.0 to 100.0): ").strip())
                if 0.0 <= tolerance <= 100.0:
                    self.tolerance = (100 - tolerance) / 100.0
                    self.logs.append(f"Confidence level set to {(1-self.tolerance)*100}%.")
                else:
                    self.logs.append("Invalid confidence level. It must be between 0.0 and 100.0.")
            except ValueError:
                self.logs.append("Invalid input. Please enter a number between 0.0 and 100.0.")
            input("Press any key to continue...")
        elif choice == 6:
            self.configure_camera()
        elif choice == 7:
            self.excel_operation()
        elif choice == 8:
            self.load_custom_excel()
            input("Press any key to continue...")
        elif choice == 9:
            self.logs.append("Exiting the application.")
            Camera.restore_defaults(self.cam_defaults)
            sys.exit(0)

    def register_user_camera(self):
        try:
            img = self.cam.capture_image(cam_defaults=self.cam_defaults)
            if img is None:
                self.logs.append("No image captured from camera.")
                return
        except RuntimeError as e:
            self.logs.append(f"Error capturing image: {e}")
            return
        self.register_faces(img)      

    def register_faces(self, img):
        face_locs = self.cam.get_face_locations(img)
        face_ens = self.cam.get_face_encodings(img, face_locs)
        if not face_ens:
            self.logs.append("No face encodings found.")
            return

        for en, loc in zip(face_ens, face_locs):
            try:
                img1 = img.copy()
                self.cam.put_rect(img1, loc)
                self.cam.show_image(img1)
                m_res = match(en,self.data)

                if m_res is not None:
                    if m_res[1] < self.tolerance:
                        choice = user_already_exists(m_res[0][0], m_res[0][1], m_res[1], self.show_confidence)
                        if choice == 1:
                            self.register_user(en, m_res[0][0], m_res[0][1])
                        elif choice == 2:
                            new_name, new_id = self.save.get_nameid()
                            self.update_existing_user(en, m_res[0][0], m_res[0][1], new_name, new_id)
                        else:
                            continue
                    else:
                        name, id = self.save.get_nameid()
                        self.register_user(en, name, id)
                else:
                    name, id = self.save.get_nameid()
                    self.register_user(en, name, id)
            except Exception as e:
                self.logs.append(f"Error registering user: {e}")
                continue

    def register_user(self, encoding, name, id):
        filename = self.save.get_filename(name, id)
        try:
            self.save.save(encoding, filename)
        except ValueError as e:
            self.logs.append(f"Error saving encoding: {e}")
            return
        self.data.append_new_data(encoding, name, id, 0)
        self.logs.append(f"User {name} with ID {id} registered successfully.")

    def update_existing_user(self, name, id, new_name, new_id):
        if new_id == id and new_name == name:
            self.logs.append("No changes made to the user.")
            return
        if not new_name or not new_id:
            self.logs.append("Name and ID cannot be empty.")
            return
        for file in os.listdir(self.path):
            if file.startswith(f"{name}_{id}_"):
                try:
                    dno = file.split('_')[-1]
                    os.rename(os.path.join(self.path, file), os.path.join(self.path, f"{new_name}_{new_id}_{dno}"))
                except ValueError as e:
                    self.logs.append(f"Error updating user: {e}")
        self.logs.append(f"User {name} with ID {id} updated successfully.")

    def register_user_image(self, image_path):
        if not os.path.exists(image_path):
            self.logs.append(f"Image file {image_path} does not exist.")
            return
        try:
            img = self.cam.img_read(image_path)
        except Exception as e:
            self.logs.append(f"Error processing image: {e}")
        self.register_faces(img)

    def keypress_recognition(self):
        try:
            img = self.cam.capture_image(cam_defaults=self.cam_defaults)
            if img is None:
                self.logs.append("No image captured from camera.")
                return
            
        except RuntimeError as e:
            self.logs.append(f"Error capturing image: {e}")
            return
        face_locs = self.cam.get_face_locations(img)
        face_ens = self.cam.get_face_encodings(img, face_locs)
        if not face_ens:
            self.logs.append("No face encodings found.")
            return
        for en, loc in zip(face_ens, face_locs):
            try:
                img1 = img.copy()
                self.cam.put_rect(img1, loc)
                self.cam.show_image(img1)
                m_res = match(en, self.data)

                if m_res is not None and m_res[1] < self.tolerance:
                    print(f"Recognized user: {m_res[0][0]} with ID {m_res[0][1]} and confidence {m_res[1]}")
                    if self.ex.write_to_excel(m_res[0][0], m_res[0][1], m_res[1], self.time_gap):
                        if self.show_confidence:
                            print(f"User {m_res[0][0]} with ID {m_res[0][1]} recognized with confidence {(1-m_res[1])*100:.2f}%.")
                        else:
                            print(f"User {m_res[0][0]} with ID {m_res[0][1]} recognized.")
            except Exception as e:
                self.logs.append(f"Error recognizing user: {e}")
                continue

    def recognise_user(self,ls_frame, stop_event,rec_users):
        while not stop_event.is_set():
            img = ls_frame.pop() if ls_frame else None
            if img is None:
                time.sleep(0.1)
                continue
            face_locs = Camera.get_face_locations(img)
            face_ens = Camera.get_face_encodings(img, face_locs)
            if not face_ens:
                self.logs.append("No face encodings found.")
                continue 
            for en in face_ens:
                try:
                    m_res = match(en, self.data)
                    if m_res is not None and m_res[1] < self.tolerance:
                        print(f"Recognized user: {m_res[0][0]} with ID {m_res[0][1]} and confidence {(1-m_res[1])*100:.2f}%")
                        rec_users.put((m_res[0][0], m_res[0][1], m_res[1], datetime.now().strftime("%d/%m/%Y - %H:%M:%S")))
                except Exception as e:
                    self.logs.append(f"Error recognizing user: {e}")
                    continue
            if len(ls_frame) > 20:
                del ls_frame[:10]

    def real_time_recognition(self):
        stop_event = mp.Event()
        ls_frame = mp.Manager().list()
        rec_users = mp.Queue()
        mp1 = mp.Process(target=self.recognise_user, args=(ls_frame,stop_event,rec_users))
        mp1.start()
        if self.config['camera_index'] not in self.cam_defaults:
            self.cam_defaults[self.config['camera_index']] = Camera.get_defaults(self.config['camera_index'])
        self.cam.capture_real_time(ls_frame, stop_event)
        mp1.join()
        while not rec_users.empty():
            user = rec_users.get()
            self.ex.write_to_excel(user[0], user[1], user[2], self.time_gap, user[3])

    def load_custom_excel(self):
        file_path = input("Enter the path to the custom Excel file: ").strip()
        if not os.path.exists(file_path):
            self.logs.append(f"File {file_path} does not exist.")
            return
        self.ex = excel(file_path)
        self.logs.append(f"Custom Excel file {file_path} loaded successfully.")

    def excel_operation(self):
        while True:
            choice = excel_menu()
            if choice == 1:
                self.query_entry_by_date(self.ex.get_row_number(input("Enter the ID of the User.")))
            elif choice == 2:
                self.query_entry_by_time_range(self.ex.get_row_number(input("Enter the ID of the User.")))
            elif choice == 3:
                self.query_all_entries_for_user(self.ex.get_row_number(input("Enter the ID of the User.")))
            elif choice == 4:
                self.create_entry_now(self.ex.get_row_number(input("Enter the ID of the User.")))
            elif choice == 5:
                self.create_entry_manual(self.ex.get_row_number(input("Enter the ID of the User.")))
            elif choice == 6:
                self.delete_entry(self.ex.get_row_number(input("Enter the ID of the User.")))
            elif choice == 7:
                break
            if choice != 7:
                input("Press Enter to continue...")

    def query_entry_by_date(self,c_row):
        if c_row is None:
            print("The user has no entries.")
            return
        date = input("Enter the date (dd/mm/yyyy): ").strip()
        if not self.ex.is_valid_date(date):
            print("Invalid date format. Please use dd/mm/yyyy.")
            return
        initial_time = date + " - 00:00:00"
        final_time = date + " - 23:59:59"
        entries = self.ex.get_entries_by_time_range(c_row,initial_time, final_time)
        count = 0
        if entries:
            print(f"Entries for {date}:")
            for entry in entries:
                if entry is None:
                    continue
                print(entry)
                count += 1
            print(f"Entries for {self.ex.read_excel(c_row, 2)} (ID = {self.ex.read_excel(c_row,1)}) : {count}")
        else:
            print(f"No entries found for {date}.")

    def query_entry_by_time_range(self,c_row):
        if c_row is None:
            print("The user has no entries.")
            return
        initial_time = input("Enter the initial time (dd/mm/yyyy - HH:MM:SS): ").strip()
        final_time = input("Enter the final time (dd/mm/yyyy - HH:MM:SS): ").strip()
        if not self.ex.is_valid_time(initial_time) or not self.ex.is_valid_time(final_time):
            print("Invalid time format. Please use dd/mm/yyyy - HH:MM:SS.")
            input("Press Enter to continue...")
            return
        entries = self.ex.get_entries_by_time_range(c_row,initial_time, final_time)
        count = 0
        if entries:
            print(f"Entries from {initial_time} to {final_time}:")
            for entry in entries:
                if entry is None:
                    continue
                print(entry)
                count += 1
            print(f"Entries for {self.ex.read_excel(c_row, 2)} (ID = {self.ex.read_excel(c_row,1)}) : {count}")
        else:
            print(f"No entries found between {initial_time} and {final_time}.")   

    def query_all_entries_for_user(self,c_row,index = False):
        if c_row is None:
            print("The user has no entries.")
            return
        if index:
            print("Index | Date and Time")
            print("---------------------")
        i = 0
        for cl in range(5,self.ex.ws.max_column+1):
            val = self.ex.read_excel(c_row,cl)
            if val is None:
                continue
            i+=1
            if index:
                print(f"{i} | {val}")
            else:
                print(val)
        if not index:
            print(f"Total entries for {self.ex.read_excel(c_row, 2)} (ID = {self.ex.read_excel(c_row,1)}) : {self.ex.read_excel(c_row,4)}")

    def create_entry_now(self,c_row):
        if c_row is None:
            print("The user has no entries.")
            return
        self.ex.increment_entry_count(c_row)
        self.ex.write_excel(c_row,self.ex.ws.max_column+1,self.ex.get_date_time_now())

    def create_entry_manual(self,c_row):
        if c_row is None:
            print("The user has no entries.")
            return
        dt = input("Enter the date and time (dd/mm/yyyy - HH:MM:SS): ").strip()
        if not self.ex.is_valid_time(dt):
            print("Invalid date/time format. Please use dd/mm/yyyy - HH:MM:SS.")
            input("Press Enter to continue...")
            return
        self.ex.increment_entry_count(c_row)
        self.ex.write_excel(c_row,self.ex.ws.max_column+1,dt)

    def delete_entry(self, c_row):
        if c_row is None:
            print("The user has no entries.")
            return
        self.query_all_entries_for_user(c_row, index=True)
        try:
            max_index = self.ex.read_excel(c_row, 4)
            if max_index is None or max_index < 1:
                print("No entries found for this user.")
                return
            index = int(input("Enter the index of the entry you want to delete: "))
            if index < 1 or index > max_index:
                print("Invalid index. Please try again.")
                return
            col = index + 4  # Adjust for the first four columns
            for cl in range(col, max_index + 4):
                self.ex.write_excel(c_row, cl, self.ex.read_excel(c_row, cl + 1))
            self.ex.ws.delete_cols(max_index + 4, 1)  # Delete the last column
            self.ex.write_excel(c_row, 4, max_index - 1)  # Decrement the entry count
            print("Entry deleted successfully.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"Error deleting entry: {e}")

    def configure_camera(self):
        cam_config = self.camera_config
        cam_defaults = self.cam_defaults.get(self.config['camera_index'], Camera.get_defaults(self.config['camera_index']))
        while True:
            choice = configure_camera_menu()
            if choice == 1:
                self.cam.capture_image(cam_config, cam_defaults=self.cam_defaults)
            elif choice == 2:
                cam_idx = input_int("Enter camera index: ", default=cam_config['camera_index'], range_min=0)
                if Camera.test_camera_idx(cam_idx):
                    cam_config['camera_index'] = cam_idx
                    self.logs.append(f"Camera index set to {cam_idx}.")
            elif choice == 3:
                width = input_int("Enter camera width: ", default=cam_config['camera_resolution'][0], range_min=1)
                height = input_int("Enter camera height: ", default=cam_config['camera_resolution'][1], range_min=1)
                if Camera.test_camera_resolution(cam_config,(width, height)):
                    cam_config['camera_resolution'] = (width, height)
                    self.logs.append(f"Camera resolution set to {width}x{height}.")
            elif choice == 4:
                fps = input_int("Enter camera frame rate: ", default=cam_config['camera_fps'], range_min=5)
                if Camera.test_camera_fps(cam_config, fps):
                    cam_config['camera_fps'] = fps
                    self.logs.append(f"Camera frame rate set to {fps} FPS.")
            elif choice == 5:
                focus = input_int("Enter camera focus (0 to 100): ", default=int(cam_config.get('camera_focus', 0)*100), range_min=-1, range_max=100)
                if focus >= 0:
                    cam_config['camera_focus'] = float(focus)/100
                    self.logs.append(f"Camera focus set to {focus}%.")
                else:
                    cam_config['camera_focus'] = -1
                    self.logs.append("Camera focus set to auto.")
            elif choice == 6:
                brightness = input_int("Enter camera brightness (0 to 100): ", default=int(cam_config['camera_brightness']*100), range_min=-1, range_max=100)
                if brightness < 0:
                    cam_config['camera_brightness'] = cam_defaults['camera_brightness']
                    self.logs.append("Camera brightness set to default value.")
                else:
                    cam_config['camera_brightness'] = float(brightness)/100
                    self.logs.append(f"Camera brightness set to {brightness}%.")
            elif choice == 7:
                contrast = input_int("Enter camera contrast (0 to 100): ", default=int(cam_config['camera_contrast']*100), range_min=-1, range_max=100)
                if contrast < 0:
                    cam_config['camera_contrast'] = cam_defaults['camera_contrast']
                    self.logs.append("Camera contrast set to default value.")
                else:
                    cam_config['camera_contrast'] = float(contrast)/100
                    self.logs.append(f"Camera contrast set to {contrast}%.")
            elif choice == 8:
                saturation = input_int("Enter camera saturation (0 to 100): ", default=int(cam_config['camera_saturation']*100), range_min=-1, range_max=100)
                if saturation < 0:
                    cam_config['camera_saturation'] = cam_defaults['camera_saturation']
                    self.logs.append("Camera saturation set to default value.")
                else:
                    cam_config['camera_saturation'] = float(saturation)/100
                    self.logs.append(f"Camera saturation set to {saturation}%.")
            elif choice == 9:
                exposure = input_int("Enter camera exposure (0 to 100): ", default=int(cam_config['camera_exposure']*100), range_min=-1, range_max=100)
                if exposure >= 0:
                    cam_config['camera_exposure'] = float(exposure)/100
                    self.logs.append(f"Camera exposure set to {exposure}%.")
                else:
                    cam_config['camera_exposure'] = -1
                    self.logs.append("Camera exposure set to auto.")
            elif choice == 10:
                gain = input_int("Enter camera gain (0 to 100): ", default=int(cam_config['camera_gain']*100), range_min=-1, range_max=100)
                if gain >= 0:
                    cam_config['camera_gain'] = float(gain)/100
                    self.logs.append(f"Camera gain set to {gain}%.")
                else:
                    cam_config['camera_gain'] = cam_defaults['camera_gain']
                    self.logs.append("Camera gain set to default value.")
            elif choice == 11:
                hue = input_int("Enter camera hue (0 to 100): ", default=int(cam_config.get('camera_hue', 0)*100), range_min=-1, range_max=100)
                if hue < 0:
                    cam_config['camera_hue'] = cam_defaults.get('camera_hue', 0)
                    self.logs.append("Camera hue set to default value.")
                else:
                    cam_config['camera_hue'] = float(hue)/100
                    self.logs.append(f"Camera hue set to {hue}%.")
            elif choice == 12:
                sharpness = input_int("Enter camera sharpness (0 to 100): ", default=int(cam_config.get('camera_sharpness', 0)*100), range_min=-1, range_max=100)
                if sharpness < 0:
                    cam_config['camera_sharpness'] = cam_defaults.get('camera_sharpness', 0)
                    self.logs.append("Camera sharpness set to default value.")
                else:
                    cam_config['camera_sharpness'] = float(sharpness)/100
                    self.logs.append(f"Camera sharpness set to {sharpness}%.")
            elif choice == 14:
                gamma = input_int("Enter camera gamma (0 to 100): ", default=int(cam_config.get('camera_gamma', 0)*100), range_min=-1, range_max=100)
                if gamma < 0:
                    cam_config['camera_gamma'] = cam_defaults.get('camera_gamma', 0)
                    self.logs.append("Camera gamma set to default value.")
                else:
                    cam_config['camera_gamma'] = float(gamma)/100
                    self.logs.append(f"Camera gamma set to {gamma}%.")
            elif choice == 13:
                wb = input_int("Enter camera white balance (0 to 100): ", default=int(cam_config.get('camera_white_balance', 0)*100), range_min=-1, range_max=100)
                if wb >= 0:
                    cam_config['camera_white_balance'] = float(wb)/100
                    self.logs.append(f"Camera white balance set to {wb}%.")
                else:
                    cam_config['camera_white_balance'] = -1
                    self.logs.append("Camera white balance set to auto.")
            elif choice == 15:
                ct = input_int("Enter camera color temperature (0 to 100): ", default=int(cam_config.get('camera_color_temperature', 0)*100), range_min=-1, range_max=100)
                if ct < 0:
                    cam_config['camera_color_temperature'] = -1
                    self.logs.append("Camera color temperature set to auto.")
                else:
                    cam_config['camera_color_temperature'] = float(ct)/100
                    self.logs.append(f"Camera color temperature set to {ct}%.")
            elif choice == 16:
                self.camera_config = cam_config
                self.config['camera_index'] = cam_config['camera_index']
                self.config['camera_resolution'] = cam_config['camera_resolution']
                self.config['camera_fps'] = cam_config['camera_fps']
                self.config['camera_focus'] = cam_config.get('camera_focus', 0)
                self.config['camera_brightness'] = cam_config['camera_brightness']
                self.config['camera_contrast'] = cam_config['camera_contrast']
                self.config['camera_saturation'] = cam_config['camera_saturation']
                self.config['camera_exposure'] = cam_config['camera_exposure']
                self.config['camera_gain'] = cam_config['camera_gain']
                self.config['camera_hue'] = cam_config.get('camera_hue', 0)
                self.config['camera_sharpness'] = cam_config.get('camera_sharpness', 0)
                self.config['camera_gamma'] = cam_config.get('camera_gamma', 0)
                self.config['camera_white_balance'] = cam_config.get('camera_white_balance', 0)
                self.config['camera_color_temperature'] = cam_config.get('camera_color_temperature', 0)
                self.save_config(self.config)
            if choice < 17:
                input("Press Enter to continue...")
            if choice == 17:
                return
            

if __name__ == "__main__":
    cli = CLI()
    while True:
        cli.run()
    