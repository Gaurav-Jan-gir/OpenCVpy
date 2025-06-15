import cv2 as cv
import os
import datetime
import sys

def get_safe_data_path():
    base_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'data','captured_camera_frames')
    os.makedirs(data_path, exist_ok=True)
    return data_path

class Capture_camera_frames:
    def __init__(self):
        self.path = get_safe_data_path()
        os.makedirs(self.path, exist_ok=True)  # Ensure folder exists
        self.fps = 30  # Default frames per second
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        
    
    def run(self, fps, q):
        fps = self.adjust_frame_perseconds(fps)
        self.capture_camera_frames(q)

    def capture_camera_frames(self,q):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        
        cam = cv.VideoCapture(0)
        if not cam.isOpened():
            print("Could not open camera. Please check your camera connection.")
            return
        cam.set(cv.CAP_PROP_FRAME_WIDTH, 640)  # Set frame width
        cam.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
        
        i=0
        self.fps = max(self.fps, 6)  # Ensure minimum FPS is 6
        
        
        while True:
            ret, frame = cam.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            cv.imshow('Live Capture - Press \'q\' to Quit', frame)
            key = cv.waitKey(int(1000/self.fps)) & 0xFF
            
            img_path = os.path.join(self.path, f'img_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}')+f'_{i}.jpg'
            i += 1
            if(i%(int(self.fps/6))==0):
                cv.imwrite(img_path, frame)
                q.put(img_path)  # Add the image path to the queue
            if key == ord('q'):
                print("Capture cancelled.")
                break

        cam.release()
        cv.destroyAllWindows()
        q.put('q')  # Signal that the capture is done

    def adjust_frame_perseconds(self,fps):
        if fps <= 0:
            print("FPS must be a positive integer.")  # Default FPS
        self.fps = fps


if __name__ == "__main__":
    cap = Capture_camera_frames()
    cap.run(30, None)  # Adjust FPS as needed
    print("Capture completed.")