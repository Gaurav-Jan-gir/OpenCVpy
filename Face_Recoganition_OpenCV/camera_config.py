import os
import json
import cv2 as cv
import camera_range_manager as crm

def set_attr(prop_id, cap, value, ranges, camera_index):
    if prop_id[1] is not None:
        if value < 0:
            cap.set(prop_id[0], prop_id[1])
        else:
            cap.set(prop_id[0], 0)
    
    if (camera_index, prop_id[0]) not in ranges:
        ranges[(camera_index, prop_id[0])] = crm.get_range(prop_id[0], cap)
    
    range_info = ranges[(camera_index, prop_id[0])]
    if range_info:
        com_value = range_info[0] + ((range_info[1] - range_info[0]) * value)
        cap.set(prop_id[0], com_value)
    
    return range_info

def release(cap):
    cap.release()
    cv.destroyAllWindows()

class Camera:
    def __init__(self):
        pass

    @staticmethod
    def test_camera_idx(camera_index):
        cap = cv.VideoCapture(camera_index)
        if not cap.isOpened():
            print(f"Camera with index {camera_index} is not available.")
            release(cap)
            return False
        else:
            release(cap)
            return True

    @staticmethod
    def test_camera_resolution(config, resolution):
        cap = cv.VideoCapture(config['camera_index'])
        cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
        cap.set(cv.CAP_PROP_FRAME_WIDTH, resolution[0])
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, resolution[1])
        if cap.get(cv.CAP_PROP_FRAME_WIDTH) == resolution[0] and cap.get(cv.CAP_PROP_FRAME_HEIGHT) == resolution[1]:
            release(cap)
            return True
        else:
            print(f"Camera with index {config['camera_index']} does not support resolution {resolution}.")
            release(cap)
            return False
        
    @staticmethod
    def test_camera_fps(config,fps):
        cap = cv.VideoCapture(config['camera_index'])
        cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
        cap.set(cv.CAP_PROP_FRAME_WIDTH, config['camera_resolution'][0])
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, config['camera_resolution'][1])
        cap.set(cv.CAP_PROP_FPS, fps)
        if cap.get(cv.CAP_PROP_FPS) == fps:
            release(cap)
            return True
        else:
            print(f"Camera with index {config['camera_index']} does not support FPS {fps} with resolution {config['camera_resolution']}.")
            release(cap)
            return False
        
    @staticmethod
    def get_defaults(camera_index):
        cap = cv.VideoCapture(camera_index)
        if not cap.isOpened():
            raise RuntimeError(f"Failed to open camera with index {camera_index}.")
        
        defaults = {
            'camera_index': camera_index,
            'camera_resolution': (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))),
            'camera_fps': cap.get(cv.CAP_PROP_FPS),
            'camera_focus': cap.get(cv.CAP_PROP_FOCUS),
            'camera_brightness': cap.get(cv.CAP_PROP_BRIGHTNESS),
            'camera_contrast': cap.get(cv.CAP_PROP_CONTRAST),
            'camera_saturation': cap.get(cv.CAP_PROP_SATURATION),
            'camera_exposure': cap.get(cv.CAP_PROP_EXPOSURE),
            'camera_gain': cap.get(cv.CAP_PROP_GAIN),
            'camera_hue': cap.get(cv.CAP_PROP_HUE) if hasattr(cv, 'CAP_PROP_HUE') else 0,
            'camera_sharpness': cap.get(cv.CAP_PROP_SHARPNESS) if hasattr(cv, 'CAP_PROP_SHARPNESS') else 0,
            'camera_gamma': cap.get(cv.CAP_PROP_GAMMA) if hasattr(cv, 'CAP_PROP_GAMMA') else 0,
            'camera_white_balance': cap.get(cv.CAP_PROP_WHITE_BALANCE_BLUE_U) if hasattr(cv, 'CAP_PROP_WHITE_BALANCE_BLUE_U') else 0,
            'camera_color_temperature': cap.get(cv.CAP_PROP_WB_TEMPERATURE) if hasattr(cv, 'CAP_PROP_WB_TEMPERATURE') else 0,
            'camera_auto_exposure': cap.get(cv.CAP_PROP_AUTO_EXPOSURE) if hasattr(cv, 'CAP_PROP_AUTO_EXPOSURE') else 0,
            'camera_auto_focus': cap.get(cv.CAP_PROP_AUTOFOCUS) if hasattr(cv, 'CAP_PROP_AUTOFOCUS') else 0,
            'camera_auto_white_balance': cap.get(cv.CAP_PROP_AUTO_WB) if hasattr(cv, 'CAP_PROP_AUTO_WB') else 0
        }
        print(defaults)
        
        release(cap)
        return defaults

    @staticmethod
    def restore_defaults(cam_defaults):
        for camera_index, defaults in cam_defaults.items():
            cap = cv.VideoCapture(camera_index)
            if not cap.isOpened():
                raise RuntimeError(f"Failed to open camera with index {camera_index}.")
            
            try:
                # Basic properties
                cap.set(cv.CAP_PROP_FRAME_WIDTH, defaults['camera_resolution'][0])
                cap.set(cv.CAP_PROP_FRAME_HEIGHT, defaults['camera_resolution'][1])
                cap.set(cv.CAP_PROP_FPS, defaults['camera_fps'])

                cap.set(cv.CAP_PROP_FOCUS, defaults['camera_focus'])
                cap.set(cv.CAP_PROP_EXPOSURE, defaults['camera_exposure'])
                cap.set(cv.CAP_PROP_WB_TEMPERATURE, defaults['camera_color_temperature'])
                cap.set(cv.CAP_PROP_WHITE_BALANCE_BLUE_U, defaults['camera_white_balance'])
                
                # Set to auto mode for supported properties
                cap.set(cv.CAP_PROP_AUTOFOCUS, defaults['camera_auto_focus'])        # Auto focus
                cap.set(cv.CAP_PROP_AUTO_WB, defaults['camera_auto_white_balance'])          # Auto white balance & color temp
                cap.set(cv.CAP_PROP_AUTO_EXPOSURE, defaults['camera_auto_exposure'])    # Auto exposure
                
                # Manual properties - set to defaults
                cap.set(cv.CAP_PROP_BRIGHTNESS, defaults.get('camera_brightness', 0.5))
                cap.set(cv.CAP_PROP_CONTRAST, defaults.get('camera_contrast', 0.5))
                cap.set(cv.CAP_PROP_SATURATION, defaults.get('camera_saturation', 0.5))
                cap.set(cv.CAP_PROP_GAIN, defaults.get('camera_gain', 0.5))
                
                # Optional properties with checks
                if hasattr(cv, 'CAP_PROP_HUE'):
                    cap.set(cv.CAP_PROP_HUE, defaults.get('camera_hue', 0.5))
                if hasattr(cv, 'CAP_PROP_SHARPNESS'):
                    cap.set(cv.CAP_PROP_SHARPNESS, defaults.get('camera_sharpness', 0.5))
                if hasattr(cv, 'CAP_PROP_GAMMA'):
                    cap.set(cv.CAP_PROP_GAMMA, defaults.get('camera_gamma', 0.5))
                
            except Exception as e:
                print(f"Error restoring defaults for camera {camera_index}: {e}")
            finally:
                release(cap)
    
    def capture_image(self, config=None, cam_defaults=None):
        if cam_defaults is not None and config['camera_index'] not in cam_defaults:
            cam_defaults[config['camera_index']] = self.get_defaults(config['camera_index'])
        if config is None:
            config = self.camera_config

        cap = cv.VideoCapture(config['camera_index'])

        try:
            cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
            cap.set(cv.CAP_PROP_FRAME_WIDTH, config['camera_resolution'][0])
            cap.set(cv.CAP_PROP_FRAME_HEIGHT, config['camera_resolution'][1])
            cap.set(cv.CAP_PROP_FPS, config['camera_fps'])

            property_mappings = {
                'brightness': (cv.CAP_PROP_BRIGHTNESS, None),
                'focus': (cv.CAP_PROP_FOCUS, cam_defaults[config['camera_index']]['camera_focus']),
                'contrast': (cv.CAP_PROP_CONTRAST, None),
                'saturation': (cv.CAP_PROP_SATURATION, None),
                'exposure': (cv.CAP_PROP_EXPOSURE, cam_defaults[config['camera_index']]['camera_auto_exposure']),
                'gain': (cv.CAP_PROP_GAIN, None),
                'hue': (cv.CAP_PROP_HUE if hasattr(cv, 'CAP_PROP_HUE') else None, None),
                'sharpness': (cv.CAP_PROP_SHARPNESS if hasattr(cv, 'CAP_PROP_SHARPNESS') else None, None),
                'gamma': (cv.CAP_PROP_GAMMA if hasattr(cv, 'CAP_PROP_GAMMA') else None, None),
                'white_balance': (cv.CAP_PROP_WHITE_BALANCE_BLUE_U if hasattr(cv, 'CAP_PROP_WHITE_BALANCE_BLUE_U') else None, cam_defaults[config['camera_index']]['camera_auto_white_balance']),
                'color_temperature': (cv.CAP_PROP_WB_TEMPERATURE if hasattr(cv, 'CAP_PROP_WB_TEMPERATURE') else None, cam_defaults[config['camera_index']]['camera_auto_white_balance'])
            }
            try:
                for prop_name, prop_id in property_mappings.items():
                    if prop_id is not None and prop_name in config:
                        set_attr(prop_id, cap, config[f'camera_{prop_name}'],self.ranges, config['camera_index'])
            except Exception as e:
                print(f"Error can't set properties : {e}")
            
            for prop_name, prop_id in property_mappings.items():
                if prop_id[0] is not None:
                    try:
                        value = cap.get(prop_id[0])
                        print(f"  {prop_name}: {value}")
                    except Exception as e:
                        print(f"  {prop_name}: Error reading ({e})")
                else:
                    print(f"  {prop_name}: Not supported")
            
        except Exception as e:
            print(f"Error setting camera properties: {e}")

        if not cap.isOpened():
            raise RuntimeError(f"Failed to open camera with index {config['camera_index']}.")
        
        while True:
            ret, frame = cap.read()
            if ret:
                cv.imshow("Camera Feed", frame)
                key = cv.waitKey(1) & 0xFF
                if key == ord('q'):
                    release(cap)
                    return None
                elif key == ord('s'):
                    release(cap)
                    return frame
            else:
                raise RuntimeError("Failed to capture image from camera.")

def configure_camera_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("📷 Camera Configuration Menu")
    print("Enter -1 value to use default values of set to auto.")
    print("----------------------------")
    print("1. Preview Camera")
    print("2. Set Camera Index")
    print("3. Set Camera Resolution")
    print("4. Set Frame Rate")
    print("5. Set Focus")
    print("6. Set Brightness")
    print("7. Set Contrast")
    print("8. Set Saturation")
    print("9. Set Exposure")
    print("10. Set Gain")
    print("11. Set Hue")
    print("12. Set Sharpness")
    print("13. Set White Balance")
    print("14. Set Gamma")
    print("15. Set Color Temperature")
    print("16. Save Camera Settings")
    print("17. Back to Main Menu")
    return loop_int("Enter your choice: ", range_min=1, range_max=17)
    
def input_int(prompt, default=None, range_min=None, range_max=None):
    try:
        value = int(input(prompt))
        if range_min is None and range_max is not None:
            if value > range_max:
                raise ValueError(f"Value must be less than or equal to {range_max}.")
        elif range_max is None and range_min is not None:
            if value < range_min:
                raise ValueError(f"Value must be greater than or equal to {range_min}.")
        elif range_min is not None and range_max is not None:
            if value < range_min or value > range_max:
                raise ValueError(f"Value must be between {range_min} and {range_max}.")
        return value
    except ValueError:
        if default is not None:
            print(f"Invalid input. Using default value: {default}")
            return default
        else:
            return None
    
def loop_int(prompt, range_min=None, range_max=None):
    while True:
        value = input_int(prompt, None, range_min, range_max)
        if value is not None:
            return value
        else:
            if range_min is not None and range_max is not None:
                print(f"Invalid input. Please enter a valid int between {range_min} and {range_max}.")
            else:
                print("Invalid input. Please enter a valid integer.")

class CameraConfig:
    def __init__(self):
        self.config = self.load_config()
        self.camera_config = {
            'camera_index': self.config['camera_index'] if 'camera_index' in self.config else 0, 
            'camera_resolution': self.config['camera_resolution'] if 'camera_resolution' in self.config else (640, 480),
            'camera_fps': self.config['camera_fps'] if 'camera_fps' in self.config else 30,
            'camera_focus': self.config.get('camera_focus', -1),
            'camera_brightness': self.config['camera_brightness'] if 'camera_brightness' in self.config else 0.5,
            'camera_contrast': self.config['camera_contrast'] if 'camera_contrast' in self.config else 0.5,
            'camera_saturation': self.config['camera_saturation'] if 'camera_saturation' in self.config else 0.5,
            'camera_exposure': self.config['camera_exposure'] if 'camera_exposure' in self.config else 0.5,
            'camera_gain': self.config['camera_gain'] if 'camera_gain' in self.config else 0.5,
            'camera_hue': self.config.get('camera_hue', 0),
            'camera_sharpness': self.config.get('camera_sharpness', 0),
            'camera_gamma': self.config.get('camera_gamma', 0),
            'camera_white_balance': self.config.get('camera_white_balance', -1),
            'camera_color_temperature': self.config.get('camera_color_temperature', -1),
        }

    def load_config(self):
        cam0_defaults = Camera.get_defaults(0)
        default_config = {
            "tolerance": 0.4,
            "camera_index": 0,
            "camera_resolution": (640, 480),
            "camera_fps": 30,
            "camera_focus": cam0_defaults.get('camera_focus', -1),
            "camera_brightness": cam0_defaults['camera_brightness'],
            "camera_contrast": cam0_defaults['camera_contrast'],
            "camera_saturation": cam0_defaults['camera_saturation'],
            "camera_exposure": cam0_defaults['camera_exposure'] if 'camera_exposure' in cam0_defaults else -1,
            "camera_gain": cam0_defaults['camera_gain'],
            "camera_hue": cam0_defaults.get('camera_hue', 0),
            "camera_sharpness": cam0_defaults.get('camera_sharpness', 0),
            "camera_gamma": cam0_defaults.get('camera_gamma', 0),
            "camera_white_balance": cam0_defaults.get('camera_white_balance', -1),
            "camera_color_temperature": cam0_defaults.get('camera_color_temperature', -1),
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