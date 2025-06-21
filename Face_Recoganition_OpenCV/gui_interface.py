from tkinter import *
from tkinter import ttk
from gui_functions import *
from LoadData import loadData
from tkinter import filedialog
import json
from excel_handle import Excel_handle
from multiprocessing import Process, Queue, Manager
import shutil
from dynamic_size import DynamicSize as ds

def dateWidget(frame, row, column, label_text, entry_width=20):
    label = Label(frame, text=label_text)
    label.grid(row=row, column=column)
    entry = Entry(frame, width=entry_width)
    entry.grid(row=row, column=column+1)
    return label, entry
def timeWidget(frame, row, column, label_text, entry_width=20):
    label = Label(frame, text=label_text)
    label.grid(row=row, column=column)
    entry = Entry(frame, width=entry_width)
    entry.grid(row=row, column=column+1)
    return label, entry
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
def open_xlsx_file():
    file_path = filedialog.askopenfilename(
        title="Select an Excel File",
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
    )
    
    if not file_path:
        print("No file selected.")
        return None
    
    try:
        excel_handle = Excel_handle(file_path)
        return excel_handle
    except Exception as e:
        print(f"Error opening Excel file: {e}")
        return None
class keyBind:
    def __init__(self, root):
        self.root = root
        self.bindings = {}

    def bind_key(self, button, key):
        if not key:
            return
        self.bindings[key.lower()] = button
        self.root.bind(f'<Key-{key.lower()}>', lambda event: self.conditional_invoke(event,button))
        self.root.bind(f'<Key-{key.upper()}>', lambda event: self.conditional_invoke(event,button))

    def conditional_invoke(self, event, button):
        if isinstance(event.widget, (Entry, Text)):
            # If the event is from an Entry or Text widget, do not invoke the button
            return
        button.invoke()  # Invoke the button's command

    def unbind_key(self, key):
        if not key:
            return
        if key.lower() in self.bindings:
            self.root.unbind(f'<Key-{key.lower()}>')
            self.root.unbind(f'<Key-{key.upper()}>')
            del self.bindings[key.lower()]

    def unbind_all(self):
        for key in list(self.bindings.keys()):
            self.unbind_key(key)
class mButtons:
    def __init__(self,frame,fs):
        self.frame = frame
        self.buttons = {}
        self.bg = 'white'
        self.fg = 'black'
        self.fs = fs
        self.font = f'consolas {fs.get_button_text_size()}'
        self.bdrW = '4'
        self.padx = 10
        self.pady = 10
        # Use the toplevel window for key bindings
        self.key_binds = keyBind(frame.winfo_toplevel())

    def create_button(self,button_name,button_text,button_position, button_command=None,padding=[0,0], key_bind=None):
        self.font = self.fs.get_button_font()
        if key_bind is None:
            index = -1
        else:
            index = button_text.lower().find(key_bind)
        # Always create the button, underline only if found
        self.buttons[button_name] = Button(
            self.frame, text=button_text, fg=self.fg, bg=self.bg, font=self.font,
            borderwidth=self.bdrW, command=button_command, padx=padding[0], pady=padding[1], underline=index
        )
        if key_bind is not None and index != -1:
            self.key_binds.bind_key(self.buttons[button_name], key_bind)
        self.grid(button_name, button_position)

    def grid(self,button_name,button_position,rowspan=1,columnspan=1):
        if button_name in self.buttons:
            self.buttons[button_name].grid(row=button_position[0], column=button_position[1],padx=self.padx, pady=self.pady,sticky="EW", rowspan=rowspan, columnspan=columnspan)

    def hide(self,button_name):
        if button_name in self.buttons:
            self.buttons[button_name].grid_remove()
            # Unbind using the key if underline is set, else do nothing
            underline_index = self.buttons[button_name].cget('underline')
            if underline_index != -1:
                key = self.buttons[button_name].cget('text')[underline_index]
                self.key_binds.unbind_key(key)

    def create_buttons(self,buttons_text, buttons_position,buttons_command=[],key_bindings=[]):
        if len(buttons_command) == 0:
            buttons_command = [None] * len(buttons_text)
        if len(key_bindings) == 0:
            key_bindings = [None] * len(buttons_text)
        for i in range(len(buttons_text)):
            self.create_button(f"btn{i}", buttons_text[i], buttons_position[i], buttons_command[i],key_bind = key_bindings[i])

    def hide_all(self):
        for button in self.buttons:
            self.buttons[button].grid_remove()
        self.key_binds.unbind_all()
        self.buttons.clear()  # Remove all button references
class Widgets:
    def __init__(self, frame,fs):
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
        self.buttons = mButtons(self.frame,fs)

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
        self._resize_pending = False
        self._last_width = root.winfo_width()
        self._last_height = root.winfo_height()
        self.root.bind('<Configure>', self.on_configure)
        self.frame = ttk.Frame(root, padding=10)
        self.frame.grid(row=0, column=0, sticky="NS") 
        self.path = get_safe_data_path()
        self.cap = [None] 
        self.control_flag = False
        self.latest_image = [None]
        self.faces = []
        self.locations = []
        self.encodings = []
        self.data = loadData()
        self.config_path = os.path.join(self.path, 'config.json')
        self.config = self.load_config(self.config_path)
        self.confidence_match = self.config["confidence_match"]
        self.save_confidence = self.config["confidence_save"]
        self.showConfidence = self.config["show_confidence"]
        self.tg = self.config["time_gap"]
        self.ex = Excel_handle(os.path.join(self.path,'data.xlsx'))
        self.fps = 30 
        self.root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        self.fs = ds(root)
        for i in range(8):
            self.frame.rowconfigure(i, weight=1)
        self.frame.columnconfigure(0, weight=1) 
        self.widgets = Widgets(self.frame,self.fs)
        self.active_gui = None
        self.retrieve_data = {
            'entries': [],
            'texts': [],
            'messages': [],
            'check_boxes': [],
            'scales': [],
            'list_boxes': [],
            'scrollbars': []
        }

    def exit_gui(self, event=None):  # Accept event argument for key binding
        new_root = Toplevel(self.root)
        new_root.title("Exit Confirmation")
        new_root.grab_set()
        new_root.focus_set()
        new_root.resizable(False, False)
        new_frame = ttk.Frame(new_root, padding=10)
        new_frame.grid(row=0, column=0, sticky="NS")
        label = Label(new_frame, text="Are you sure you want to exit?", font=self.fs.get_main_label_font())
        label.grid(row=0, column=0, columnspan=2)
        yes_button = Button(new_frame, text="Yes", command=self.root.quit, font=self.fs.get_button_font())
        yes_button.grid(row=1, column=0, padx=10, pady=10)
        no_button = Button(new_frame, text="No", command=new_root.destroy, font=self.fs.get_button_font())
        no_button.grid(row=1, column=1, padx=10, pady=10)

        parent_x = self.root.winfo_rootx()
        parent_y = self.root.winfo_rooty()
        parent_w = self.root.winfo_width()
        parent_h = self.root.winfo_height()

        w = new_root.winfo_width()
        h = new_root.winfo_height()
        x = parent_x + (parent_w)//2 - w//2
        y = parent_y + (parent_h)//2 - h//2
        new_root.geometry(f"+{x}+{y}")

        new_root.bind("<Escape>", lambda e: new_root.destroy())
        new_root.bind("<Return>", lambda e: self.root.quit())


    def load_config(self,config_path=None):
        default_config = {
            "confidence_match": 0.4,
            "confidence_save": 0.4,
            "show_confidence": False,
            "time_gap": 3600
        }
        if config_path is None:
            config_path = self.config_path
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"Error loading config: {e}")
        return default_config

    def save_config(self,config, config_path=None):
        if config_path is None:
            config_path = self.config_path
        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

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

    def on_configure(self, event):
        # Only refresh if the window size has changed
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        if (width != self._last_width) or (height != self._last_height):
            self._last_width = width
            self._last_height = height
            if not self._resize_pending:
                self._resize_pending = True
                self.root.after(100, self.refresh_frame)

    def refresh_frame(self,event = None):
        print("Refreshing frame...")
        self._resize_pending = False
        self.fs.on_resize(event)
        self.back_up_current_frame_data()
        if self.active_gui == 'start_gui':
            self.start_gui()
        elif self.active_gui == 'register_gui':
            self.register_gui()
        elif self.active_gui == 'cam_reg_gui':
            self.cam_reg_gui()
        elif self.active_gui == 'img_reg_gui':
            self.img_reg_gui()
        elif self.active_gui == 'check_reg_gui':
            self.check_reg_gui()
        elif self.active_gui == 'recognize_gui':
            self.recognize_gui()
        elif self.active_gui == 'real_time_rec_gui':
            self.real_time_rec_gui()
        elif self.active_gui == 'keypress_rec_gui':
            self.keypress_rec_gui()
        self.restore_frame_data()

    def back_up_current_frame_data(self):
        for key in self.retrieve_data:
            self.retrieve_data[key].clear()
        for entry in self.widgets.entries:
            self.retrieve_data['entries'].append(entry.get())
        for text in self.widgets.texts:
            self.retrieve_data['texts'].append(text.get("1.0", END).strip())
        for message in self.widgets.messages:
            self.retrieve_data['messages'].append(message.cget("text").strip())
        for check_box in self.widgets.check_boxes:
            self.retrieve_data['check_boxes'].append(check_box.get())
        for scale in self.widgets.scales:
            self.retrieve_data['scales'].append(scale.get())
        for list_box in self.widgets.list_boxes:
            self.retrieve_data['list_boxes'].append(list_box.get(0, END))
        for scrollbar in self.widgets.scrollbars:
            self.retrieve_data['scrollbars'].append(scrollbar.get())

    def restore_frame_data(self):
        for i, entry in enumerate(self.widgets.entries):
            if i < len(self.retrieve_data['entries']):
                entry.delete(0, END)
                entry.insert(0, self.retrieve_data['entries'][i])
        for i, text in enumerate(self.widgets.texts):
            if i < len(self.retrieve_data['texts']):
                text.delete("1.0", END)
                text.insert("1.0", self.retrieve_data['texts'][i])
        for i, message in enumerate(self.widgets.messages):
            if i < len(self.retrieve_data['messages']):
                message.config(text=self.retrieve_data['messages'][i])
        for i, check_box in enumerate(self.widgets.check_boxes):
            if i < len(self.retrieve_data['check_boxes']):
                check_box.set(self.retrieve_data['check_boxes'][i])
        for i, scale in enumerate(self.widgets.scales):
            if i < len(self.retrieve_data['scales']):
                scale.set(self.retrieve_data['scales'][i])
        for i, list_box in enumerate(self.widgets.list_boxes):
            if i < len(self.retrieve_data['list_boxes']):
                list_box.delete(0, END)
                list_box.insert(END, *self.retrieve_data['list_boxes'][i])
        for i, scrollbar in enumerate(self.widgets.scrollbars):
            if i < len(self.retrieve_data['scrollbars']):
                scrollbar.set(*self.retrieve_data['scrollbars'][i])

    def start_gui(self):
        root.title("Face Recognition")
        self.active_gui = 'start_gui'
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Face Recognition", font=self.fs.get_main_label_font()))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        buttons_text = ['Register', 'Recognize','Operate Data', 'Settings', 'Exit']
        buttons_position = [(1, 0), (2, 0), (3, 0), (4, 0),(5, 0)]
        buttons_command = [self.register_gui, self.recognize_gui, self.op_data ,self.config_gui, root.destroy]
        key_bindings = ['r', 'n', 'o', 's', 'e']  # Key bindings for buttons
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command, key_bindings)

    def register_gui(self):
        root.title("Register")
        self.active_gui = 'register_gui'
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Register", font=self.fs.get_main_label_font()))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        buttons_text = ['Camera Capture', 'Image', 'Check', 'Back']
        buttons_position = [(1, 0), (2, 0), (3, 0), (4, 0)]
        buttons_command = [self.cam_reg_gui, self.img_reg_gui, self.check_reg_gui, self.start_gui]
        key_bindings = ['c', 'i', 'k', 'b']  # Key bindings for buttons
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command, key_bindings)

    def cam_reg_gui(self):
        root.title("Camera Capture")
        self.active_gui = 'cam_reg_gui'
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Camera Capture", font=self.fs.get_main_label_font()))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.control_flag = True
        try:
            cframe, self.latest_image = camera_frame(Frame(self.frame), self.cap, self.control_flag, row=1, column=0, rowspan=4, columnspan=4,camera_frame_size= self.fs.get_camera_frame_size())
            self.widgets.camera_frames.append(cframe)
        except Exception as e:
            self.widgets.texts.append(Text(self.frame, width=40, height=17))
            self.widgets.texts[-1].insert(END,f"\n\n\n\n\n\n\n\nError Acessing Camera : {e}\n\n\n\n\n\n\n\n")
            self.widgets.texts[-1].configure(font=self.fs.get_text_font())
            self.widgets.texts[-1].configure(state=DISABLED)
            self.widgets.texts[-1].grid(row=1, column=0, columnspan=4,rowspan=4)
        self.widgets.labels.append(Label(self.frame,text='Enter Details',font = self.fs.get_main_label_font(weight='normal')))
        self.widgets.labels[-1].grid(row = 1,column = 4, columnspan = 4)
        self.widgets.labels.append(Label(self.frame, text="Enter ID : ", font=self.fs.get_text_font()))
        self.widgets.labels[-1].grid(column=5, row=2)
        self.widgets.entries.append(Entry(self.frame, width=30))
        self.widgets.entries[-1].grid(column=6, row=2)
        self.widgets.entries[-1].configure(font=self.fs.get_text_font())
        self.widgets.labels.append(Label(self.frame, text="Enter Name : ", font=self.fs.get_text_font()))
        self.widgets.labels[-1].grid(column=5, row=3)
        self.widgets.entries.append(Entry(self.frame, width=30))
        self.widgets.entries[-1].grid(column=6, row=3)
        self.widgets.entries[-1].configure(font=self.fs.get_text_font())
        self.restore_frame_data()
        buttons_text = ['Register','Update','Capture','Recapture','Skip Face','Back','Main Menu']
        buttons_position = [(4, 5), (4, 6), (5, 1), (5, 2),(5,4), (5, 5), (5, 6)]
        buttons_command = [self.reg_gui_register, self.reg_gui_update, self.cam_reg_gui_capture , self.cam_reg_gui_recapture,self.skip_face ,self.register_gui, self.start_gui]
        key_bindings = ['g','u','a','p','s','b','m']
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command, key_bindings)

    def cam_reg_gui_capture(self, put=False):
        if self.latest_image[0] is None:
            self.clear_status_messages(row=6, column=0)  # Clear messages at row 6, column 0
            message = "No image captured. Please recapture."
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font=self.fs.get_text_font()))
            self.widgets.messages[-1].grid(column=0, row=6, columnspan=4)
            return
        self.faces,self.locations,self.encodings = get_cropped_faces_locations(self.latest_image[0])
        return self.put_rectangle(put)
    
    def put_rectangle(self, put=False):
        if self.faces is not None and len(self.faces) > 0 and not (len(self.faces) == 1 and self.faces[0] is None):
            image, self.matched = match_image(self.faces[-1], self.locations[-1], self.data, self.save_confidence, self.latest_image[0])
            self.faces.pop()
            self.locations.pop()
            if put:
                return self.matched
            self.clear_camera_frame()
            self.widgets.camera_frames.append(cam_reg_gui_capture(Frame(self.frame, width=40, height=17), image, row=1, column=0, rowspan=4, columnspan=4))
            if self.matched is not None:
                self.widgets.entries[0].delete(0, END)
                self.widgets.entries[0].insert(0, str(self.matched[1]))
                
                self.widgets.entries[1].delete(0, END)
                self.widgets.entries[1].insert(0, str(self.matched[0]))
            
    def skip_face(self):
        if len(self.encodings) > 0:
            self.encodings.pop()
            if len(self.faces) > 0:
                self.put_rectangle()
        
    def cam_reg_gui_recapture(self):
        self.clear_camera_frame()
        self.faces.clear()
        self.locations.clear()
        self.encodings.clear()
        self.control_flag = True
        try:
            cframe,self.latest_image = camera_frame(Frame(self.frame,width=40,height=17),self.cap, self.control_flag ,row=1, column=0, rowspan=4, columnspan=4,camera_frame_size= self.fs.get_camera_frame_size())
            self.widgets.camera_frames.append(cframe)
        except Exception as e:
            self.widgets.texts.append(Text(self.frame, width=40, height=17))
            self.widgets.texts[-1].insert(END,f"\n\n\n\n\n\n\n\nError Acessing Camera : {e}\n\n\n\n\n\n\n\n")
            self.widgets.texts[-1].configure(font=self.fs.get_text_font())
            self.widgets.texts[-1].configure(state=DISABLED)
            self.widgets.texts[-1].grid(row=1, column=0, columnspan=4,rowspan=4)
            self.control_flag = False

    def reg_gui_register(self, imag_reg = False):
        if self.widgets.entries[0].get() == "" or self.widgets.entries[1].get() == "":
            self.clear_status_messages(row=6, column=0)  # Clear messages at row 6, column 0
            message = "Please enter both ID and Name."
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font=self.fs.get_text_font()))
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
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font=self.fs.get_text_font()))
            self.widgets.messages[-1].grid(column=0, row=6, columnspan=4) 
            if not imag_reg:
                self.cam_reg_gui_recapture()

    def reg_gui_update(self, imag_reg = False):
        if self.widgets.entries[0].get() == "" or self.widgets.entries[1].get() == "":
            self.clear_status_messages(row=6, column=0)  # Clear messages at row 6, column 0
            message = "Please enter both ID and Name."
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font=self.fs.get_text_font()))
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
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font=self.fs.get_text_font()))
            self.widgets.messages[-1].grid(column=0, row=6, columnspan=4) 
            if not imag_reg:
                self.cam_reg_gui_recapture()

    def img_reg_gui(self):
        root.title("Image Capture")
        self.active_gui = 'img_reg_gui'
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Image Capture", font=self.fs.get_main_label_font()))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.widgets.texts.append(Text(self.frame, width=40, height=17))
        self.widgets.texts[-1].insert(END,"\n\n\n\n\n\n\n\n                 Image\n\n\n\n\n\n\n\n")
        self.widgets.texts[-1].configure(font=self.fs.get_text_font())
        self.widgets.texts[-1].configure(state=DISABLED)
        self.widgets.texts[-1].grid(row=1, column=0, columnspan=4,rowspan=4)
        self.widgets.labels.append(Label(self.frame,text='Enter Details',font = self.fs.get_main_label_font(weight='normal')))
        self.widgets.labels[-1].grid(row = 1,column = 4, columnspan = 4)
        self.widgets.labels.append(Label(self.frame, text="Enter ID : ", font=self.fs.get_text_font()))
        self.widgets.labels[-1].grid(column=5, row=2)
        self.widgets.entries.append(Entry(self.frame, width=30))
        self.widgets.entries[-1].grid(column=6, row=2)
        self.widgets.entries[-1].configure(font=self.fs.get_text_font())
        self.widgets.labels.append(Label(self.frame, text="Enter Name : ", font=self.fs.get_text_font()))
        self.widgets.labels[-1].grid(column=5, row=3)
        self.widgets.entries.append(Entry(self.frame, width=30))
        self.widgets.entries[-1].grid(column=6, row=3)
        self.widgets.entries[-1].configure(font=self.fs.get_text_font())
        self.restore_frame_data()
        self.widgets.buttons.create_button('sel_img', 'Select Image', (4, 0), self.sel_img,key_bind= 'i')
        self.widgets.buttons.hide('sel_img')
        self.widgets.buttons.grid('sel_img', (5,0), rowspan=1, columnspan=3)
        buttons_text = ['Register','Update','Skip Face','Back','Main Menu']
        buttons_position = [(4, 5), (4, 6), (5,4) ,(5, 5), (5, 6)]
        buttons_command = [lambda: self.reg_gui_register(True), lambda : self.reg_gui_update(True),self.skip_face ,self.register_gui, self.start_gui]
        key_bindings = ['g','u','s','b','m']
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command, key_bindings)

    def sel_img(self):
        image,frame = open_img_file(self.frame, width=self.fs.get_camera_frame_size()[0], height=self.fs.get_camera_frame_size()[1], row=1, column=0, rowspan=4, columnspan=4)
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
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font=self.fs.get_text_font()))
            self.widgets.messages[-1].grid(column=0, row=6, columnspan=4)

    def check_reg_gui(self):
        root.title("Check Registration")
        self.active_gui = 'check_reg_gui'
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Check Registration", font=self.fs.get_main_label_font()))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=4)
        self.widgets.labels.append(Label(self.frame, text="Enter ID : ", font=self.fs.get_text_font()))
        self.widgets.labels[-1].grid(column=1, row=1)
        self.widgets.entries.append(Entry(self.frame, width=30))
        self.widgets.entries[-1].grid(column=2, row=1)
        self.widgets.entries[-1].configure(font=self.fs.get_text_font())
        self.widgets.labels.append(Label(self.frame, text="Enter Name : ", font=self.fs.get_text_font()))
        self.widgets.labels[-1].grid(column=1, row=2)
        self.widgets.entries.append(Entry(self.frame, width=30))
        self.widgets.entries[-1].grid(column=2, row=2)
        self.widgets.entries[-1].configure(font=self.fs.get_text_font())
        self.widgets.messages.append(Message(self.frame, text="         ", width=200, font=self.fs.get_text_font()))
        self.widgets.messages[-1].grid(column=0, row=3, columnspan=4)
        self.restore_frame_data()
        buttons_text = ['Check','Back','Main Menu']
        buttons_position = [(4, 1), (4, 2), (4, 3)]
        buttons_command = [self.check_registration, self.register_gui, self.start_gui]
        key_bindings = ['c','b','m']
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command, key_bindings)

    def check_registration(self):
        id_value = self.widgets.entries[0].get()
        name_value = self.widgets.entries[1].get()
        if id_value == "" or name_value == "":
            self.clear_status_messages(row=3, column=0)
            message = "Please enter both ID and Name."
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font=self.fs.get_text_font()))
            self.widgets.messages[-1].grid(column=0, row=3, columnspan=4)
            return
        if check_registration(name_value, id_value):
            self.clear_status_messages(row=3, column=0)
            message = f"User {name_value} with ID {id_value} is registered."
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font=self.fs.get_text_font()))
            self.widgets.messages[-1].grid(column=0, row=3, columnspan=4)
        else:
            self.clear_status_messages(row=3, column=0)
            message = f"User {name_value} with ID {id_value} is not registered."
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font=self.fs.get_text_font()))
            self.widgets.messages[-1].grid(column=0, row=3, columnspan=4)

    def recognize_gui(self):
        root.title("Recognize")
        self.active_gui = 'recognize_gui'
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Recognize", font=self.fs.get_main_label_font()))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        buttons_text = ['Real-time Recognition', 'Keypress Recognition', 'Back']
        buttons_position = [(1, 0), (2, 0), (3, 0)]
        buttons_command = [self.real_time_rec_gui, self.keypress_rec_gui, self.start_gui]
        key_bindings = ['r','k','b']
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command, key_bindings)

    def real_time_rec_gui(self):
        root.title("Real-time Recognition")
        self.active_gui = 'real_time_rec_gui'
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Real-time Recognition", font=self.fs.get_main_label_font()))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.control_flag = True
        # try:
        #     cframe,self.latest_image = camera_frame(Frame(self.frame,width=40,height=17),self.cap, self.control_flag ,row=1, column=0, rowspan=4, columnspan=4,camera_frame_size= self.fs.get_camera_frame_size())
        #     self.widgets.camera_frames.append(cframe)
        # except Exception as e:
        #     self.widgets.texts.append(Text(self.frame, width=40, height=17))
        #     self.widgets.texts[-1].insert(END,f"\n\n\n\n\n\n\n\nError Acessing Camera : {e}\n\n\n\n\n\n\n\n")
        #     self.widgets.texts[-1].configure(font=self.fs.get_text_font())
        #     self.widgets.texts[-1].configure(state=DISABLED)
        #     self.widgets.texts[-1].grid(row=1, column=0, columnspan=4,rowspan=4)
        self.widgets.labels.append(Label(self.frame,text='Last Recognised Users',font = self.fs.get_main_label_font(weight='normal')))
        self.widgets.labels[-1].grid(row = 1,column = 4, columnspan = 2)
        self.widgets.texts.append(Text(self.frame, width = 30, height = 16))
        self.widgets.texts[-1].configure(font=self.fs.get_text_font())
        self.widgets.texts[-1].configure(state=DISABLED)
        self.widgets.texts[-1].grid(row = 2,column = 4,rowspan = 3, columnspan = 2)
        self.restore_frame_data()
        buttons_text = ['Start','Stop','Back', 'Main Menu']
        buttons_position = [(5,0),(5,1),(5, 2), (5, 4)]
        buttons_command = [self.real_time_rec_gui_start , self.real_time_rec_gui_stop, self.recognize_gui, self.start_gui]
        key_bindings = ['t','p','b','m']
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command, key_bindings)

    def real_time_rec_gui_start(self):
        self.clear_camera_frame()
        self.control_flag = True
        self.st = Manager().list()  # Use a Manager list for inter-process communication
        try:
            cframe,self.latest_image = camera_frame(Frame(self.frame,width=40,height=17),self.cap, self.control_flag ,row=1, column=0, rowspan=4, columnspan=4, st=[self.st], path_save=os.path.join(self.path,'captured_images'),camera_frame_size= self.fs.get_camera_frame_size())
            self.widgets.camera_frames.append(cframe)
        except Exception as e:
            self.widgets.texts.append(Text(self.frame, width=40, height=17))
            self.widgets.texts[-1].insert(END,f"\n\n\n\n\n\n\n\nError Acessing Camera : {e}\n\n\n\n\n\n\n\n")
            self.widgets.texts[-1].configure(font=self.fs.get_text_font())
            self.widgets.texts[-1].configure(state=DISABLED)
            self.widgets.texts[-1].grid(row=1, column=0, columnspan=4,rowspan=4)
            self.control_flag = False
            return
        self.qu = Queue()
        self.rec_process = Process(target= self.real_time_rec, args=(self.st,self.qu,self.data,self.confidence_match))
        self.rec_process.daemon = True
        self.rec_process.start()

        self.poll_queue()

    def poll_queue(self):
        try:
            while not self.qu.empty():
                matched = self.qu.get_nowait()
                if matched is not None:
                    if self.ex.write_to_excel(matched[0], matched[1], matched[2], self.tg):
                        self.widgets.texts[-1].configure(state=NORMAL)
                        self.widgets.texts[-1].insert(END, f"Name: {matched[0]} ID: {matched[1]}" + f" Confidence: {((1-matched[3])*100):.2f}% \n" if self.showConfidence else "\n")
                        self.widgets.texts[-1].configure(state=DISABLED)
                    
        except Exception as e:
            print(f"Error in poll_queue: {e}")
        
        if self.control_flag:
            self.root.after(100, lambda: self.poll_queue())
        
    def real_time_rec_gui_stop(self):
        self.control_flag = False
        if hasattr(self, 'rec_process') and self.rec_process.is_alive():
            self.rec_process.terminate()
            self.rec_process.join()
        self.st[:] = []
        self.qu.close()
        shutil.rmtree(os.path.join(self.path, 'captured_images'), ignore_errors=True)

        self.clear_camera_frame()

    @staticmethod
    def real_time_rec(st, qu, load_data, confidence_match):
        while len(st) > 0:
            img_path = st.pop()
            image = read_image(img_path, convert_to_bgr=True)
            if image is not None:
                faces, locations, encodings = get_cropped_faces_locations(image)
                while len(encodings) > 0:
                    img, matched = match_image(faces[-1], locations[-1], load_data, confidence_match, image)
                    faces.pop()
                    locations.pop()
                    encodings.pop()
                    if matched is not None and matched[3] is not None and matched[3] < confidence_match:
                        try:
                            qu.put(matched)
                        except Exception:
                            return # Adjust sleep time as needed
                    
    def keypress_rec_gui(self):
        root.title("Keypress Recognition")
        self.active_gui = 'keypress_rec_gui'
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Keypress Recognition", font=self.fs.get_main_label_font()))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.control_flag = True
        try:
            cframe,self.latest_image = camera_frame(Frame(self.frame,width=40,height=17),self.cap, self.control_flag ,row=1, column=0, rowspan=4, columnspan=4,camera_frame_size= self.fs.get_camera_frame_size())
            self.widgets.camera_frames.append(cframe)
        except Exception as e:
            self.widgets.texts.append(Text(self.frame, width=40, height=17))
            self.widgets.texts[-1].insert(END,f"\n\n\n\n\n\n\n\nError Acessing Camera : {e}\n\n\n\n\n\n\n\n")
            self.widgets.texts[-1].configure(font=self.fs.get_text_font())
            self.widgets.texts[-1].configure(state=DISABLED)
            self.widgets.texts[-1].grid(row=1, column=0, columnspan=4,rowspan=4)
        self.widgets.labels.append(Label(self.frame,text='Last Recognised Users',font = self.fs.get_main_label_font(weight='normal')))
        self.widgets.labels[-1].grid(row = 1,column = 4, columnspan = 2)
        self.widgets.buttons.create_button('reco', 'Recognize', (1 ,1), self.keypress_rec_gui_reco,key_bind='r')
        self.widgets.buttons.hide('reco')
        self.widgets.buttons.grid('reco', (5, 0), rowspan=1, columnspan=2)
        self.widgets.texts.append(Text(self.frame, width = 30, height = 16))
        self.widgets.texts[-1].configure(font=self.fs.get_text_font())
        self.widgets.texts[-1].configure(state=DISABLED)
        self.widgets.texts[-1].grid(row = 2,column = 4,rowspan = 3, columnspan = 2)
        self.restore_frame_data()
        buttons_text = ['back', 'main menu']
        buttons_position = [(5, 2), (5, 4)]
        buttons_command = [self.recognize_gui, self.start_gui]
        key_bindings = ['b','m']
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command, key_bindings)

    def keypress_rec_gui_reco(self):
        matched = self.cam_reg_gui_capture(True)
        while len(self.encodings) > 0:
            self.encodings.pop()
            if matched is not None:
                if self.ex.write_to_excel(matched[0],matched[1],matched[2],self.tg):
                    self.widgets.texts[-1].configure(state = NORMAL)
                    self.widgets.texts[-1].insert(END,f"Name: {matched[0]} ID: {matched[1]}"+f" Confidence: {((1-matched[3])*100):.2f}% \n" if self.showConfidence else "\n")
                    self.widgets.texts[-1].configure(state = DISABLED)
            if len(self.encodings) > 0:
                matched = self.put_rectangle(True)
            else:
                break
                
    def op_data(self):
        root.title("Operate Data")
        self.active_gui = 'op_data'
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Operate Data", font=self.fs.get_main_label_font()))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.widgets.labels.append(Label(self.frame, text="Enter ID : ", font=self.fs.get_text_font()))
        self.widgets.labels[-1].grid(column=0, row=1)
        self.widgets.entries.append(Entry(self.frame, width=7))
        self.widgets.entries[-1].grid(column=1, row=1)
        self.widgets.entries[-1].configure(font=self.fs.get_text_font())
        self.restore_frame_data()
        buttons_text = ['Read Data', 'Write Data', 'Back']
        buttons_position = [ (2, 0), (3, 0),(4, 0)]
        buttons_command = [ self.read_data_gui, self.write_data_gui, self.start_gui]
        key_bindings = ['r','w','b']
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command, key_bindings)

    def read_data_gui(self):
        root.title("Read Data")
        self.active_gui = 'read_data_gui'
        user_id = self.widgets.entries[-1].get()
        if user_id == "":
            self.clear_status_messages(row=5, column=0)
            message = "Please enter a valid ID."
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font=self.fs.get_text_font()))
            self.widgets.messages[-1].grid(column=0, row=5, columnspan=2)
            return
        c_row = self.ex.get_row_number(user_id)
        if c_row is None:
            self.clear_status_messages(row=5, column=0)
            message = f"No data found for ID {user_id}."
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font=self.fs.get_text_font()))
            self.widgets.messages[-1].grid(column=0, row=5, columnspan=2)
            return
        self.clear_frame()
        user_name = self.ex.read_excel(c_row, 2)
        self.widgets.labels.append(Label(self.frame, text="Read Data", font=self.fs.get_main_label_font()))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.widgets.labels.append(Label(self.frame, text=f"Name : {user_name} (ID :{user_id})", font=self.fs.get_main_label_font(weight='normal')))
        self.widgets.labels[-1].grid(column=0, row=1, columnspan=2)
        entries = self.ex.get_all_entries(c_row)
        self.widgets.texts.append(Text(self.frame, width = 40, height = 15))
        for entry in entries:
            self.widgets.texts[-1].insert(END, f"{entry}\n")
        self.widgets.texts[-1].configure(font = self.fs.get_text_font())
        self.widgets.texts[-1].configure(state = DISABLED)
        self.widgets.texts[-1].grid(row=2, column=0, columnspan=3, rowspan=4)
        self.widgets.labels.append(Label(self.frame, text= f"Total Entries : {len(entries)}", font=self.fs.get_text_font()))
        self.widgets.labels[-1].grid(row=6, column=0, columnspan=3)
        label_date_in, entry_date_in = dateWidget(self.frame, 7, 0, "Initial Date (DD/MM/YYYY):")
        label_time_in, entry_time_in = timeWidget(self.frame, 7, 2, "Time (HH:MM:SS):")
        label_date_in.configure(font=self.fs.get_text_font())
        label_time_in.configure(font=self.fs.get_text_font())
        entry_date_in.configure(font=self.fs.get_text_font())
        entry_time_in.configure(font=self.fs.get_text_font())
        self.widgets.labels.append(label_date_in)
        self.widgets.entries.append(entry_date_in)
        self.widgets.labels.append(label_time_in)
        self.widgets.entries.append(entry_time_in)
        label_date_out, entry_date_out = dateWidget(self.frame, 8, 0, "Final Date (DD/MM/YYYY):")
        label_time_out, entry_time_out = timeWidget(self.frame, 8, 2, "Time (HH:MM:SS):")
        label_date_out.configure(font=self.fs.get_text_font())
        label_time_out.configure(font=self.fs.get_text_font())
        entry_date_out.configure(font=self.fs.get_text_font())
        entry_time_out.configure(font=self.fs.get_text_font())
        self.widgets.labels.append(label_date_out)
        self.widgets.entries.append(entry_date_out)
        self.widgets.labels.append(label_time_out)
        self.widgets.entries.append(entry_time_out)
        self.restore_frame_data()
        buttons_text = ['Read','Back','Main Menu']
        buttons_position = [(9, 0), (9, 1), (9, 2)]
        buttons_command = [lambda: self.read_data_gui_read(c_row), self.op_data, self.start_gui]
        key_bindings = ['r','b','m']
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command, key_bindings)

    def read_data_gui_read(self,c_row):
        date_in = self.widgets.entries[-4].get()
        time_in = self.widgets.entries[-3].get()
        date_out = self.widgets.entries[-2].get()
        time_out = self.widgets.entries[-1].get()

        date_in, time_in, date_out, time_out = get_all_date_time(self.ex, c_row, date_in, time_in, date_out, time_out)

        if date_in == "" and time_in == "" and date_out == "" and time_out == "":
            self.clear_status_messages(row=10, column=0)
            message = "Please enter valid dates and times."
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font=self.fs.get_text_font()))
            self.widgets.messages[-1].grid(column=0, row=10, columnspan=2)
            return
        
        in_time = f"{date_in} - {time_in}"
        fi_time = f"{date_out} - {time_out}"
        entries = self.ex.get_entries_by_time_range(c_row, in_time, fi_time)
        self.clear_status_messages(row=10, column=0)
        self.widgets.texts[-1].configure(state=NORMAL)
        self.widgets.texts[-1].delete(1.0, END)
        for entry in entries:
            self.widgets.texts[-1].insert(END, f"{entry}\n")
        self.widgets.texts[-1].configure(state=DISABLED)
        
    def write_data_gui(self, c_row=None):
        root.title("Write Data")
        self.active_gui = 'write_data_gui'
        if c_row is None:
            user_id = self.widgets.entries[-1].get()
            if user_id == "":
                self.clear_status_messages(row=5, column=0)
                message = "Please enter a valid ID."
                self.widgets.messages.append(Message(self.frame, text=message, width=200, font=self.fs.get_text_font()))
                self.widgets.messages[-1].grid(column=0, row=5, columnspan=2)
                return
            c_row = self.ex.get_row_number(user_id)
            if c_row is None:
                new_root = Tk()
                fram = ttk.Frame(new_root, padding=10)
                fram.grid(row=0, column=0, sticky="NS")
                label = Label(fram, text="Enter Name ", font=self.fs.get_main_label_font(weight='normal'))
                label.grid(column=0, row=0)
                entry = Entry(fram, width=30)
                entry.grid(column=1, row=0)
                create_new_user_entry(label.get(), entry.get(), self.ex)
                label.grid_remove()
                entry.grid_remove()
                fram.grid_remove()
                new_root.destroy()
                c_row = self.ex.max_row
            user_name = self.ex.read_excel(c_row, 2)
        else:
            user_id = self.ex.read_excel(c_row, 1)
            user_name = self.ex.read_excel(c_row, 2)
        
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Write Data", font=self.fs.get_main_label_font()))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.widgets.labels.append(Label(self.frame, text=f"Name : {user_name} (ID :{user_id})", font=self.fs.get_main_label_font(weight='normal')))
        self.widgets.labels[-1].grid(column=0, row=1, columnspan=2)
        self.widgets.labels.append(Label(self.frame, text="Write Data", font=self.fs.get_main_label_font()))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.restore_frame_data()
        buttons_text = ['Create Data','Delete Data','Back','Main Menu']
        buttons_position = [(2, 0), (3,0), (4, 0), (5, 0)]
        buttons_command = [lambda : self.create_entry_gui(c_row), lambda: self.delete_entry_gui(c_row), self.op_data, self.start_gui]
        key_bindings = ['c','d','b','m']
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command, key_bindings)

    def create_entry_gui(self, c_row):
        root.title("Create Entry")
        self.active_gui = 'create_entry_gui'
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Create Entry", font=self.fs.get_main_label_font()))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.widgets.labels.append(Label(self.frame, text=f"Name : {self.ex.read_excel(c_row,2)} (ID :{self.ex.read_excel(c_row,1)})", font=self.fs.get_main_label_font(weight='normal')))
        self.widgets.labels[-1].grid(column=0, row=1, columnspan=2)
        date_label, date_entry = dateWidget(self.frame, 2, 0, "Enter Date (DD/MM/YYYY):")
        time_label, time_entry = timeWidget(self.frame, 2, 2, "Enter Time (HH:MM:SS):")
        date_entry.configure(font=self.fs.get_text_font())
        time_entry.configure(font=self.fs.get_text_font())
        date_label.configure(font=self.fs.get_text_font())
        time_label.configure(font=self.fs.get_text_font())
        self.widgets.labels.append(date_label)
        self.widgets.entries.append(date_entry)
        self.widgets.labels.append(time_label)
        self.widgets.entries.append(time_entry)
        self.restore_frame_data()
        buttons_text = ['Now','Create','Back','Main Menu']
        buttons_position = [(3, 0),(3,1), (3, 2), (3, 3)]
        buttons_command = [self.create_entry_gui_now, lambda: self.create_entry_gui_create(c_row),lambda : self.write_data_gui(c_row), self.start_gui]
        key_bindings = ['n','c','b','m']
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command, key_bindings)

    def create_entry_gui_now(self):
        from datetime import datetime
        now = datetime.now()
        date_str = now.strftime("%d/%m/%Y")
        time_str = now.strftime("%H:%M:%S")
        self.widgets.entries[-2].delete(0, END)
        self.widgets.entries[-2].insert(0, date_str)
        self.widgets.entries[-1].delete(0, END)
        self.widgets.entries[-1].insert(0, time_str)

    def create_entry_gui_create(self, c_row):
        date_in = self.widgets.entries[-2].get()
        time_in = self.widgets.entries[-1].get()

        if date_in == "" or time_in == "":
            self.clear_status_messages(row=4, column=0)
            message = "Please enter both date and time."
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font=self.fs.get_text_font()))
            self.widgets.messages[-1].grid(column=0, row=4, columnspan=2)
            return
        if not validate_date(date_in) or not validate_time(time_in):
            self.clear_status_messages(row=4, column=0)
            message = "Please enter valid date and time formats."
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font=self.fs.get_text_font()))
            self.widgets.messages[-1].grid(column=0, row=4, columnspan=2)
            return

        entry_time = f"{date_in} - {time_in}"
        self.ex.write_excel(c_row, self.ex.ws.max_column+1,entry_time)
        self.clear_status_messages(row=4, column=0)
        message = "Entry created successfully."
        self.widgets.messages.append(Message(self.frame, text=message, width=200, font=self.fs.get_text_font()))
        self.widgets.messages[-1].grid(column=0, row=4, columnspan=2)

    def delete_entry_gui(self, c_row):
        root.title("Delete Entry")
        self.active_gui = 'delete_entry_gui'
        self.clear_frame()
        user_name = self.ex.read_excel(c_row, 2)
        user_id = self.ex.read_excel(c_row, 1)
        self.widgets.labels.append(Label(self.frame, text="Delete Entry", font=self.fs.get_main_label_font()))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.widgets.labels.append(Label(self.frame, text=f"Name : {user_name} (ID :{user_id})", font=self.fs.get_main_label_font(weight='normal')))
        self.widgets.labels[-1].grid(column=0, row=1, columnspan=2)
        self.widgets.frames.append(Frame(self.frame))
        self.widgets.frames[-1].grid(column=0, row=4, columnspan=2, sticky='ew')
        self.widgets.scrollbars.append(Scrollbar(self.widgets.frames[-1], orient=VERTICAL))
        self.widgets.scrollbars[-1].pack(side=RIGHT, fill=Y)
        self.widgets.list_boxes.append(Listbox(self.widgets.frames[-1], width=50, height=10 , font=self.fs.get_text_font(), selectmode=MULTIPLE, yscrollcommand=self.widgets.scrollbars[-1].set)) 
        entries = self.ex.get_all_entries(c_row)
        for entry in entries:
            self.widgets.list_boxes[-1].insert(END, entry)
        
        self.widgets.list_boxes[-1].pack(side=LEFT, fill=BOTH, expand=True)
        self.restore_frame_data()
        buttons_text = ['Delete','Back','Main Menu']
        buttons_position = [(5, 0), (5,1), (5, 2)]
        buttons_command = [ lambda: self.delete_entry_gui_delete(c_row),lambda: self.write_data_gui(c_row), self.start_gui]
        key_bindings = ['d','b','m']
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command, key_bindings)

    def delete_entry_gui_delete(self, c_row):
        selected_indices = self.widgets.list_boxes[-1].curselection()
        if not selected_indices:
            self.clear_status_messages(row=6, column=0)
            message = "Please select at least one entry to delete."
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font=self.fs.get_text_font()))
            self.widgets.messages[-1].grid(column=0, row=6, columnspan=2)
            return
        delete_user_entries(self.ex, c_row, selected_indices, self.widgets.list_boxes[-1])
        for index in sorted(selected_indices, reverse=True):
            self.widgets.list_boxes[-1].delete(index)
        
    def config_gui(self):
        root.title("Settings")
        self.active_gui = 'config_gui'
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Settings", font=self.fs.get_main_label_font()))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        buttons_text = ['Confidence','Load Data','Time Gap','Back']
        buttons_position = [(1, 0), (2, 0), (3, 0),(4,0)]
        buttons_command = [self.config_conf_gui, self.config_load_gui,self.time_gap_config ,self.start_gui]
        key_bindings = ['c','l','t','b']
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command, key_bindings)

    def time_gap_config(self):
        root.title("Time Gap Configuration")
        self.active_gui = 'time_gap_config'
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Time Gap between two recognitions(in seconds) ", font=self.fs.get_main_label_font()))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.widgets.entries.append(Entry(self.frame, width = 7))
        self.widgets.entries[-1].grid(column = 2, row = 0)
        self.widgets.entries[-1].configure(font=self.fs.get_text_font())
        self.widgets.entries[-1].insert(END,self.tg)
        buttons_text = ['Save', 'Back', 'Main Menu']
        buttons_position = [(2,0),(2,1),(2,2)]
        buttons_command = [self.tg_save , self.config_gui, self.start_gui]
        key_bindings = ['s','b','m']
        self.widgets.buttons.create_buttons(buttons_text,buttons_position,buttons_command, key_bindings)

    def tg_save(self):
        self.tg = self.widgets.entries[-1].get()
        try:
            self.tg = int(self.tg)
            if self.tg < 0:
                raise ValueError("Time gap must be positive.")
            self.config['time_gap'] = self.tg
            self.save_config(self.config)
            self.clear_status_messages(row=6, column=0)
            message = "Time gap updated successfully."
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font=self.fs.get_text_font()))
            self.widgets.messages[-1].grid(column=0, row=6, columnspan=2)
        except ValueError as e:
            self.clear_status_messages(row=6, column=0)
            message = f"Invalid input: {e}"
            self.widgets.messages.append(Message(self.frame, text=message, width=200, font=self.fs.get_text_font()))
            self.widgets.messages[-1].grid(column=0, row=6, columnspan=2)

    def config_conf_gui(self):
        root.title("Confidence Settings")
        self.active_gui = 'config_conf_gui'
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Confidence Settings", font=self.fs.get_main_label_font()))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.widgets.check_boxes.append(Checkbutton(self.frame, text="Show Confidence", font=self.fs.get_main_label_font(weight='normal')))
        if self.showConfidence:
            self.widgets.check_boxes[-1].select()
        self.widgets.check_boxes[-1].grid(column=0, row=1, columnspan=2)
        self.widgets.labels.append(Label(self.frame, text="Save Confidence Threshold", font=self.fs.get_main_label_font(weight='normal')))
        self.widgets.labels[-1].grid(column=0, row=2, columnspan=1)
        self.widgets.scales.append(Scale(self.frame, orient='horizontal'))
        self.widgets.scales[-1].set((1- self.save_confidence) * 100)
        self.widgets.scales[-1].grid(column=1, row=2, columnspan=1, sticky='ew')
        self.widgets.labels.append(Label(self.frame, text="Match Confidence Threshold", font=self.fs.get_main_label_font(weight='normal')))
        self.widgets.labels[-1].grid(column=0, row=3, columnspan=1)
        self.widgets.scales.append(Scale(self.frame, orient='horizontal'))
        self.widgets.scales[-1].set((1 - self.confidence_match) * 100)
        self.widgets.scales[-1].grid(column=1, row=3, columnspan=1, sticky='ew')
        buttons_text = ['Save','Back','Main Menu']
        buttons_position = [(4, 0), (4, 1), (4, 2)]
        buttons_command = [self.config_conf_gui_save, self.config_gui, self.start_gui]
        key_bindings = ['s','b','m']
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command, key_bindings)

    def config_conf_gui_save(self):
        # Use IntVar for checkboxes, so get() returns 1/0
        show_conf = self.widgets.check_boxes[-1].var.get() if hasattr(self.widgets.check_boxes[-1], 'var') else self.widgets.check_boxes[-1].instate(['selected'])
        self.showConfidence = bool(show_conf)
        self.save_confidence = 1 - (self.widgets.scales[-2].get() / 100)
        self.confidence_match = 1 - (self.widgets.scales[-1].get() / 100)
        self.config['show_confidence'] = self.showConfidence
        self.config['confidence_save'] = self.save_confidence
        self.config['confidence_match'] = self.confidence_match
        self.save_config(self.config)
        self.clear_status_messages(row=5, column=0)
        message = "Settings saved successfully."
        self.widgets.messages.append(Message(self.frame, text=message, width=200, font=self.fs.get_text_font()))
        self.widgets.messages[-1].grid(column=0, row=5, columnspan=2)

    def config_load_gui(self):
        root.title("Load Data Settings")
        self.active_gui = 'config_load_gui'
        self.clear_status_messages(row=5, column=0, clear_all=True)
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Load Data Settings", font=self.fs.get_main_label_font()))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        load = [self.ex]
        # Add key binding for the "Load Data" button (e.g., 'l')
        self.widgets.buttons.create_button('load', 'Load Data', (1, 1), lambda: self.config_load_gui_load(load), key_bind='l')
        self.widgets.buttons.hide('load')
        self.widgets.buttons.grid('load', (1, 0), rowspan=1, columnspan=3)
        buttons_text = ['Save','Back','Main Menu']
        buttons_position = [(4, 0), (4, 1), (4, 2)]
        buttons_command = [lambda: self.config_load_gui_save(load), self.config_gui, self.start_gui]
        key_bindings = ['s','b','m']
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command, key_bindings)

    def config_load_gui_load(self,load):
        ex_file = open_xlsx_file()
        if ex_file is not None:
            load[0] = ex_file

    def config_load_gui_save(self,load):
        self.ex = load[0]
        self.widgets.messages.append(Message(self.frame, text="Data loaded successfully.", width=200, font=self.fs.get_text_font()))
        self.widgets.messages[-1].grid(column=0, row=5, columnspan=2)

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


if __name__ == '__main__':

    root = Tk()
    root.geometry("1280x720")

    gui = GUI(root)
    gui.start_gui()
    root.mainloop()
