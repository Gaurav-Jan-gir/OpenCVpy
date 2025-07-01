import cv2 as cv

if __name__ == "__main__":
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Failed to open camera.")

    # Try different codecs
    cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
    # OR
    # cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'RGB3'))
    # OR just remove the codec setting entirely

    while True:
        ret, frame = cap.read()
        if not ret:
            raise RuntimeError("Failed to read frame from camera.")
        
        cv.imshow("Camera Feed", frame)
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.set(cv.CAP_PROP_GAMMA, 300)

    defaults = {
        'camera_index': 0,
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
        'camera_color_temperature': cap.get(cv.CAP_PROP_WB_TEMPERATURE) if hasattr(cv, 'CAP_PROP_WB_TEMPERATURE') else 0
    }
    print(defaults)

    
    print("Camera opened successfully.")
    cap.release()
    cv.destroyAllWindows()