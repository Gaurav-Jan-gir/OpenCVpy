from multiprocessing import Process, Queue
import os
from MatchData import match
from SaveData import saveData
from LoadData import loadData
from camera import Camera
from interFace_msg import message
from excel_handle import Excel_handle
import json
from capture_camera_frames import Capture_camera_frames as ccf
import sys

def get_safe_data_path():
    base_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'data')
    os.makedirs(data_path, exist_ok=True)
    return data_path
class interFace:
    def __init__(self, excel_path, config_path):
        self.path = get_safe_data_path()
        os.makedirs(self.path, exist_ok=True)  # Extra safety
        self.config = self.load_config(config_path)
        self.load_data = loadData()
        self.confidence_match = self.config["confidence_match"]
        self.save_confidence = self.config["confidence_save"]
        self.showConfidence = self.config["show_confidence"]
        if excel_path is None:
            excel_path = os.path.join(self.path,'data.xlsx')
        self.ex = Excel_handle(excel_path)
        self.run(config_path)

    def run(self,config_path):
        while True:
            print("Welcome to the face recognition system")
            print("1. Register a new user via Camera")
            print("2. Register a new user via Image")
            print("3. Start Recognition")
            print("4. Check if User Data exist or not.")
            print("5. Configure Confidence Levels (Default 60%)")
            print("6. Operate on data in Excel.")
            print("7. Load Custom Excel File")
            print("8. Exit")
            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                input("Press any key to continue...")
                self.clear_screen()
                continue

            if choice == 1:
                self.registerViaCamera()
            elif choice == 2:
                imag = input("Enter the path of the image: ")
                self.registerViaImage(imag)
            elif choice == 3:
                self.recognize()
            elif choice == 4:
                if self.is_valid_path(os.path.join(self.path,f'{input("Enter User Name ")}_{input("Enter User ID ")}_0.npy')):
                    print("The User Data Exists. ")
                else:
                    print("The User Data does not exist.")
                print()
                input("Press any key to continue...")
                self.clear_screen()
            elif choice==5:
                self.configureConfidence()
                self.config["confidence_match"] = self.confidence_match
                self.config["confidence_save"] = self.save_confidence
                self.config["show_confidence"] = self.showConfidence
                self.save_config(self.config,config_path)
            elif choice == 6:
                self.operate_excel()

            elif choice == 7:
                self.load_custom_excel()
                
            elif choice==8:
                print("Exiting program...")
                return
            else:
                print("Invalid choice")
                input("Press any key to continue...")
                self.clear_screen()

    def registerViaCamera(self):
        cam = Camera()
        cam.capture()
        cam.destroy()
        if cam.isSaved:
            self.registerViaImage(os.path.join(self.path, 'temp.jpg'))
        else:
            self.clear_screen()

    def registerViaImage(self, image_path):
        if not os.path.exists(image_path):
            message("Image file does not exist. Please provide a valid image path.", input_key=True)
            return
        saveStatus = saveData(image_path,self.load_data,self.showConfidence,self.save_confidence)
        if saveStatus.flag != 0:
            print("User registered successfully")
            if saveStatus.flag == 1 or saveStatus.flag == 2:
                self.load_data.append_data_in_burst(saveStatus.new_data, saveStatus.new_labels)
            else:
                self.load_data = loadData() 
        message("", input_key=True)
        return

    def recognize(self):
        print("🎥 Select Recognition Mode:")
        print("1. Real-time Recognition (Continuous Camera Feed)")
        print("2. Recognition by Capturing Frames on Key Press")
        print("Press any other key to Go Back to Main Menu")

        choice = input("Enter your choice: ")

        tg = None
        while tg is None:
            try:
                tg = int(input("Enter time (seconds) for valid duplicate gap (recognition logic): "))
                if tg <= 0:
                    print("Time must be a positive integer. Please try again.")
                    tg = None
            except ValueError:
                print("Invalid input. Please enter a number.")

        if choice == '1':
            self.real_time_recognition(tg)
        elif choice == '2':
            self.capture_on_keypress(tg)
        else:
            return

    def capture_on_keypress(self, tg):
        print("Starting Recognition... Press 's' to save, 'q' to quit.")
        cam = Camera()  # Create camera ONCE outside the loop
        try:
            while True:
                cam.capture()
                if cam.isSaved:
                    cropped_faces, cropped_face_locations = Camera.crop_face(os.path.join(self.path, 'temp.jpg'))
                    for cropped_face, location in zip(cropped_faces, cropped_face_locations):
                        matched = match(Camera.convert_to_rgb(cropped_face),self.load_data)
                        if matched is not None and matched[3] < self.confidence_match:
                            try:
                                self.ex.write_to_excel(matched[0], matched[1], matched[3],tg)   
                            except PermissionError as e:
                                print(f"Permission Error: {e}. Please close the Excel file and try again.")
                                input("Press any key to continue...")
                                return
                else:
                    break  # Exit if user pressed 'q'
        finally:
            cam.destroy()  # ✅ Always cleanup camera
            if cam.isSaved:
                os.remove(os.path.join(self.path, 'temp.jpg'))

    def real_time_recognition(self,tg):
        try:
            fps = int(input("Enter the frames per second for capturing frames: "))
            if fps <= 0:
                print("FPS must be a positive integer. Using default FPS of 30.")
                fps = 30
        except ValueError:
            print("Invalid input. Using default FPS of 30.")
            fps = 30

        q = Queue()
        q_r = Queue()
        c_i = ccf()
        p1 = Process(target=c_i.run, args=(fps,q))
        p2 = Process(target=self.recognize_from_frames, args=(tg, q, q_r))

        p1.start()
        p2.start()

        done = False
        while not done:
            item = q_r.get()
            if item[0] == 'done':
                done = True
            else:
                _, name, user_id, confidence, tg_val, date_time = item
                try:
                    self.ex.write_to_excel(name, user_id, confidence, tg_val, date_time)
                except PermissionError as e:
                    print(f"⚠️ Permission Error: {e}. Please close the Excel file and try again.")
                    input("Press any key to continue...")
                    return
        

        p1.join()
        p2.join()   
        self.ex.wb.save(os.path.join(self.path, 'data.xlsx'))

    def recognize_from_frames(self, tg, q, q_r):    
        while True:

            image_path = q.get()
            if image_path == 'q':
                q_r.put(('done',))
                break
            

            if not os.path.exists(image_path):
                print(f"Image {image_path} does not exist. Skipping...")
                continue

            result = Camera.crop_face(image_path)
            if not result:
                continue
            cropped_faces, cropped_locations = result
            img,date,time,idx = os.path.basename(image_path).split('_')
            date = date[6:] + '/' + date[4:6] + '/' + date[:4]
            time = time[:2] + ':' + time[2:4] + ':' + time[4:]

            for face_img, location in zip(cropped_faces, cropped_locations):
                matched = match(Camera.convert_to_rgb(face_img),self.load_data)
                if matched and matched[3] < self.confidence_match:
                    q_r.put(('excel', matched[0], matched[1], matched[3], tg, f"{date} - {time}"))

            try:
                os.remove(image_path)
            except Exception as e:
                print(f"⚠️ Warning: Couldn't delete {image_path}: {e}")


    def configureConfidence(self):
        while True:
            self.clear_screen()
            print("Select the item you want to configure.")
            print("1.Change Whether to Show Confidence or not.")
            print("2.Change Confidence for Recoganising (Matching)")
            print("3.Change Confidence for Saving (Registering)")
            print("4.Go Back to Main Menu")

            choice = input("Enter your choice: ")
            if choice == '1':
                self.showConfidence = not self.showConfidence
                print(f"Show Confidence is now set to {self.showConfidence}")
            elif choice == '2':
                try:
                    confidence = float(input("Enter the new confidence level for recognition in percentage: "))
                    if 0 <= confidence <= 100:
                        self.confidence_match = (100-confidence)/100
                        print(f"Recognition confidence set to {confidence:.2f}%")
                    else:
                        print("Invalid confidence level. Please enter a value between 0 and 100.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            elif choice == '3':
                try:
                    confidence = float(input("Enter the new confidence level for saving in percentage: "))
                    if 0 <= confidence <= 100:
                        self.save_confidence = (100-confidence)/100
                        print(f"Saving confidence set to {confidence:.2f}%")
                    else:
                        print("Invalid confidence level. Please enter a value between 0 and 100.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            elif choice == '4':
                return
            else:
                print("Invalid choice")
            input("Press any key to continue...")

    def is_valid_path(self, path):
        return os.path.exists(path) and os.path.isfile(path)
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def load_config(self,config_path=None):
        default_config = {
            "confidence_match": 0.3,
            "confidence_save": 0.3,
            "show_confidence": True
        }
        if config_path is None:
            config_path = os.path.join(self.path, 'config.json')
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"Error loading config: {e}")
        return default_config

    def save_config(self,config, config_path='config.json'):
        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
        
    def operate_excel(self):
        while True:
            self.clear_screen()
            print("📄 Excel Operations Menu")
            print("------------------------")
            print("1. Check user entry on a specific date")
            print("2. Check user entries in a time range")
            print("3. Get all entries of a user")
            print("4. Manually create user entry with current date/time")
            print("5. Manually create user entry with manual date/time")
            print("6. Delete a user entry") 
            print("7. Back to Main Menu")
            
            choice = input("Enter your choice: ").strip()
            if choice == '1':
                self.query_entry_by_date(self.ex.get_row_number(input("Enter the ID of the User.")))
            elif choice == '2':
                self.query_entry_by_time_range(self.ex.get_row_number(input("Enter the ID of the User.")))
            elif choice == '3':
                self.query_all_entries_for_user(self.ex.get_row_number(input("Enter the ID of the User.")))
            elif choice == '4':
                self.create_entry_now(self.ex.get_row_number(input("Enter the ID of the User.")))
            elif choice == '5':
                self.create_entry_manual(self.ex.get_row_number(input("Enter the ID of the User.")))
            elif choice == '6':
                self.delete_entry(self.ex.get_row_number(input("Enter the ID of the User.")))
            elif choice == '7':
                break
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")
            print()
            input("Press Enter to Continue...")

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
        

    def load_custom_excel(self):
        excel_path = input("Enter the path to the Excel file: ").strip()
        if not os.path.exists(excel_path):
            print("File does not exist. Please provide a valid path.")
            return
        self.ex = Excel_handle(excel_path)
        print("Excel file loaded successfully.")