import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def welcome_message():
    while True:
        clear_screen()
        print("Welcome to the face recognition system")
        print("1. Register a new user via Camera")
        print("2. Register a new user via Image")
        print("3. Start Recognition")
        print("4. Check if User Data exist or not.")
        print("5. Configure Confidence Levels (Default 60%)")
        print("6. Configure Camera Settings")
        print("7. Operate on data in Excel.")
        print("8. Load Custom Excel File")
        print("9. Export Data to csv")
        print("10. Exit")
        return loop_int("Enter your choice: ", range_min=1, range_max=10)

def user_already_exists(name, id, score, show_confidence=True):
    clear_screen()
    if show_confidence:
        print(f"User {name} with ID {id} already exists with confidence score {(1-score)*100:.2f}%.")
    else:
        print(f"User {name} with ID {id} already exists.")
    print("1. Register Duplicate User")
    print("2. Update Existing User")
    print("3. Exit")
    return loop_int("Enter your choice: ", range_min=1, range_max=3)

def config_confidence_menu(confidence_match, confidence_save):
    clear_screen()
    print("Configure Confidence Levels")
    print("Current Values")
    print(f"Confidence Level for Saving User Data: {int((1-confidence_save) * 100)}%")
    print(f"Confidence Level for Recognizing User Data: {int((1-confidence_match) * 100)}%")
    print("---------------------------")
    print("1. Set Confidence Level for Saving User Data (Default 60%)")
    print("2. Set Confidence Level for Recognizing User Data (Default 60%)")
    print("3. Back to Main Menu")
    return loop_int("Enter your choice: ", range_min=1, range_max=3)
    
def recognition_cli():
    clear_screen()
    print("Recognition Mode")
    print("1. Real Time Recognition")
    print("2. Recognition with keypress")
    print("3. Exit")
    return loop_int("Enter your choice: ", range_min=1, range_max=3)
    
def excel_menu():
    clear_screen()
    print("📄 Excel Operations Menu")
    print("------------------------")
    print("1. Check user entry on a specific date")
    print("2. Check user entries in a time range")
    print("3. Get all entries of a user")
    print("4. Manually create user entry with current date/time")
    print("5. Manually create user entry with manual date/time")
    print("6. Delete a user entry") 
    print("7. Back to Main Menu")
    return loop_int("Enter your choice: ", range_min=1, range_max=7)
    
def configure_camera_menu():
    clear_screen()
    print("📷 Camera Configuration Menu")
    print("Enter -1 value to use default values of set to auto.")
    print("----------------------------")
    print("1. Preview Camera")
    print("2. Set Camera Index")
    print("3. Set Camera Resolution")
    print("4. Set Frame Rate")
    print("5. Light Control")
    print("6. Save Camera Settings")
    print("7. Back to Main Menu")
    return loop_int("Enter your choice: ", range_min=1, range_max=7)
    
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

    