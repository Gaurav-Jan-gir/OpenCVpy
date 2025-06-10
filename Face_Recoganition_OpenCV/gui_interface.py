from tkinter import *
from tkinter import ttk
from gui_functions import *
from MatchData import match
from LoadData import loadData
from tkinter import filedialog

def dateWidget(frame, row, column, label_text, entry_width=20):
    label = Label(frame, text=label_text, font='consolas 12')
    label.grid(row=row, column=column)
    entry = Entry(frame, width=entry_width)
    entry.grid(row=row, column=column+1)
    return label, entry

def timeWidget(frame, row, column, label_text, entry_width=20):
    label = Label(frame, text=label_text, font='consolas 12')
    label.grid(row=row, column=column)
    entry = Entry(frame, width=entry_width)
    entry.grid(row=row, column=column+1)
    return label, entry

def validate_date(date_str):
    try:
        day, month, year = map(int, date_str.split('/'))
        if 1 <= day <= 31 and 1 <= month <= 12 and year > 0:
            return True
    except ValueError:
        pass
    return False

def validate_time(time_str):
    try:
        hour, minute = map(int, time_str.split(':'))
        if 0 <= hour < 24 and 0 <= minute < 60:
            return True
    except ValueError:
        pass
    return False

def open_img_file(master, width=350, height=350, row=0, column=0, rowspan=1, columnspan=1):
    # Fix the filetypes parameter syntax
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("BMP files", "*.bmp"),
            ("All files", "*.*")
        ]
    )
    
    if not file_path:
        print("No file selected.")
        return None,None
    
    try:
        image = resize_image(read_image(file_path), width, height)
        if image is not None:
            return image,cam_reg_gui_capture(
                Frame(master, width=40, height=17), 
                image, 
                row, column, 0, 0, rowspan, columnspan
            )
        else:
            print("Failed to load image")
            return None,None
    except Exception as e:
        print(f"Error processing image: {e}")
        return None,None

class mButtons:
    def __init__(self,frame):
        self.frame = frame
        self.buttons = {}
        self.bg = 'white'
        self.fg = 'black'
        self.font = 'consolas 16'
        self.bdrW = '4'
        self.padx = 10
        self.pady = 10
        

    def create_button(self,button_name,button_text,button_position, button_command=None,padding=[0,0]):
        self.buttons[button_name] = Button(self.frame, text=button_text, fg = self.fg, bg = self.bg, font = self.font, borderwidth=self.bdrW, command=button_command, padx=padding[0], pady=padding[1])
        self.grid(button_name, button_position)
    
    def grid(self,button_name,button_position,rowspan=1,columnspan=1):
        if button_name in self.buttons:
            self.buttons[button_name].grid(row=button_position[0], column=button_position[1],padx=self.padx, pady=self.pady,sticky="EW", rowspan=rowspan, columnspan=columnspan)

    def hide(self,button_name):
        if button_name in self.buttons:
            self.buttons[button_name].grid_remove()

    def create_buttons(self,buttons_text, buttons_position, buttons_command=None):
        for i in range(len(buttons_text)):
            self.create_button(f"btn{i}", buttons_text[i], buttons_position[i], buttons_command[i])

    def hide_all(self):
        for button in self.buttons:
            self.buttons[button].grid_remove()

class Widgets:
    def __init__(self, frame):
        self.frame = frame
        self.labels = []
        self.entries = []
        self.check_boxes = []
        self.scrollbars = []
        self.scales = []
        self.messages = []
        self.texts = []
        self.list_boxes = []
        self.frames = []
        self.camera_frames = []
        self.buttons = mButtons(self.frame)

    def clear_widgets(self,cap):
        for widget in self.labels+self.entries+self.check_boxes+self.scrollbars+self.scales+self.messages+self.texts+self.list_boxes+ self.frames + self.camera_frames:
            widget.grid_remove()
        self.labels.clear()
        self.entries.clear()
        self.texts.clear()
        self.check_boxes.clear()
        self.scrollbars.clear()
        self.scales.clear()
        self.buttons.hide_all()
        self.messages.clear()
        self.list_boxes.clear()
        self.frames.clear()
        destroy_camera(cap)
        self.camera_frames.clear()

class GUI:
    def __init__(self, root):
        self.root = root
        self.frame = ttk.Frame(root, padding=10)
        self.frame.grid(row=0, column=0, sticky="NS") 
        self.cap = [None] 
        self.control_flag = False
        self.latest_image = [None]
        self.faces = []
        self.locations = []
        self.encodings = []
        self.data = loadData()
        self.save_confidence = 0.4
        
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        for i in range(8):
            self.frame.rowconfigure(i, weight=1)
        self.frame.columnconfigure(0, weight=1) 
        self.widgets = Widgets(self.frame)

    def clear_frame(self):
        self.latest_image = [None]
        self.control_flag = False
        self.widgets.clear_widgets(self.cap)
        self.cap = [None]

    def clear_camera_frame(self):
        self.control_flag = False
        for camera_frame in self.widgets.camera_frames:
            camera_frame.grid_remove()
        destroy_camera(self.cap)
        self.widgets.camera_frames.clear()
        self.cap[0] = None

    def start_gui(self):
        root.title("Face Recognition")
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Face Recognition", font='consolas 24 bold'))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        buttons_text = ['Register', 'Recognize','Operate Data', 'Settings', 'Exit']
        buttons_position = [(1, 0), (2, 0), (3, 0), (4, 0),(5, 0)]
        buttons_command = [self.register_gui, self.recognize_gui, self.op_data ,self.config_gui, root.destroy]
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command)

    def register_gui(self):
        root.title("Register")
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Register", font='consolas 24 bold'))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        buttons_text = ['Camera Capture', 'Image', 'Check', 'Back']
        buttons_position = [(1, 0), (2, 0), (3, 0), (4, 0)]
        buttons_command = [self.cam_reg_gui, self.img_reg_gui, self.check_reg_gui, self.start_gui]
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command)

    def cam_reg_gui(self):
        root.title("Camera Capture")
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Camera Capture", font='consolas 24 bold'))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.control_flag = True
        try:
            cframe,self.latest_image = camera_frame(Frame(self.frame,width=40,height=17),self.cap, self.control_flag ,row=1, column=0, rowspan=4, columnspan=4)
            self.widgets.camera_frames.append(cframe)
        except Exception as e:
            self.widgets.texts.append(Text(self.frame, width=40, height=17))
            self.widgets.texts[-1].insert(END,f"\n\n\n\n\n\n\n\nError Acessing Camera : {e}\n\n\n\n\n\n\n\n")
            self.widgets.texts[-1].configure(font='consolas 12')
            self.widgets.texts[-1].configure(state=DISABLED)
            self.widgets.texts[-1].grid(row=1, column=0, columnspan=4,rowspan=4)
        self.widgets.labels.append(Label(self.frame,text='Enter Details',font = 'consolas 16'))
        self.widgets.labels[-1].grid(row = 1,column = 4, columnspan = 4)
        self.widgets.labels.append(Label(self.frame, text="Enter ID : ", font='consolas 12'))
        self.widgets.labels[-1].grid(column=5, row=2)
        self.widgets.entries.append(Entry(self.frame, width=30))
        self.widgets.entries[-1].grid(column=6, row=2)
        self.widgets.labels.append(Label(self.frame, text="Enter Name : ", font='consolas 12'))
        self.widgets.labels[-1].grid(column=5, row=3)
        self.widgets.entries.append(Entry(self.frame, width=30))
        self.widgets.entries[-1].grid(column=6, row=3)
        buttons_text = ['Register','Update','Capture','Recapture','Back','Main Menu']
        buttons_position = [(4, 5), (4, 6), (5, 1), (5, 2), (5, 5), (5, 6)]
        buttons_command = [self.reg_gui_register, self.reg_gui_update, self.cam_reg_gui_capture , self.cam_reg_gui_recapture, self.register_gui, self.start_gui]
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command)

    def cam_reg_gui_capture(self):
        if self.latest_image[0] is None:
            self.clear_status_messages(row=6, column=0)  # Clear messages at row 6, column 0
            message = "No image captured. Please recapture."
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font='consolas 12'))
            self.widgets.messages[-1].grid(column=0, row=6, columnspan=4)
            return
        self.faces,self.locations,self.encodings = get_cropped_faces_locations(self.latest_image[0])
        self.put_rectangle()
    
    def put_rectangle(self):
        if self.faces is not [None] and not len(self.faces)==0:
            image,self.matched = match_image(self.faces[-1], self.locations[-1], self.data, self.save_confidence,self.latest_image[0])
            self.clear_camera_frame()
            self.widgets.camera_frames.append(cam_reg_gui_capture(Frame(self.frame, width=40, height=17), image, row=1, column=0, rowspan=4, columnspan=4))
            if self.matched is not None:
                self.widgets.entries[0].delete(0, END)
                self.widgets.entries[0].insert(0, str(self.matched[1]))
                
                self.widgets.entries[1].delete(0, END)
                self.widgets.entries[1].insert(0, str(self.matched[0]))
            
            self.faces.pop()
            self.locations.pop()
        
    def cam_reg_gui_recapture(self):
        self.clear_camera_frame()
        self.faces.clear()
        self.locations.clear()
        self.control_flag = True
        cframe,self.latest_image = camera_frame(Frame(self.frame,width=40,height=17),self.cap, self.control_flag ,row=1, column=0, rowspan=4, columnspan=4)
        self.widgets.camera_frames.append(cframe)

    def reg_gui_register(self, imag_reg = False):
        if self.widgets.entries[0].get() == "" or self.widgets.entries[1].get() == "":
            self.clear_status_messages(row=6, column=0)  # Clear messages at row 6, column 0
            message = "Please enter both ID and Name."
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font='consolas 12'))
            self.widgets.messages[-1].grid(column=0, row=6, columnspan=4)
            return
        if len(self.encodings) == 0:
            return
        new_data,new_labels = save_image_data(self.encodings[-1],self.widgets.entries[1].get(), self.widgets.entries[0].get(), self.data, showConfidence=True, threshold_confidence=self.save_confidence)
        self.data.append_data_in_burst(new_data, new_labels)
        self.encodings.pop()
        if len(self.faces) != 0:
            self.put_rectangle()
        else:
            self.clear_status_messages(row=6, column=0)  # Clear messages at row 6, column 0
            message = "User Registered Successfully."
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font='consolas 12'))
            self.widgets.messages[-1].grid(column=0, row=6, columnspan=4) 
            if not imag_reg:
                self.cam_reg_gui_recapture()

    def reg_gui_update(self, imag_reg = False):
        if self.widgets.entries[0].get() == "" or self.widgets.entries[1].get() == "":
            self.clear_status_messages(row=6, column=0)  # Clear messages at row 6, column 0
            message = "Please enter both ID and Name."
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font='consolas 12'))
            self.widgets.messages[-1].grid(column=0, row=6, columnspan=4)
            return
        if len(self.encodings) == 0:
            return
        saveData.changeAllMatchData(self.matched[0],self.matched[1],self.widgets.entries[1].get(), self.widgets.entries[0].get())
        new_data,new_labels = save_image_data(self.encodings[-1],self.widgets.entries[1].get(), self.widgets.entries[0].get(), self.data, showConfidence=True, threshold_confidence=self.save_confidence)
        self.data.append_data_in_burst(new_data, new_labels)
        self.encodings.pop()
        if len(self.faces) != 0:
            self.put_rectangle()
        else:
            self.clear_status_messages(row=6, column=0)  # Clear messages at row 6, column 0
            message = "User Updated Successfully."
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font='consolas 12'))
            self.widgets.messages[-1].grid(column=0, row=6, columnspan=4) 
            if not imag_reg:
                self.cam_reg_gui_recapture()

    def img_reg_gui(self):
        root.title("Image Capture")
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Image Capture", font='consolas 24 bold'))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.widgets.texts.append(Text(self.frame, width=40, height=17))
        self.widgets.texts[-1].insert(END,"\n\n\n\n\n\n\n\n                 Image\n\n\n\n\n\n\n\n")
        self.widgets.texts[-1].configure(font='consolas 12')
        self.widgets.texts[-1].configure(state=DISABLED)
        self.widgets.texts[-1].grid(row=1, column=0, columnspan=4,rowspan=4)
        self.widgets.labels.append(Label(self.frame,text='Enter Details',font = 'consolas 16'))
        self.widgets.labels[-1].grid(row = 1,column = 4, columnspan = 4)
        self.widgets.labels.append(Label(self.frame, text="Enter ID : ", font='consolas 12'))
        self.widgets.labels[-1].grid(column=5, row=2)
        self.widgets.entries.append(Entry(self.frame, width=30))
        self.widgets.entries[-1].grid(column=6, row=2)
        self.widgets.labels.append(Label(self.frame, text="Enter Name : ", font='consolas 12'))
        self.widgets.labels[-1].grid(column=5, row=3)
        self.widgets.entries.append(Entry(self.frame, width=30))
        self.widgets.entries[-1].grid(column=6, row=3)
        self.widgets.buttons.create_button('sel_img', 'Select Image', (4, 0), self.sel_img)
        self.widgets.buttons.hide('sel_img')
        self.widgets.buttons.grid('sel_img', (5,1), rowspan=1, columnspan=3)
        buttons_text = ['Register','Update','Back','Main Menu']
        buttons_position = [(4, 5), (4, 6),  (5, 5), (5, 6)]
        buttons_command = [lambda: self.reg_gui_register(True), lambda : self.reg_gui_update(True), self.register_gui, self.start_gui]
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command)
    
    def sel_img(self):
        image,frame = open_img_file(self.frame, width=350, height=350, row=1, column=0, rowspan=4, columnspan=4)
        if image is not None and frame is not None:
            if len(self.widgets.texts) > 0:
                self.widgets.texts[-1].grid_remove()
                self.widgets.texts.pop()
            self.widgets.camera_frames.append(frame)
            self.latest_image[0] = image
            self.faces,self.locations,self.encodings = get_cropped_faces_locations(self.latest_image[0])
            self.put_rectangle()
        else:
            self.clear_status_messages(row=6, column=0)  # Clear messages at row 6, column 0
            message = "No image selected."
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font='consolas 12'))
            self.widgets.messages[-1].grid(column=0, row=6, columnspan=4)

    def check_reg_gui(self):
        root.title("Check Registration")
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Check Registration", font='consolas 24 bold'))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=4)
        self.widgets.labels.append(Label(self.frame, text="Enter ID : ", font='consolas 12'))
        self.widgets.labels[-1].grid(column=1, row=1)
        self.widgets.entries.append(Entry(self.frame, width=30))
        self.widgets.entries[-1].grid(column=2, row=1)
        self.widgets.labels.append(Label(self.frame, text="Enter Name : ", font='consolas 12'))
        self.widgets.labels[-1].grid(column=1, row=2)
        self.widgets.entries.append(Entry(self.frame, width=30))
        self.widgets.entries[-1].grid(column=2, row=2)
        self.widgets.messages.append(Message(self.frame, text="         ", width=200, font='consolas 12'))
        self.widgets.messages[-1].grid(column=0, row=3, columnspan=4)
        buttons_text = ['Check','Back','Main Menu']
        buttons_position = [(4, 1), (4, 2), (4, 3)]
        buttons_command = [self.check_registration, self.register_gui, self.start_gui]
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command)

    def check_registration(self):
        id_value = self.widgets.entries[0].get()
        name_value = self.widgets.entries[1].get()
        if id_value == "" or name_value == "":
            self.clear_status_messages(row=3, column=0)
            message = "Please enter both ID and Name."
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font='consolas 12'))
            self.widgets.messages[-1].grid(column=0, row=3, columnspan=4)
            return
        if check_registration(name_value, id_value):
            self.clear_status_messages(row=3, column=0)
            message = f"User {name_value} with ID {id_value} is registered."
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font='consolas 12'))
            self.widgets.messages[-1].grid(column=0, row=3, columnspan=4)
        else:
            self.clear_status_messages(row=3, column=0)
            message = f"User {name_value} with ID {id_value} is not registered."
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font='consolas 12'))
            self.widgets.messages[-1].grid(column=0, row=3, columnspan=4)

    def recognize_gui(self):
        root.title("Recognize")
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Recognize", font='consolas 24 bold'))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        buttons_text = ['Real-time Recognition', 'Keypress Recognition', 'Back']
        buttons_position = [(1, 0), (2, 0), (3, 0)]
        buttons_command = [self.real_time_rec_gui, self.keypress_rec_gui, self.start_gui]
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command)

    def real_time_rec_gui(self):
        root.title("Real-time Recognition")
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Real-time Recognition", font='consolas 24 bold'))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.widgets.texts.append(Text(self.frame, width=40, height=17))
        self.widgets.texts[-1].insert(END,"\n\n\n\n\n\n\n\n                 Camera\n\n\n\n\n\n\n\n")
        self.widgets.texts[-1].configure(font='consolas 12')
        self.widgets.texts[-1].configure(state=DISABLED)
        self.widgets.texts[-1].grid(row=1, column=0, columnspan=4,rowspan=4)
        self.widgets.labels.append(Label(self.frame,text='Last Recognised Users',font = 'consolas 16'))
        self.widgets.labels[-1].grid(row = 1,column = 4, columnspan = 2)
        self.widgets.texts.append(Text(self.frame, width = 30, height = 16))
        self.widgets.texts[-1].insert(END,"Name 1 : ID 1\nName 2 : ID 2\nName 3 : ID 3\n\n\n")
        self.widgets.texts[-1].configure(font='consolas 12')
        self.widgets.texts[-1].configure(state=DISABLED)
        self.widgets.texts[-1].grid(row = 2,column = 4,rowspan = 3, columnspan = 2)
        buttons_text = ['Start','Stop','Back', 'Main Menu']
        buttons_position = [(5,0),(5,1),(5, 2), (5, 4)]
        buttons_command = [lambda : print('Start') , lambda : print('Stop'), self.recognize_gui, self.start_gui]
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command)

    def keypress_rec_gui(self):
        root.title("Keypress Recognition")
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Keypress Recognition", font='consolas 24 bold'))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.widgets.texts.append(Text(self.frame, width=40, height=17))
        self.widgets.texts[-1].insert(END,"\n\n\n\n\n\n\n\n                 Camera\n\n\n\n\n\n\n\n")
        self.widgets.texts[-1].configure(font='consolas 12')
        self.widgets.texts[-1].configure(state=DISABLED)
        self.widgets.texts[-1].grid(row=1, column=0, columnspan=4,rowspan=4)
        self.widgets.labels.append(Label(self.frame,text='Last Recognised Users',font = 'consolas 16'))
        self.widgets.labels[-1].grid(row = 1,column = 4, columnspan = 2)
        self.widgets.buttons.create_button('reco', 'Recognize', (1 ,1), lambda: print("Recognize Button Pressed"))
        self.widgets.buttons.hide('reco')
        self.widgets.buttons.grid('reco', (5, 0), rowspan=1, columnspan=2)
        self.widgets.texts.append(Text(self.frame, width = 30, height = 16))
        self.widgets.texts[-1].insert(END,"Name 1 : ID 1\nName 2 : ID 2\nName 3 : ID 3\n\n\n")
        self.widgets.texts[-1].configure(font='consolas 12')
        self.widgets.texts[-1].configure(state=DISABLED)
        self.widgets.texts[-1].grid(row = 2,column = 4,rowspan = 3, columnspan = 2)
        buttons_text = ['back', 'main menu']
        buttons_position = [(5, 2), (5, 4)]
        buttons_command = [self.recognize_gui, self.start_gui]
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command)
    
    def op_data(self):
        root.title("Operate Data")
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Operate Data", font='consolas 24 bold'))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.widgets.labels.append(Label(self.frame, text="Enter ID : ", font='consolas 12'))
        self.widgets.labels[-1].grid(column=0, row=1)
        self.widgets.entries.append(Entry(self.frame, width=7))
        self.widgets.entries[-1].grid(column=1, row=1)
        buttons_text = ['Read Data', 'Write Data', 'Back']
        buttons_position = [ (2, 0), (3, 0),(4, 0)]
        buttons_command = [ self.read_data_gui, self.write_data_gui, self.start_gui]
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command)

    def read_data_gui(self):
        root.title("Read Data")
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Read Data", font='consolas 24 bold'))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.widgets.labels.append(Label(self.frame, text="Name : User1 ID :1", font='consolas 16'))
        self.widgets.labels[-1].grid(column=0, row=1, columnspan=2)
        buttons_text = ['Read On Date','Read on Time Range', 'Read all ','Back','Main Menu']
        buttons_position = [(2,0),(3,0),(4,0),(5,0),(6,0)]
        buttons_command = [ self.read_on_date_gui, self.read_on_time_range_gui, self.read_all_gui, self.op_data, self.start_gui]
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command)

    def read_on_date_gui(self):
        root.title("Read On Date")
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Read On Date", font='consolas 24 bold'))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.widgets.labels.append(Label(self.frame, text="Name : User1 ID :1", font='consolas 16'))
        self.widgets.labels[-1].grid(column=0, row=1, columnspan=2)
        self.widgets.texts.append(Text(self.frame, width = 40, height = 17))
        self.widgets.texts[-1].insert(END,'Date 1 - Time 1\nDate 2 - Time 2\nDate 3 - Time 3\n')
        self.widgets.texts[-1].configure(font = 'consolas 12')
        self.widgets.texts[-1].configure(state = DISABLED)
        self.widgets.texts[-1].grid(row=2, column=0, columnspan=3, rowspan=5)
        label_date, entry_date = dateWidget(self.frame, 7, 0, "Enter Date (DD/MM/YYYY):")
        self.widgets.labels.append(label_date)
        self.widgets.entries.append(entry_date)
        entry_date.grid(column=1, row=7, columnspan=2)
        buttons_text = ['Read','Back','Main Menu']
        buttons_position = [(8, 0), (8, 1), (8, 2)]
        buttons_command = [lambda: print("Read Button Pressed"), self.read_data_gui, self.start_gui]
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command)

    def read_on_time_range_gui(self):
        root.title("Read On Time Range")
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Read On Time Range", font='consolas 24 bold'))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.widgets.labels.append(Label(self.frame, text="Name : User1 ID :1", font='consolas 16'))
        self.widgets.labels[-1].grid(column=0, row=1, columnspan=2)
        self.widgets.texts.append(Text(self.frame, width = 40, height = 17))
        self.widgets.texts[-1].insert(END,'Date 1 - Time 1\nDate 2 - Time 2\nDate 3 - Time 3\n')
        self.widgets.texts[-1].configure(font = 'consolas 12')
        self.widgets.texts[-1].configure(state = DISABLED)
        self.widgets.texts[-1].grid(row=2, column=0, columnspan=3, rowspan=5)
        label_date_in, entry_date_in = dateWidget(self.frame, 7, 0, "Initial Date (DD/MM/YYYY):")
        label_time_in, entry_time_in = timeWidget(self.frame, 7, 2, "Time (HH:MM:SS):")
        self.widgets.labels.append(label_date_in)
        self.widgets.entries.append(entry_date_in)
        self.widgets.labels.append(label_time_in)
        self.widgets.entries.append(entry_time_in)
        label_date_out, entry_date_out = dateWidget(self.frame, 8, 0, "Final Date (DD/MM/YYYY):")
        label_time_out, entry_time_out = timeWidget(self.frame, 8, 2, "Time (HH:MM:SS):")
        self.widgets.labels.append(label_date_out)
        self.widgets.entries.append(entry_date_out)
        self.widgets.labels.append(label_time_out)
        self.widgets.entries.append(entry_time_out)
        buttons_text = ['Read','Back','Main Menu']
        buttons_position = [(9, 0), (9, 1), (9, 2)]
        buttons_command = [lambda: print("Read Button Pressed"), self.read_data_gui, self.start_gui]
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command)

    def read_all_gui(self):
        root.title("Read All Data")
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Read All Data", font='consolas 24 bold'))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.widgets.labels.append(Label(self.frame, text="Name : User1 ID :1", font='consolas 16'))
        self.widgets.labels[-1].grid(column=0, row=1, columnspan=2)
        self.widgets.texts.append(Text(self.frame, width = 40, height = 17))
        self.widgets.texts[-1].insert(END,'Date 1 - Time 1\nDate 2 - Time 2\nDate 3 - Time 3\n')
        self.widgets.texts[-1].configure(font = 'consolas 12')
        self.widgets.texts[-1].configure(state = DISABLED)
        self.widgets.texts[-1].grid(row=2, column=0, columnspan=3, rowspan=5)
        buttons_text = ['Back','Main Menu']
        buttons_position = [(7, 0), (7, 1)]
        buttons_command = [self.read_data_gui, self.start_gui]
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command)

    def write_data_gui(self):
        root.title("Write Data")
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Write Data", font='consolas 24 bold'))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.widgets.labels.append(Label(self.frame, text="Name : User1 ID :1", font='consolas 16'))
        self.widgets.labels[-1].grid(column=0, row=1, columnspan=2)
        buttons_text = ['Create Data','Delete Data','Back','Main Menu']
        buttons_position = [(2, 0), (3,0), (4, 0), (5, 0)]
        buttons_command = [self.create_entry_gui, self.delete_entry_gui, self.op_data, self.start_gui]
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command)

    def create_entry_gui(self):
        root.title("Create Entry")
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Create Entry", font='consolas 24 bold'))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.widgets.labels.append(Label(self.frame, text="Name : User1 ID :1", font='consolas 16'))
        self.widgets.labels[-1].grid(column=0, row=1, columnspan=2)
        date_label, date_entry = dateWidget(self.frame, 2, 0, "Enter Date (DD/MM/YYYY):")
        time_label, time_entry = timeWidget(self.frame, 2, 2, "Enter Time (HH:MM:SS):")
        self.widgets.labels.append(date_label)
        self.widgets.entries.append(date_entry)
        self.widgets.labels.append(time_label)
        self.widgets.entries.append(time_entry)
        buttons_text = ['Now','Create','Back','Main Menu']
        buttons_position = [(3, 0),(3,1), (3, 2), (3, 3)]
        buttons_command = [lambda: print("Now Button Pressed"), lambda: print("Create Entry Button Pressed"), self.write_data_gui, self.start_gui]
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command)

    def delete_entry_gui(self):
        root.title("Delete Entry")
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Delete Entry", font='consolas 24 bold'))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.widgets.labels.append(Label(self.frame, text="Name : User1 ID :1", font='consolas 16'))
        self.widgets.labels[-1].grid(column=0, row=1, columnspan=2)
        
        
        self.widgets.frames.append(Frame(self.frame))
        self.widgets.frames[-1].grid(column=0, row=4, columnspan=2, sticky='ew')
        self.widgets.scrollbars.append(Scrollbar(self.widgets.frames[-1], orient=VERTICAL))
        self.widgets.scrollbars[-1].pack(side=RIGHT, fill=Y)
        self.widgets.list_boxes.append(Listbox(self.widgets.frames[-1], width=50, height=10 , font='consolas 12', selectmode=MULTIPLE, yscrollcommand=self.widgets.scrollbars[-1].set)) 
        self.widgets.list_boxes[-1].insert(END, "Date 1 - Time 1")
        self.widgets.list_boxes[-1].insert(END, "Date 2 - Time 2")
        self.widgets.list_boxes[-1].insert(END, "Date 3 - Time 3")
        self.widgets.list_boxes[-1].insert(END, "Date 1 - Time 1")
        self.widgets.list_boxes[-1].insert(END, "Date 2 - Time 2")
        self.widgets.list_boxes[-1].insert(END, "Date 3 - Time 3")
        self.widgets.list_boxes[-1].insert(END, "Date 1 - Time 1")
        self.widgets.list_boxes[-1].insert(END, "Date 2 - Time 2")
        self.widgets.list_boxes[-1].insert(END, "Date 3 - Time 3")
        self.widgets.list_boxes[-1].insert(END, "Date 1 - Time 1")
        self.widgets.list_boxes[-1].insert(END, "Date 2 - Time 2")
        self.widgets.list_boxes[-1].insert(END, "Date 3 - Time 3")
        
        self.widgets.list_boxes[-1].pack(side=LEFT, fill=BOTH, expand=True)
        buttons_text = ['Delete','Back','Main Menu']
        buttons_position = [(5, 0), (5,1), (5, 2)]
        buttons_command = [ lambda: print("Delete Entry Button Pressed"), self.write_data_gui, self.start_gui]
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command)

    def config_gui(self):
        root.title("Settings")
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Settings", font='consolas 24 bold'))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        buttons_text = ['Confidence','Load Data','Back']
        buttons_position = [(1, 0), (2, 0), (3, 0)]
        buttons_command = [self.config_conf_gui, self.config_load_gui, self.start_gui]
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command)
    
    def config_conf_gui(self):
        root.title("Confidence Settings")
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Confidence Settings", font='consolas 24 bold'))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.widgets.check_boxes.append(Checkbutton(self.frame, text="Show Confidence", font='consolas 16'))
        self.widgets.check_boxes[-1].select()
        self.widgets.check_boxes[-1].grid(column=0, row=1, columnspan=2)
        self.widgets.labels.append(Label(self.frame, text="Save Confidence Threshold", font='consolas 16'))
        self.widgets.labels[-1].grid(column=0, row=2, columnspan=1)
        self.widgets.scales.append(Scale(self.frame, orient='horizontal'))
        self.widgets.scales[-1].set(60)
        self.widgets.scales[-1].grid(column=1, row=2, columnspan=1, sticky='ew')
        self.widgets.labels.append(Label(self.frame, text="Match Confidence Threshold", font='consolas 16'))
        self.widgets.labels[-1].grid(column=0, row=3, columnspan=1)
        self.widgets.scales.append(Scale(self.frame, orient='horizontal'))
        self.widgets.scales[-1].set(60)
        self.widgets.scales[-1].grid(column=1, row=3, columnspan=1, sticky='ew')
        buttons_text = ['Save','Back','Main Menu']
        buttons_position = [(4, 0), (4, 1), (4, 2)]
        buttons_command = [lambda: print("Save Button Pressed"), self.config_gui, self.start_gui]
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command)

    def config_load_gui(self):
        root.title("Load Data Settings")
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Load Data Settings", font='consolas 24 bold'))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.widgets.buttons.create_button('load', 'Load Data', (1 ,1), lambda: print("Load Data Button Pressed"))
        self.widgets.buttons.hide('load')
        self.widgets.buttons.grid('load', (1, 0), rowspan=1, columnspan=3)
        buttons_text = ['Save','Back','Main Menu']
        buttons_position = [(4, 0), (4, 1), (4, 2)]
        buttons_command = [lambda: print("Save Button Pressed"), self.config_gui, self.start_gui]
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command)

    def clear_status_messages(self, row=None, column=None, clear_all=False):
        """
        Clear status messages based on grid position
        
        Args:
            row: Specific row to clear (None = any row)
            column: Specific column to clear (None = any column)
            clear_all: If True, clear all messages regardless of position
        """
        i = 0
        while i < len(self.widgets.messages):
            try:
                if clear_all:
                    # Clear all messages
                    self.widgets.messages[i].grid_remove()
                    self.widgets.messages.pop(i)
                    continue
                
                grid_info = self.widgets.messages[i].grid_info()
                msg_row = grid_info.get('row')
                msg_column = grid_info.get('column')
                
                # Check if message matches the criteria
                should_clear = True
                
                if row is not None and msg_row != row:
                    should_clear = False
                
                if column is not None and msg_column != column:
                    should_clear = False
                
                if should_clear:
                    self.widgets.messages[i].grid_remove()
                    self.widgets.messages.pop(i)
                else:
                    i += 1
                    
            except:
                # If grid_info fails, move to next message
                i += 1

root = Tk()
root.geometry("1280x720")

gui = GUI(root)
gui.start_gui()

# frm = ttk.Frame(root)
# frm.grid(row=0, column=0, sticky="NS")












root.mainloop()
