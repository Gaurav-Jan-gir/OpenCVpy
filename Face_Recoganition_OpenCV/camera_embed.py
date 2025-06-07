import cv2 as cv
from face_recognition import face_locations, face_encodings
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import datetime

def show_camera_embed(parent_frame,fps, img_dir):
    if(fps < 6):
        fps = 6
    cam_label = tk.Label(parent_frame)
    cam_label.grid(row=0, column=0, padx=10, pady=10)
    latest_frame = [None]  
    flag = [False]  # Use list for mutability

    cap =cv.VideoCapture(0)
    def update_frame():
        ret, frame = cap.read()
        if ret:
            latest_frame[0] = frame
            frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(img)
            cam_label.img_tk = img_tk
            cam_label.config(image=img_tk)
        cam_label.after(int(1000/fps), update_frame)
    update_frame()
    
    def save_image():
        if latest_frame[0] is not None:
            if not os.path.exists(img_dir):
                os.makedirs(img_dir)
            img_path = os.path.join(img_dir, 'latest_frame.jpg')
            cv.imwrite(img_path, latest_frame[0])
            flag[0] = True
            

    save_btn = ttk.Button(parent_frame, text="Save Image", command=save_image)
    save_btn.grid(row=1, column=0, padx=10, pady=10)

    def on_close():
        cap.release()
        parent_frame.quit()
        return flag[0]
    parent_frame.protocol("WM_DELETE_WINDOW", on_close)

def cont_camera_capture(parent_frame, fps, img_dir):
    if fps < 6:
        fps = 6
    cam_label = tk.Label(parent_frame)
    cam_label.grid(row=0, column=0, padx=10, pady=10)
    latest_frame = [None]  # Use list for mutability
    count = [0]
    n = 6

    cap = cv.VideoCapture(0)

    def update_frame():
        ret, frame = cap.read()
        if ret:
            latest_frame[0] = frame
            count[0] += 1
            frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(img)
            cam_label.img_tk = img_tk
            cam_label.config(image=img_tk)
            if count[0] % n == 0:
                save_image()
        cam_label.after(int(1000 / fps), update_frame)

    def save_image():
        if latest_frame[0] is not None:
            if not os.path.exists(img_dir):
                os.makedirs(img_dir)
            file_name = datetime.datetime.now().strftime("img_%Y%m%d_%H%M%S.jpg")
            img_path = os.path.join(img_dir, file_name)
            cv.imwrite(img_path, latest_frame[0])

    update_frame()

    def on_close():
        cap.release()
        parent_frame.quit()

    parent_frame.protocol("WM_DELETE_WINDOW", on_close)


