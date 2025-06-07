import camera_embed as ce
from Interface_excel import interFace 
import os

class GUIFunctions:
    def __init__(self, master, Buttons, excel_path=None,config_path=None):
        self.master = master
        self.buttons = Buttons
        self.ie = interFace(excel_path, config_path)
        self.path = self.ie.get_safe_data_path()
        self.setup_buttons()

    def setup_buttons(self):
        self.buttons.add_button('register', 'Register via Camera', self.register_via_camera, row=0, column=0)

    def register_via_camera(self,frame):
        res = ce.show_camera_embed(frame, 30, self.path)
        if res:
            self.ie.registerViaImage(os.path.join(self.path, 'latest_frame.jpg'))
        else:
            print("Image capture cancelled or failed.")

    def capture_on_keypress(self, frame, tg ,fps=30):
        res = ce.cont_camera_capture(frame, fps, self.path)
        if res:
            try:
                return self.ie.recoganize_k(os.path.join(self.path, 'temp.jpg'), tg)
            except PermissionError as e:
                print(f"Permission Error: {e}. Please close the Excel file and try again.")
                return None
        else:
            return None
        
