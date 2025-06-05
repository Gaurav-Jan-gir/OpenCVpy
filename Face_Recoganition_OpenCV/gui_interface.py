from tkinter import *
from tkinter import ttk
import os

def_geometry = "640x480"
def_resizable = (True, True)
def_bg_color = 'lightblue'
def_state = 'normal' 
def_icon_path = "D:\\Python\\OpenCV\\OpenCVpy\\Face_Recoganition_OpenCV\\icon.ico"

class Buttons:
    def __init__(self, master):
        self.master = master
        self.buttons = {}

    def add_button(self, button_name, button_text, command, row=0, column=0, sticky=(N, W, E, S)):
        button = ttk.Button(self.master, text=button_text, command=command,style='Big.TButton')
        button.grid(row=row, column=column, sticky=sticky, pady=15, padx=40, ipadx=30, ipady=15)
        self.buttons[button_name] = button

    def get_button(self, button_name):
        return self.buttons.get(button_name, None)
    
    def hide_button(self, button_name):
        button = self.get_button(button_name)
        if button:
            button.grid_remove()
    
    def remove_button(self, button_name):
        button = self.get_button(button_name)
        if button:
            button.grid_forget()
            del self.buttons[button_name]
        
    def update_button(self, button_name, new_text, new_command=None):
        button = self.get_button(button_name)
        if button:
            button.config(text=new_text)
            if new_command:
                button.config(command=new_command)

def set_properties(frame, title, geometry=def_geometry, resizable=def_resizable, 
                  icon_path=def_icon_path, bg_color=def_bg_color, state=def_state):
    """Set window properties with error handling"""
    frame.title(title)
    frame.geometry(geometry)
    frame.resizable(*resizable)
    
    # Safe icon loading
    try:
        if os.path.exists(icon_path):
            frame.iconbitmap(icon_path)
    except Exception as e:
        print(f"Could not load icon: {e}")
    
    frame.configure(bg=bg_color)
    frame.state(state)

def clear_frame(frame):
    """Remove all widgets from the frame."""
    for widget in frame.winfo_children():
        widget.destroy()

def start_gui(root, buttons):
    """Initialize main GUI"""
    clear_frame(buttons.master)  # Clear existing widgets
    
    # Add title label
    title_label = ttk.Label(buttons.master, text="🎯 Face Recognition System", 
                           font=("Arial", 16, 'bold'))
    title_label.grid(row=0, column=0, pady=20, sticky=(N))
    
    buttons.add_button("btn0", "👤 User Registration", 
                      lambda: user_reg_gui(root, buttons), 
                      row=1, column=0, sticky=(N))
    
    buttons.add_button("btn1", "🔍 Face Recognition", 
                      lambda: face_recognition_gui(root, buttons), 
                      row=2, column=0, sticky=(N))
    
    buttons.add_button("btn2", "⚙️ Configuration & Management", 
                      lambda: config_gui(root, buttons), 
                      row=3, column=0, sticky=(N))
    
    buttons.add_button("btn3", "❌ Quit", 
                      root.destroy, 
                      row=4, column=0, sticky=(N))

def user_reg_gui(root, buttons):
    """User registration menu"""
    clear_frame(buttons.master)  # Clear existing widgets
    
    # Add new title
    title_label = ttk.Label(buttons.master, text="👤 User Registration", 
                           font=("Arial", 16, 'bold'))
    title_label.grid(row=0, column=0, pady=20, sticky=(N))
    
    buttons.add_button("btn0", "📷 Register User Via Camera", 
                      lambda: print("Register User Via Camera clicked!"), 
                      row=1, column=0, sticky=(N))
    buttons.add_button("btn1", "📁 Register User Via Image", 
                      lambda: print("Register User Via Image clicked!"), 
                      row=2, column=0, sticky=(N))
    buttons.add_button("btn2", "🔍 Check Registered Users", 
                      lambda: print("Check Registered Users clicked!"), 
                      row=3, column=0, sticky=(N))
    buttons.add_button("btn3", "🔙 Back to Main Menu", 
                      lambda: start_gui(root, buttons), 
                      row=4, column=0, sticky=(N))

def face_recognition_gui(root, buttons):
    """Face recognition menu"""
    clear_frame(buttons.master)  # Clear existing widgets
    
    # Add new title
    title_label = ttk.Label(buttons.master, text="🔍 Face Recognition", 
                           font=("Arial", 16, 'bold'))
    title_label.grid(row=0, column=0, pady=20, sticky=(N))
    
    buttons.add_button("btn0", "🎬 Real-time Recognition", 
                      lambda: print("Real-time Recognition clicked!"), 
                      row=1, column=0, sticky=(N))
    buttons.add_button("btn1", "⌨️ Keypress Recognition", 
                      lambda: print("Keypress Recognition clicked!"), 
                      row=2, column=0, sticky=(N))
    buttons.add_button("btn2", "🔙 Back to Main Menu", 
                      lambda: start_gui(root, buttons), 
                      row=3, column=0, sticky=(N))

def config_gui(root, buttons):
    """Configuration menu"""
    clear_frame(buttons.master)  # Clear existing widgets
    
    # Add new title
    title_label = ttk.Label(buttons.master, text="⚙️ Configuration & Management", 
                           font=("Arial", 16, 'bold'))
    title_label.grid(row=0, column=0, pady=20, sticky=(N))
    
    buttons.add_button("btn0", "🎯 Configure Confidence", 
                      lambda: print("Configure Confidence clicked!"), 
                      row=1, column=0, sticky=(N))
    buttons.add_button("btn1", "📊 Excel Operations", 
                      lambda: print("Excel Operations clicked!"), 
                      row=2, column=0, sticky=(N))
    buttons.add_button("btn2", "📂 Load Custom Excel", 
                      lambda: print("Load Custom Excel clicked!"), 
                      row=3, column=0, sticky=(N))
    buttons.add_button("btn3", "🔙 Back to Main Menu", 
                      lambda: start_gui(root, buttons), 
                      row=4, column=0, sticky=(N))

# Main application setup
if __name__ == "__main__":
    root = Tk()
    
    # Configure root window grid
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    style = ttk.Style(root)
    style.configure(
        'Big.TButton',
        font=('Arial', 20, 'bold'),   # Large font
        padding=20                    # Extra padding inside button
    )
    
    # Create main frame
    frm = ttk.Frame(root, padding=20)
    frm.grid(row=0, column=0, sticky=(N, W, E, S))
    frm.columnconfigure(0, weight=1)
    
    # Create button manager
    buttons = Buttons(frm)
    
    # Start the GUI
    start_gui(root, buttons)
    
    # Start the main loop
    root.mainloop()