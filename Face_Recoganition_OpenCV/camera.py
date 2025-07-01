import cv2 as cv
from face_recognition import face_encodings,face_locations
import camera_range_manager as crm

def release(cap):
    cap.release()
    cv.destroyAllWindows()

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

def set_lb(cap, value, camera_index, ranges = None):
    if cap.get(cv.CAP_PROP_GAMMA) != -1:
        if ranges is None:
            cap.set(cv.CAP_PROP_GAMMA, value)
            return
        if (camera_index, cv.CAP_PROP_GAMMA) not in ranges:
            ranges[(camera_index, cv.CAP_PROP_GAMMA)] = crm.get_range(cv.CAP_PROP_GAMMA, cap)
        range_info = ranges[(camera_index, cv.CAP_PROP_GAMMA)]
        if range_info:
            com_value = range_info[0] + ((range_info[1] - range_info[0]) * value)
            cap.set(cv.CAP_PROP_GAMMA, com_value)
    
    else:
        if ranges is None:
            cap.set(cv.CAP_PROP_BRIGHTNESS, value)
            return
        if (camera_index, cv.CAP_PROP_BRIGHTNESS) not in ranges:
            ranges[(camera_index, cv.CAP_PROP_BRIGHTNESS)] = crm.get_range(cv.CAP_PROP_BRIGHTNESS, cap)
        range_info = ranges[(camera_index, cv.CAP_PROP_BRIGHTNESS)]
        if range_info:
            com_value = range_info[0] + ((range_info[1] - range_info[0]) * value)
            cap.set(cv.CAP_PROP_BRIGHTNESS, com_value)

class Camera:
    def __init__(self, camera_config):
        self.camera_config = camera_config
        self.ranges = {}

    def set_camera(self, config = None, cam_defaults=None):
        if config is None:
            config = self.camera_config
        if cam_defaults is None or config['camera_index'] not in cam_defaults:
            cam_defaults[config['camera_index']] = self.get_defaults(config['camera_index'])
        
        cap = cv.VideoCapture(config['camera_index'])
        cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
        cap.set(cv.CAP_PROP_FRAME_WIDTH, config['camera_resolution'][0])
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, config['camera_resolution'][1])
        cap.set(cv.CAP_PROP_FPS, config['camera_fps'])
        if config['camera_light_balance'] == -1:
            set_lb(cap, cam_defaults[config['camera_index']]['camera_light_balance'], config['camera_index'])
        else:
            set_lb(cap, config['camera_light_balance'],config['camera_index'], self.ranges)

        if not cap.isOpened():
            raise RuntimeError(f"Failed to open camera with index {config['camera_index']}.")
        return cap
    
    def capture_image(self, config=None, cam_defaults=None):
        cap = self.set_camera(config, cam_defaults)
        while True:
            ret, frame = cap.read()
            if ret:
                cv.imshow("Press 's' to save, 'q' to quit", frame)
                key = cv.waitKey(1) & 0xFF
                if key == ord('q'):
                    release(cap)
                    return None
                elif key == ord('s'):
                    release(cap)
                    return frame
            else:
                raise RuntimeError("Failed to capture image from camera.")

    @staticmethod
    def get_face_locations(image):
        if image is None:
            raise ValueError("Image cannot be None.")
        return face_locations(image)
    
    @staticmethod
    def get_face_encodings(image, known_face_locations=None):
        if image is None:
            raise ValueError("Image cannot be None.")
        return face_encodings(image, known_face_locations=known_face_locations)
    
    @staticmethod
    def img_read(image_path):
        if not image_path:
            raise ValueError("Image path cannot be empty.")
        img = cv.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Image file {image_path} not found.")
        return img
    
    @staticmethod
    def put_rect(image, face_location):
        if image is None or face_location is None:
            raise ValueError("Image and face location cannot be None.")
        top, right, bottom, left = face_location
        cv.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        return image
    
    @staticmethod
    def show_image(image):
        if image is None:
            raise ValueError("Image cannot be None.")
        cv.imshow("Image", image)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def capture_real_time(self, ls, stop_event,config=None, cam_defaults=None):
        cap = self.set_camera(config, cam_defaults)
        while True:
            ret, frame = cap.read()
            if ret:
                cv.imshow("Real-time Feed Press 'q' to quit", frame)
                ls.append(frame)
                if cv.waitKey(1) & 0xFF == ord('q'):
                    release(cap)
                    stop_event.set()
                    break
            else:
                raise RuntimeError("Failed to capture real-time feed from camera.")

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
        print(cap.get(cv.CAP_PROP_FRAME_WIDTH), cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        if abs(cap.get(cv.CAP_PROP_FRAME_WIDTH) - resolution[0]) < 2 and abs(cap.get(cv.CAP_PROP_FRAME_HEIGHT) - float(resolution[1])) < 2:
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
        if abs(cap.get(cv.CAP_PROP_FPS) - fps) < 1e-2:
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
        
        if cap.get(cv.CAP_PROP_GAMMA) != -1:
            clb = cap.get(cv.CAP_PROP_GAMMA)
        elif cap.get(cv.CAP_PROP_EXPOSURE) != -1:
            clb = cap.get(cv.CAP_PROP_EXPOSURE)
        else:
            clb = cap.get(cv.CAP_PROP_BRIGHTNESS)
        
        defaults = {
            'camera_index': camera_index,
            'camera_resolution': (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))),
            'camera_fps': cap.get(cv.CAP_PROP_FPS),
            'camera_light_balance': clb
        }
        release(cap)
        return defaults

    @staticmethod
    def restore_defaults(cam_defaults):
        for camera_index, defaults in cam_defaults.items():
            cap = cv.VideoCapture(camera_index)
            if not cap.isOpened():
                raise RuntimeError(f"Failed to open camera with index {camera_index}.")  
            set_lb(cap, defaults['camera_light_balance'], camera_index)
            release(cap)

    @staticmethod
    def resize_image(image, width=None, height=None):
        if image is None:
            print("Error: No image provided for resizing.")
            return None
        if width is None and height is None:
            print("Error: At least one of width or height must be specified.")
            return image
        h, w = image.shape[:2]
        if width is None:
            width = int((height / h) * w)
        elif height is None:
            height = int((width / w) * h)
        resized_image = cv.resize(image, (width, height))
        return resized_image

    @staticmethod
    def get_available_cameras(max_cameras=10):
        available_cams = []
        for i in range(max_cameras):
            try:
                cam = cv.VideoCapture(i)
            except cv.error as e:
                break
            if cam.isOpened():
                available_cams.append(i)
                cam.release()
            elif len(available_cams) > 0:
                break
        if not available_cams:
            print("No cameras found.")
        return available_cams

