import Interface_excel as Interface
import sys
import create_backup as backup
import os
import traceback

def get_safe_data_path(folder_name='data'):
    base_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
    data_path = os.path.join(base_dir, folder_name)
    os.makedirs(data_path, exist_ok=True)
    return data_path

backup_dir = get_safe_data_path('backup')
data_dir = get_safe_data_path('data')

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    os.makedirs(backup_dir, exist_ok=True)  # Ensure backup directory exists
    os.makedirs(data_dir, exist_ok=True)  # Ensure data directory exists
    excel_path = os.path.join(data_dir, 'data.xlsx')
    config_path = os.path.join(data_dir, 'config.json')
    # If you want to allow custom Excel/config paths when running directly,
    # uncomment the following block. For bundled (PyInstaller) use, keep it commented.
    # if len(sys.argv) > 1:
    #     if sys.argv[1]:
    #         excel_path = sys.argv[1]
    #         if not os.path.exists(excel_path):
    #             print(f"Excel file '{excel_path}' does not exist.")
    #             if input("Do you want to continue with the default path? (y/n): ").strip().lower() != 'y':
    #                 sys.exit(1)
    #         if not excel_path.endswith('.xlsx'):
    #             print(f"Invalid file format for '{excel_path}'.")
    #             if input("Do you want to continue with the default path? (y/n): ").strip().lower() != 'y':
    #                 sys.exit(1)
            
    # if len(sys.argv) >2 and sys.argv[2]:  # Fix: Add () for method call
    #     config_path = sys.argv[2]

    try:
         backup.create_backup(data_dir, excel_path,backup_dir)
    except Exception as e:
        print(f"An error occurred while creating backup: {e}")
        if input("Do you want to continue without backup? (y/n): ").strip().lower() != 'y':
            sys.exit(1)
    try:
        Interface.interFace(excel_path , config_path)
        backup.remove_backup(backup_dir)
    except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            print("Please check the configuration and try again.")
            if input("Do you want to restore backup? (y/n): ").strip().lower() == 'y':
                backup.restore_backup(backup_dir, data_dir, excel_path)
            sys.exit(1)