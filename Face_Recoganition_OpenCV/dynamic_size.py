from tkinter import *

class DynamicSize:
    def __init__(self, root):
        self.root = root
        self.width = self.root.winfo_width()
        self.height = self.root.winfo_height()
        self.base_width = 1280
        self.base_height = 720
        self.base_dpi = 96
        self.dpi = self.root.winfo_fpixels('1i') 

    def on_resize(self, event):
        new_width = self.root.winfo_width()
        new_height = self.root.winfo_height()
        new_dpi = self.root.winfo_fpixels('1i')
        if new_width != self.width or new_height != self.height:
            self.width = new_width
            self.height = new_height
            self.dpi = new_dpi

    def get_scale(self):
        scale = self.width / self.base_width
        scale *= self.height / self.base_height
        scale *= self.dpi / self.base_dpi
        return scale**0.5

    def get_button_text_size(self):
        return int(16 * self.get_scale())
    
    def get_main_label_size(self):
        return int(24 * self.get_scale())
    
    def get_text_size(self):
        return int(12 * self.get_scale())
    
    def get_camera_frame_size(self):
        return (int(640 * self.get_scale()), int(480 * self.get_scale()))
    
    def get_button_font(self,weight="normal"):
        return ('Courier', self.get_button_text_size(), weight)
    
    def get_main_label_font(self,weight="bold"):
        return ('Courier', self.get_main_label_size(), weight)
    
    def get_text_font(self,weight="normal"):
        return ('Courier', self.get_text_size(), weight)
    
    