import os

def message(message,input_key = False):
        if message:    
            print(f"{message}")
        if input_key:
            print()
            input("Press any key to continue...")
            os.system('cls' if os.name == 'nt' else 'clear')

def interfaceSaveData(name, id ,conf, showConfidence=False):
        if not showConfidence:
            print(f'User already exists with\nName: {name} and ID: {id}')
        else:
            print(f'User already exists with\nName: {name} and ID: {id} with confidence {(1-conf)*100:.2f}%')
        print('Press 1 to Save Current data with existing Name and ID')
        print('Press 2 to Save current data with new Name and ID')
        print('Press 3 to Update existing data with new Name and ID')
        print('Press any other key to abort saving current data')
        choice = input()
        if(choice=='1'):
            return 1
        elif(choice=='2'):
            return 2
        elif(choice=='3'):
            return 3
        else:
            return 0

def input_data():
        name = input("Enter User Name for the face detected: ")
        id = input("Enter User ID for the face detected: ")
        return name, id
        

    
