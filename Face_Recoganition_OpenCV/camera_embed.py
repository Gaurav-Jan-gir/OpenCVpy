import cv2 as cv
import tkinter as tk
from PIL import Image, ImageTk
import os
import datetime
import time
import platform

def show_camera_embed(parent_frame,fps,cap,control_flag,latest_frame, st = [None] ,path_save = None,camera_frame_size=(640, 480), camera_index=0, resolution=(640, 480)):
    if(fps < 6):
        fps = 6
    cam_label = tk.Label(parent_frame)
    cam_label.grid(row=0, column=0, padx=10, pady=10)

    if cap[0] is None:
        cap[0] = cv.VideoCapture(camera_index)
        cap[0].set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))  # Set codec to MJPG for better compatibility
        cap[0].set(cv.CAP_PROP_FRAME_WIDTH, resolution[0])
        cap[0].set(cv.CAP_PROP_FRAME_HEIGHT, resolution[1])
        cap[0].set(cv.CAP_PROP_FPS, fps)

    def update_frame():
        if cap[0] is None:
            return
        ret, frame = cap[0].read()
        if ret:
            frame = cv.resize(frame, camera_frame_size)
            latest_frame[0] = frame
            if path_save is not None:
                if not os.path.exists(path_save):
                    os.makedirs(path_save)
                i = 0
                file_name = datetime.datetime.now().strftime(f"img_%Y%m%d_%H%M%S_{i}.jpg")
                img_path = os.path.join(path_save, file_name)
                while os.path.exists(img_path):
                    i += 1
                    file_name = datetime.datetime.now().strftime(f"img_%Y%m%d_%H%M%S_{i}.jpg")
                    img_path = os.path.join(path_save, file_name)
                if st[0] is not None:
                    st[0].append(img_path)
                cv.imwrite(img_path, frame)
                if platform.system() != "Windows":
                    for _ in range(3):
                        try:
                            test_img = cv.imread(img_path)
                            if test_img is None:
                                raise ValueError("Image not read correctly")
                            break
                        except Exception as e:
                            time.sleep(0.01)

            frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(img)
            cam_label.img_tk = img_tk
            cam_label.config(image=img_tk)
        if control_flag:
            actual_fps = cap[0].get(cv.CAP_PROP_FPS)
            if actual_fps > 0:
                cam_label.after(int(1000/actual_fps), update_frame)
            else:
                cam_label.after(int(1000/fps), update_frame)
    if control_flag:
        update_frame()

def destroy_camera(cap):
    if cap is not None and cap[0] is not None:
        cap[0].release()
    cv.destroyAllWindows()

def show_image_embed(parent_frame, img):
    img_label = tk.Label(parent_frame)
    img_label.grid(row=0, column=0, padx=10, pady=10)
    if img is not None:
        img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)
        img_label.img_tk = img_tk
        img_label.config(image=img_tk)
    else:
        img_label.config(text="No image available")

# def cont_camera_capture(parent_frame, fps, img_dir,camera_frame_size=(640, 480),camera_index=0):
#     if fps < 6:
#         fps = 6
#     cam_label = tk.Label(parent_frame)
#     cam_label.grid(row=0, column=0, padx=10, pady=10)
#     latest_frame = [None]  # Use list for mutability
#     count = [0]
#     n = 6

#     cap = cv.VideoCapture(camera_index)
#     cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))  # Set codec to MJPG for better compatibility
#     cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
#     cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

#     def update_frame():
#         ret, frame = cap.read()
#         if ret:
#             frame = cv.resize(frame, camera_frame_size)
#             latest_frame[0] = frame
#             count[0] += 1
#             frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
#             img = Image.fromarray(frame_rgb)
#             img_tk = ImageTk.PhotoImage(img)
#             cam_label.img_tk = img_tk
#             cam_label.config(image=img_tk)
#             if count[0] % n == 0:
#                 save_image()
#         cam_label.after(int(1000 / fps), update_frame)

#     def save_image():
#         if latest_frame[0] is not None:
#             if not os.path.exists(img_dir):
#                 os.makedirs(img_dir)
#             file_name = datetime.datetime.now().strftime("img_%Y%m%d_%H%M%S.jpg")
#             img_path = os.path.join(img_dir, file_name)
#             cv.imwrite(img_path, latest_frame[0])

#     update_frame()

#     def on_close():
#         cap.release()
#         parent_frame.quit()

#     parent_frame.protocol("WM_DELETE_WINDOW", on_close)


