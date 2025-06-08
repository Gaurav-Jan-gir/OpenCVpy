from tkinter import *
from tkinter import ttk


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
        self.buttons = mButtons(self.frame)

    def clear_widgets(self):
        for widget in self.labels+self.entries+self.check_boxes+self.scrollbars+self.scales+self.messages+self.texts:
            widget.grid_remove()
        self.labels.clear()
        self.entries.clear()
        self.texts.clear()
        self.check_boxes.clear()
        self.scrollbars.clear()
        self.scales.clear()
        self.buttons.hide_all()
        self.messages.clear()

class GUI:
    def __init__(self, root):
        self.root = root
        self.frame = ttk.Frame(root, padding=10)
        self.frame.grid(row=0, column=0, sticky="NS") 
        
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        for i in range(8):
            self.frame.rowconfigure(i, weight=1)
        self.frame.columnconfigure(0, weight=1) 
        self.widgets = Widgets(self.frame)

    def clear_frame(self):
        self.widgets.clear_widgets()

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
        self.widgets.texts.append(Text(self.frame, width=40, height=17))
        self.widgets.texts[-1].insert(END,"\n\n\n\n\n\n\n\n                 Camera\n\n\n\n\n\n\n\n")
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
        buttons_command = [lambda: print("Register Button Pressed"), lambda: print("Update Button Pressed"), lambda: print("Capture Button Pressed"), lambda: print("Recapture Button Pressed"), self.register_gui, self.start_gui]
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command)

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
        self.widgets.buttons.create_button('sel_img', 'Select Image', (4, 0), lambda: print("Select Image Button Pressed"))
        self.widgets.buttons.hide('sel_img')
        self.widgets.buttons.grid('sel_img', (5,1), rowspan=1, columnspan=3)
        buttons_text = ['Register','Update','Back','Main Menu']
        buttons_position = [(4, 5), (4, 6),  (5, 5), (5, 6)]
        buttons_command = [lambda: print("Register Button Pressed"), lambda: print("Update Button Pressed"), self.register_gui, self.start_gui]
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command)
    
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
        self.widgets.messages.append(Message(self.frame, text="Registration Status", width=200, font='consolas 12'))
        self.widgets.messages[-1].grid(column=0, row=3, columnspan=4)
        buttons_text = ['Check','Back','Main Menu']
        buttons_position = [(4, 1), (4, 2), (4, 3)]
        buttons_command = [lambda: print("Check Button Pressed"), self.register_gui, self.start_gui]
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command)

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
        self.widgets.buttons.create_button('date', 'Select Date', (1, 0), lambda: print("Select Date Button Pressed"))
        self.widgets.buttons.hide('date')
        self.widgets.buttons.grid('date', (7, 0), rowspan=1, columnspan=3)
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
        self.widgets.buttons.create_button('time_range_in', 'Initial Time', (1, 0), lambda: print("Initial Time Button Pressed"))
        self.widgets.buttons.hide('time_range_in')
        self.widgets.buttons.grid('time_range_in', (7, 0), rowspan=1, columnspan=3)
        self.widgets.buttons.create_button('time_range_out', 'Final Time', (1, 0), lambda: print("Final Time Button Pressed"))
        self.widgets.buttons.hide('time_range_out')
        self.widgets.buttons.grid('time_range_out', (8, 0), rowspan=1, columnspan=3)
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
        buttons_text = ['Date-Time','Date-Time Fill','Now','Create','Back','Main Menu']
        buttons_position = [(2, 0), (2, 1), (2, 2),(3,0), (3, 1), (3, 2)]
        buttons_command = [lambda: print("Date-Time Button Pressed"), lambda: print("Date-Time Fill Button Pressed"), lambda: print("Now Button Pressed"), lambda: print("Create Entry Button Pressed"), self.write_data_gui, self.start_gui]
        self.widgets.buttons.create_buttons(buttons_text, buttons_position, buttons_command)

    def delete_entry_gui(self):
        root.title("Delete Entry")
        self.clear_frame()
        self.widgets.labels.append(Label(self.frame, text="Delete Entry", font='consolas 24 bold'))
        self.widgets.labels[-1].grid(column=0, row=0, columnspan=2)
        self.widgets.labels.append(Label(self.frame, text="Name : User1 ID :1", font='consolas 16'))
        self.widgets.labels[-1].grid(column=0, row=1, columnspan=2)
        buttons_text = ['Date-Time1','Date-Time2','Scrollable','Delete','Back','Main Menu']
        buttons_position = [(2, 0), (3,0), (4, 0), (5, 0), (5,1), (5, 2)]
        buttons_command = [lambda: print("Date-Time1 Button Pressed"), lambda: print("Date-Time2 Button Pressed"), lambda: print("Scrollable Button Pressed"), lambda: print("Delete Entry Button Pressed"), self.write_data_gui, self.start_gui]
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

root = Tk()
root.geometry("800x600")

gui = GUI(root)
gui.start_gui()


root.mainloop()
